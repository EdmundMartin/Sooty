from sooty.exceptions import RequestException


class Response:

    __slots__ = ['url', 'requested_url', 'html', 'status', 'headers']

    def __init__(self, requested_url: str, url: str, html: str, status_code: int, headers: dict):
        self.url = url
        self.requested_url = requested_url
        self.html = html
        self.status = status_code
        self.headers = headers

    @property
    def status_ok(self) -> bool:
        return self.status < 300

    @property
    def is_redirect(self) -> bool:
        return self.requested_url != self.url

    def raise_for_status(self) -> None:
        if self.status >= 400:
            raise RequestException("Did not receive a 2XX Code")

    def __repr__(self):
        return 'Response(url={}, status_code={})'.format(self.url, self.status)
