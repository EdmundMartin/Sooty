import asyncio
import logging
from typing import Union, Any, List


import async_timeout

from pyppeteer import launch
from pyppeteer.browser import Browser
from pyppeteer.page import Page
from pyppeteer.errors import PageError

from sooty.helpers import get_best_event_loop
from sooty.response import Response
from sooty.exceptions import TimeoutException, ContextError


class Sooty:

    def __init__(self, headless=True, loop=None, proxy=None, auth=None):
        if not loop:
            self.loop = get_best_event_loop()
        else:
            self.loop = loop
        self._headless = headless
        self._proxy = proxy
        self._auth = auth
        self._browser: Union[None, Browser] = None
        self._page: Union[None, Page] = None

    async def _create_browser(self) -> None:
        if self._proxy:
            self._browser = await launch(headless=self._headless,  args=['--proxy-server={}'.format(self._proxy)])
        else:
            self._browser = await launch(headless=self._headless)

    async def _create_page(self) -> None:
        if self._auth:
            self._page = await self._browser.newPage()
            await self._page.authenticate(self._auth)
        else:
            self._page = await self._browser.newPage()

    async def _get_page(self) -> Page:
        if self._page:
            return self._page
        else:
            await self._create_page()
            return self._page

    @classmethod
    async def create_sooty(cls, headless=True, loop=None, proxy=None, auth=None):
        self = cls(headless=headless, loop=loop, proxy=proxy, auth=auth)
        await self._create_browser()
        return self

    async def get_request(self, url: str, timeout: int = 30) -> Response:
        page = await self._get_page()
        async with async_timeout.timeout(timeout):
            try:
                response = await page.goto(url)
            except TimeoutError:
                raise TimeoutException("Request took longer than timeout: {}".format(timeout))
        page_content = await self._page.content()
        return Response(url, response.url, page_content, response.status, response.headers)

    async def get_element(self, selector: str, method: str = 'outerHTML') -> str:
        if not self._page:
            raise ContextError("Get element requires a page as a context")
        try:
            element = await self._page.querySelector(selector)
            element = await self._page.evaluate('(element) => element.{}'.format(method), element)
        except Exception as e:
            raise e
        else:
            return element

    async def get_elements(self, selector: str, method: str = 'outerHTML') -> List[str]:
        if not self._page:
            raise ContextError("Get element requires a page as a context")
        found_elements = []
        try:
            elements = await self.page.querySelectorAll(selector)
            for el in elements:
                element = await self.page.evaluate('(el) => el.{}'.format(method), el)
                found_elements.append(element)
        except Exception as e:
            raise e
        else:
            return found_elements

    async def evaluate_javascript(self, script: str, force: bool = False, timeout: int = 30) -> Any:
        if not self._page:
            raise ContextError("Evaluate JavaScript requires a page as a context")
        async with async_timeout.timeout(timeout):
            try:
                value = await self._page.evaluate(script, force_expr=force)
            except PageError:
                raise PageError
            except TimeoutError:
                raise TimeoutException("JavaScript took to long to execute")
            else:
                return value

    async def fill_form_element_by_id(self, element: str, value: str):
        script = "document.getElementById('{}').value='{}'".format(element, value)
        await self.evaluate_javascript(script)

    async def fill_form_element_by_css(self, element: str, value: str, element_number: int = 0):
        script = """
        var form_css_element = document.getElementsByClassName("{}");
        form_css_element[{}].value='{}';
        """.format(element, element_number, value)
        await self.evaluate_javascript(script)