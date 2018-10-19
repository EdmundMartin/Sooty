import asyncio
from typing import Union


import async_timeout

from pyppeteer import launch
from pyppeteer.browser import Browser
from pyppeteer.page import Page
from pyppeteer.errors import PageError

from sooty.exceptions import TimeoutException
from sooty.response import Response


class SootyRender:

    def __init__(self, headless=True, loop=None, proxy=None, auth=None, tabs=3):
        if not loop:
            self.loop = asyncio.get_event_loop()
        else:
            self.loop = loop
        self._headless = headless
        self._proxy = proxy
        self._auth = auth
        self._browser: Union[None, Browser] = None
        self._page_queue = asyncio.Queue()
        self._tabs = tabs
        self._semaphore = asyncio.BoundedSemaphore(1)

    async def _create_browser(self) -> None:
        if self._proxy:
            self._browser = await launch(headless=self._headless,  args=['--proxy-server={}'.format(self._proxy)])
        else:
            self._browser = await launch(headless=self._headless)

    async def _create_pages(self,  threads: int) -> None:
        for p in range(threads):
            page = await self._browser.newPage()
            if self._auth:
                await page.authenticate(self._auth)
            await self._page_queue.put(page)

    @classmethod
    async def create_renderer(cls, headless=True, loop=None, proxy=None, auth=None, coroutines=5):
        self = cls(headless=headless, loop=loop, proxy=proxy, auth=auth)
        await self._create_browser()
        await self._create_pages(coroutines)
        return self

    async def __check_browser_created(self):
        async with self._semaphore:
            if self._browser is None:
                await self._create_browser()
                await self._create_pages(self._tabs)

    async def get_request(self, url: str, timeout: int = 30, post_load_wait: int = 0) -> Response:
        await self.__check_browser_created()
        page_retrieved = False
        page = await self._page_queue.get()
        async with async_timeout.timeout(timeout):
            try:
                page_retrieved = True
                response = await page.goto(url)
            except TimeoutError:
                raise TimeoutException("Request took longer than timeout: {}".format(timeout))
            else:
                if post_load_wait > 0:
                    await asyncio.sleep(post_load_wait)
                page_content = await page.content()
                return Response(url, response.url, page_content, response.status, response.headers)
            finally:
                if page_retrieved:
                    self._page_queue.put_nowait(page)

    async def close(self):
        if self._browser:
            await self._browser.close()
