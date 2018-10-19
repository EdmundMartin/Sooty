from sooty.sync import SyncSooty

s = SyncSooty(headless=False)
s.create_browser()
result = s.get_page('http://edmundmartin.com')
print(result)