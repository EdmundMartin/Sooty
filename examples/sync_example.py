from sooty.sync import SyncSooty

s = SyncSooty(headless=False)
s.create_browser()
result = s.get_request('http://edmundmartin.com')
print(result)