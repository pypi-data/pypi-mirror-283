"""kawaiipy – async wrapper for Kawaii API"""

from collections.abc import Sequence
from typing import Final, Tuple

from aiohttp.client import ClientSession, ClientTimeout
from aiohttp.client_exceptions import ContentTypeError
from yarl import URL

from kawaiipy.exceptions import KawaiiAPIException
from kawaiipy.types import EndpointsT, ResponseT

BASE_URL: Final[URL] = URL("https://kawaii.red/api/")
"""Base url of Kawaii API"""


class KawaiiAPI:
    """Represents the main class of a wrapper for working with the Kawaii API.

    Args:
        token (str): Access token to the API.
            Default: `anonymous`
        response_type (ResponseT): Specifies the type of responses.
        filter (Sequence[int]): Specify the indexes of the images that you want to retrieve.
            For example, setting `filter=[1]` will make the API return only images with index 1.

            !!! warning
                This don't work actually and I don't know why.
                API just ignore filter in headers.
        timeout (int): Timeout in seconds.
            Default: `3`
    """

    __slots__: Sequence[str] = (
        "session",
        "timeout",
        "token",
        "type",
        "filter",
    )

    def __init__(
        self,
        token: str = "anonymous",
        *,
        type: ResponseT = "json",
        filter: Tuple[int, ...] = (),
        timeout: int = 3,
    ) -> None:
        self.session: ClientSession | None = None
        self.timeout: ClientTimeout = ClientTimeout(timeout)

        self.token: str = token
        self.type: ResponseT = type
        self.filter: Tuple[int, ...] = filter

    async def get(
        self,
        category: EndpointsT,
        sub: str,
        *,
        type: ResponseT = "json",
        filter: Tuple[int, ...] = (),
    ) -> str:
        response_filter: Tuple[int, ...] = filter + self.filter
        if not self.session:
            # A necessary construction, since ClientSession required to be created in something async.
            self.session = ClientSession(
                timeout=self.timeout
            )  # TODO: Add orjson support.
        assert isinstance(self.session, ClientSession)
        try:
            async with self.session.request(
                "GET",
                BASE_URL / category / sub,
                headers={
                    "token": self.token,
                    "type": type,
                    "filter": ",".join(
                        map(str, response_filter)
                    ),  # and I tried at least one variant: `f"[{','.join(map(str, response_filter))}]"` but anyway it's not working
                },
            ) as response:
                if (type or self.type) == "json":
                    data: dict[str, str] = await response.json()
                    output: str | None = data.get("response", None)
                    if output is None:
                        raise KawaiiAPIException(data.get("error", "Unknown error"))
                    return output
                else:
                    output: str | None = await response.text("UTF-8")
                    if output[1:6] != "https":
                        raise KawaiiAPIException(output)
                    return output
        except ContentTypeError:
            raise KawaiiAPIException("Unknown URL")
