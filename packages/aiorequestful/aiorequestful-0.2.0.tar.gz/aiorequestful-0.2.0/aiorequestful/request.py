"""
All operations relating to handling of requests to an API.
"""
import asyncio
import contextlib
import inspect
import json
import logging
from collections.abc import Mapping, Callable
from datetime import datetime, timedelta
from http import HTTPStatus
from typing import Any, Self, Unpack
from urllib.parse import unquote

import aiohttp
from aiohttp import ClientResponse, ClientSession
from yarl import URL

from aiorequestful._utils import format_url_log
from aiorequestful.auth import Authoriser
from aiorequestful.cache.backend import ResponseCache
from aiorequestful.cache.session import CachedSession
from aiorequestful.exception import RequestError, ResponseError

from aiorequestful.types import JSON, URLInput, Headers, MethodInput, Method, RequestKwargs


class RequestHandler:
    """
    Generic API request handler using cached responses for GET requests only.
    Caches GET responses for a maximum of 4 weeks by default.
    Handles error responses and backoff on failed requests.
    See :py:class:`APIAuthoriser` for more info on which params to pass to authorise requests.

    :param connector: When called, returns a new session to use when making requests.
    :param authoriser: The authoriser to use when authorising requests to the API.
    """

    __slots__ = (
        "logger",
        "_connector",
        "_session",
        "authoriser",
        "backoff_start",
        "backoff_factor",
        "backoff_count",
        "_backoff_start_logged",
        "wait_time",
        "wait_increment",
        "wait_max",
        "_wait_start_logged",
    )

    @property
    def backoff_final(self) -> float:
        """
        The maximum wait time to retry a request in seconds
        until giving up when applying backoff to failed requests
        """
        return self.backoff_start * self.backoff_factor ** self.backoff_count

    @property
    def timeout(self) -> int:
        """The cumulative sum of all backoff intervals up to the final backoff time"""
        return int(sum(self.backoff_start * self.backoff_factor ** i for i in range(self.backoff_count + 1)))

    @property
    def closed(self):
        """Is the stored client session closed."""
        return self._session is None or self._session.closed

    @property
    def session(self) -> ClientSession:
        """The :py:class:`ClientSession` object if it exists and is open."""
        if not self.closed:
            return self._session

    @classmethod
    def create(cls, authoriser: Authoriser | None = None, cache: ResponseCache | None = None, **session_kwargs):
        """Create a new :py:class:`RequestHandler` with an appropriate session ``connector`` given the input kwargs"""
        def connector() -> ClientSession:
            """Create an appropriate session ``connector`` given the input kwargs"""
            if cache is not None:
                return CachedSession(cache=cache, **session_kwargs)
            return ClientSession(**session_kwargs)

        return cls(connector=connector, authoriser=authoriser)

    def __init__(self, connector: Callable[[], ClientSession], authoriser: Authoriser | None = None):
        #: The :py:class:`logging.Logger` for this  object
        self.logger: logging.Logger = logging.getLogger(__name__)

        self._connector = connector
        self._session: ClientSession | CachedSession | None = None

        #: The :py:class:`Authoriser` object
        self.authoriser = authoriser

        #: The initial backoff time in seconds for failed requests
        self.backoff_start = 0.2
        #: The factor by which to increase backoff time for failed requests i.e. backoff_start ** backoff_factor
        self.backoff_factor = 1.932
        #: The maximum number of request attempts to make before giving up and raising an exception
        self.backoff_count = 10
        self._backoff_start_logged = False

        #: The initial time in seconds to wait after receiving a response from a request
        self.wait_time = 0
        #: The amount in seconds to increase the wait time by each time a rate limit is hit i.e. 429 response
        self.wait_increment = 0.1
        #: The maximum time in seconds that the wait time can be incremented to
        self.wait_max = 1
        self._wait_start_logged = False

    async def __aenter__(self) -> Self:
        if self.closed:
            self._session = self._connector()

        await self.session.__aenter__()
        await self.authorise()

        return self

    async def __aexit__(self, __exc_type, __exc_value, __traceback) -> None:
        await self.session.__aexit__(__exc_type, __exc_value, __traceback)
        self._session = None

    async def authorise(self) -> Headers:
        """
        Method for API authorisation which tests/refreshes/reauthorises as needed.

        :return: Headers for request authorisation.
        :raise APIError: If the token cannot be validated.
        """
        if self.closed:
            raise RequestError("Session is closed. Enter the API context to start a new session.")

        headers = {}
        if self.authoriser is not None:
            self.session.headers.update(await self.authoriser())

        return headers

    async def close(self) -> None:
        """Close the current session. No more requests will be possible once this has been called."""
        await self.session.close()

    async def request(self, method: MethodInput, url: URLInput, **kwargs: Unpack[RequestKwargs]) -> JSON:
        """
        Generic method for handling API requests with back-off on failed requests.
        See :py:func:`request` for more arguments.

        :param method: method for the request:
            ``GET``, ``OPTIONS``, ``HEAD``, ``POST``, ``PUT``, ``PATCH``, or ``DELETE``.
        :param url: URL to call.
        :return: The JSON formatted response or, if JSON formatting not possible, the text response.
        :raise APIError: On any logic breaking error/response.
        """
        method = Method.get(method)
        backoff = self.backoff_start

        while True:
            async with self._request(method=method, url=url, **kwargs) as response:
                if response is None:
                    raise RequestError("No response received")

                handled = await self._handle_bad_response(response=response)
                waited = await self._wait_for_rate_limit_timeout(response=response)

                if handled or waited:
                    continue

                if response.ok:
                    data = await self._get_json_response(response)
                    break

                await self._log_response(response=response, method=method, url=url)

                if backoff > self.backoff_final or backoff == 0:
                    raise RequestError("Max retries exceeded")

                # exponential backoff
                self._log_backoff_start()
                self.log(method=method.name, url=url, message=f"Request failed: retrying in {backoff} seconds...")
                await asyncio.sleep(backoff)
                backoff *= self.backoff_factor

        self._backoff_start_logged = False
        return data

    @contextlib.asynccontextmanager
    async def _request(
            self,
            method: Method,
            url: URLInput,
            log_message: str | list[str] = None,
            **kwargs
    ) -> ClientResponse | None:
        """Handle logging a request, send the request, and return the response"""
        if isinstance(log_message, str):
            log_message = [log_message]
        elif log_message is None:
            log_message = []

        if isinstance(self.session, CachedSession):
            log_message.append("Cached Request")
        self.log(method=method.name, url=url, message=log_message, **kwargs)

        if not isinstance(self.session, CachedSession):
            self._clean_requests_kwargs(kwargs)
        if "headers" in kwargs:
            kwargs["headers"].update(self.session.headers)

        try:
            async with self.session.request(method=method.name, url=url, **kwargs) as response:
                yield response
                await asyncio.sleep(self.wait_time)
        except aiohttp.ClientError as ex:
            self.logger.debug(str(ex))
            yield

    @staticmethod
    def _clean_requests_kwargs(kwargs: dict[str, Any]) -> None:
        """Clean ``kwargs`` by removing any kwarg not in the signature of the :py:meth:`aiohttp.request` method."""
        signature = inspect.signature(aiohttp.request).parameters
        for key in list(kwargs):
            if key not in signature:
                kwargs.pop(key)

    def log(
            self, method: str, url: URLInput, message: str | list = None, level: int = logging.DEBUG, **kwargs
    ) -> None:
        """Format and log a request or request adjacent message to the given ``level``."""
        log: list[Any] = []

        url = URL(url)
        if url.query:
            log.extend(f"{k}: {unquote(v):<4}" for k, v in sorted(url.query.items()))
        if kwargs.get("params"):
            log.extend(f"{k}: {v:<4}" for k, v in sorted(kwargs.pop("params").items()))
        if kwargs.get("json"):
            log.extend(f"{k}: {str(v):<4}" for k, v in sorted(kwargs.pop("json").items()))
        if len(kwargs) > 0:
            log.extend(f"{k.title()}: {str(v):<4}" for k, v in kwargs.items() if v)
        if message:
            log.append(message) if isinstance(message, str) else log.extend(message)

        self.logger.log(level=level, msg=format_url_log(method=method, url=url, messages=log))

    def _log_backoff_start(self) -> None:
        if self._backoff_start_logged:
            return

        self.logger.warning(
            "\33[93mRequest failed: retrying using backoff strategy. "
            f"Will retry request {self.backoff_count} more times and timeout in {self.timeout} seconds...\33[0m"
        )
        self._backoff_start_logged = True

    async def _log_response(self, response: ClientResponse, method: Method, url: URLInput) -> None:
        """Log the method, URL, response text, and response headers."""
        response_headers = response.headers
        if isinstance(response.headers, Mapping):  # format headers if JSON
            response_headers = json.dumps(dict(response.headers), indent=2)
        self.log(
            method=method.name,
            url=url,
            message=[
                f"Status code: {response.status}",
                "Response text and headers follow:\n"
                f"Response text:\n\t{(await response.text()).replace("\n", "\n\t")}\n"
                f"Headers:\n\t{response_headers.replace("\n", "\n\t")}"
                f"\33[0m"
            ]
        )

    # TODO: Separate responsibility of handling specific status codes to implementations of a generic abstraction,
    #  and have this handling dependency injected for this handler.
    #  This doesn't follow SOLID very well;
    #  would need to modify function directly to implement handling of new status codes.
    async def _handle_bad_response(self, response: ClientResponse) -> bool:
        """Handle bad responses by extracting message and handling status codes that should raise an exception."""
        response_json = await self._get_json_response(response)
        error_message = response_json.get("error", {}).get("message")
        if error_message is None:
            status = HTTPStatus(response.status)
            error_message = f"{status.phrase} | {status.description}"

        handled = False

        def _log_bad_response(message: str) -> None:
            self.logger.debug(f"Status code: {response.status} | {error_message} | {message}")

        if response.status == 401:
            _log_bad_response("Re-authorising...")
            await self.authorise()
            handled = True
        elif response.status == 429:
            if self.wait_time < self.wait_max:
                self.wait_time += self.wait_increment
                _log_bad_response(f"Rate limit hit. Increasing wait time between requests to {self.wait_time}s")
                handled = True
            else:
                _log_bad_response(f"Rate limit hit and wait time already at maximum of {self.wait_time}s")
        elif 400 <= response.status < 408:
            raise ResponseError(error_message, response=response)

        return handled

    async def _wait_for_rate_limit_timeout(self, response: ClientResponse) -> bool:
        """Handle rate limits when a 'retry-after' time is included in the response headers."""
        if "retry-after" not in response.headers:
            return False

        wait_time = int(response.headers["retry-after"])
        wait_str = (datetime.now() + timedelta(seconds=wait_time)).strftime("%Y-%m-%d %H:%M:%S")

        if wait_time > self.timeout:  # exception if too long
            raise RequestError(
                f"Rate limit exceeded and wait time is greater than timeout of {self.timeout} seconds. "
                f"Retry again at {wait_str}"
            )

        if not self._wait_start_logged:
            self.logger.warning(f"\33[93mRate limit exceeded. Retrying again at {wait_str}\33[0m")
            self._wait_start_logged = True

        await asyncio.sleep(wait_time)
        self._wait_start_logged = False

        return True

    @staticmethod
    async def _get_json_response(response: ClientResponse) -> JSON:
        """Format the response to JSON and handle any errors"""
        try:
            data = await response.json()
            return data if isinstance(data, dict) else {}
        except (aiohttp.ContentTypeError, json.decoder.JSONDecodeError):
            return {}

    async def get(self, url: URLInput, **kwargs) -> JSON:
        """Sends a GET request."""
        kwargs.pop("method", None)
        return await self.request("get", url=url, **kwargs)

    async def post(self, url: URLInput, **kwargs) -> JSON:
        """Sends a POST request."""
        kwargs.pop("method", None)
        return await self.request("post", url=url, **kwargs)

    async def put(self, url: URLInput, **kwargs) -> JSON:
        """Sends a PUT request."""
        kwargs.pop("method", None)
        return await self.request("put", url=url, **kwargs)

    async def delete(self, url: URLInput, **kwargs) -> JSON:
        """Sends a DELETE request."""
        kwargs.pop("method", None)
        return await self.request("delete", url, **kwargs)

    async def options(self, url: URLInput, **kwargs) -> JSON:
        """Sends an OPTIONS request."""
        kwargs.pop("method", None)
        return await self.request("options", url=url, **kwargs)

    async def head(self, url: URLInput, **kwargs) -> JSON:
        """Sends a HEAD request."""
        kwargs.pop("method", None)
        kwargs.setdefault("allow_redirects", False)
        return await self.request("head", url=url, **kwargs)

    async def patch(self, url: URLInput, **kwargs) -> JSON:
        """Sends a PATCH request."""
        kwargs.pop("method", None)
        return await self.request("patch", url=url, **kwargs)

    def __copy__(self):
        """Do not copy handler"""
        return self

    def __deepcopy__(self, _: dict = None):
        """Do not copy handler"""
        return self
