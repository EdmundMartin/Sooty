from sooty import SootyRender
import asyncio


async def render_many(browser: SootyRender, url):
    result = await browser.get_request(url)
    print(result)


if __name__ == '__main__':
    q = asyncio.Queue()
    urls = ['http://google.com', 'http://github.com', 'http://edmundmartin.com']
    loop = asyncio.get_event_loop()
    browser = SootyRender(headless=False)
    tasks = asyncio.gather(*[render_many(browser, url) for url in urls])
    loop.run_until_complete(tasks)
    loop.run_until_complete(browser.close())
    loop.close()