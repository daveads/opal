"""
Simple HTTP get data fetcher using requests
supports 
"""

from aiohttp import ClientResponse, ClientSession
from ..fetch_provider import BaseFetchProvider
from ..events import FetcherConfig, FetchEvent
from ..logger import get_logger

logger = get_logger("http_get_fetch_provider")

class HttpGetFetcherConfig(FetcherConfig):
    """
    Config for HttpGetFetchProvider's Adding HTTP headers 
    """
    headers: dict = None
    is_json: bool = True
    process_data: bool = True

class HttpGetFetchEvent(FetchEvent):
    fetcher: str = "HttpGetFetchProvider"
    config: HttpGetFetcherConfig = None

class HttpGetFetchProvider(BaseFetchProvider):

    def __init__(self, event: HttpGetFetchEvent) -> None:
        self._event: HttpGetFetchEvent
        if event.config is None:
            event.config = HttpGetFetcherConfig()
        super().__init__(event)

    async def _fetch_(self):
        logger.debug(f"{self.__class__.__name__} fetching from {self._url}")
        headers = {}
        if self._event.config.headers is not None:
            headers = self._event.config.headers
        async with ClientSession(headers=headers) as session:
            result = await session.get(self._url)
        return result

    async def _process_(self, res: ClientResponse):
        # if we are asked to process the data before return it
        if self._event.config.process_data:
            # if data is JSON
            if self._event.config.is_json:
                return await res.json()
            else:
                return await res.text() 
        # return raw result
        else:
            return res
