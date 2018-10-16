from sooty import SootyRender
import asyncio

if __name__ == '__main__':
    async def run():
        s = await SootyRender.create_renderer(headless=False)
        result = await s.get_request('http://edmundmartin.com')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())