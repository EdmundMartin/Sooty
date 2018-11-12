import asyncio

from sooty.sooty import Sooty


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

    def get_page(self, *args, **kwargs):
        future = asyncio.Task(self.__handle_exception(self.__sooty.get_request, *args, **kwargs))
        self.loop.run_until_complete(future)
        return future.result()

    def get_element(self, *args, **kwargs):
        future = asyncio.Task(self.__handle_exception(self.__sooty.get_element, *args, **kwargs))
        self.loop.run_until_complete(future)
        return future.result()

    def get_elements(self, *args, **kwargs):
        future = asyncio.Task(self.__handle_exception(self.__sooty.get_elements, *args, **kwargs))
        self.loop.run_until_complete(future)
        return future.result()

if __name__ == '__main__':
    sooty = SyncSooty(headless=False)
    sooty.create_browser()
    sooty.create_page()
