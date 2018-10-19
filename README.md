# Sooty
Sooty is an ease of use wrapper around the Pyppeteer library, with the goal of making the library easier to use. The 
library can also be used both synchronously and asynchronously.

## Sooty
```python
import asyncio

from sooty import Sooty


async def main():
    browser = await Sooty.create_sooty(headless=False)
    resp = await browser.get_request('http://edmundmartin.com')
    print(resp)
    h1 = await browser.get_element('h1')
    print(h1)
    resp = await browser.get_request('http://edmundmartin.com/wp-login.php')
    await browser.fill_form_element_by_css('input', 'NotMyUserName', 0)
    await asyncio.sleep(30)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
```
Example usage of the standard async wrapper

## Sooty Render
```python
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
```
Sooty Render is specifically designed when you wish to render a large number of pages asynchronously.

## Sooty Sync
```python
from sooty.sync import SyncSooty

s = SyncSooty(headless=False)
s.create_browser()
result = s.get_page('http://edmundmartin.com')
print(result)
```
Provides a way to synchronously interact with the browser, maintaining the same underlying implementation.