import validators


class Utils:

    def __init__(self):
        pass

    def sanitize_url(self, url: str) -> str:
        if validators.url(url):
            return url
        else:
            return None
