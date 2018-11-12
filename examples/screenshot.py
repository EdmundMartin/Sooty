import asyncio

from sooty import Sooty


async def main():
    browser = await Sooty.create_sooty(headless=False)
    await browser.take_screenshot('http://edmundmartin.com', 'myshot.jpg')
    await browser.close_browser()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()