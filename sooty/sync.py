import asyncio
from typing import List


from sooty.sooty import Sooty
from sooty.response import Response


class SyncSooty:

    def __init__(self, headless=True, proxy=None, auth=None):
        self.loop = asyncio.get_event_loop()
        self.__sooty = Sooty(headless=headless, proxy=None, auth=None)

    async def __handle_exception(self, func, *args, **kwargs):
        try:
            result = await func(*args, **kwargs)
        except Exception as e:
            raise e
        else:
            return result

    def create_browser(self) -> None:
        future = asyncio.Task(self.__handle_exception(self.__sooty._create_browser))
        self.loop.run_until_complete(future)
        return

    def create_page(self) -> None:
        future = asyncio.Task(self.__handle_exception(self.__sooty._create_page))
        self.loop.run_until_complete(future)
        return

    def get_request(self, url: str, timeout: int = 30, post_load_wait: int = 0) -> Response:
        fake_kwargs = {'timeout': timeout, 'post_load_wait': post_load_wait}
        future = asyncio.Task(self.__handle_exception(self.__sooty.get_request, url, **fake_kwargs))
        self.loop.run_until_complete(future)
        return future.result()

    def get_element(self, selector: str, method: str = 'outerHTML') -> str:
        fake_kwargs = {'method': method}
        future = asyncio.Task(self.__handle_exception(self.__sooty.get_element, selector, **fake_kwargs))
        self.loop.run_until_complete(future)
        return future.result()

    def get_elements(self, selector: str, method: str = 'outerHTML') -> List[str]:
        fake_kwargs = {'method': method}
        future = asyncio.Task(self.__handle_exception(self.__sooty.get_elements, selector, **fake_kwargs))
        self.loop.run_until_complete(future)
        return future.result()

    def close_browser(self) -> None:
        future = asyncio.Task(self.__handle_exception(self.__sooty.close_browser))
        self.loop.run_until_complete(future)
        return future.result()


if __name__ == '__main__':
    sooty = SyncSooty(headless=False)
    sooty.create_browser()
    sooty.create_page()
