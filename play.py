import asyncio

from sooty.sooty import Sooty


async def main():
    browser = await Sooty.create_sooty(headless=False)
    resp = await browser.get_request('http://edmundmartin.com')
    print(resp)
    h1 = await browser.get_element('h1')
    print(h1)
    resp = await browser.get_request('http://edmundmartin.com/wp-login.php?redirect_to=http%3A%2F%2Fedmundmartin.com%2Fwp-admin%2F&reauth=1')
    await browser.fill_form_element_by_css('input', 'eddie', 0)
    await asyncio.sleep(30)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())