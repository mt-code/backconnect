import requests
from requests.utils import requote_uri


class PayloadRequest:
    def __init__(self, url, payload):
        self.url = url
        self.payload = payload

    def get_payload_url(self):
        return self.url.replace("INJECT", self.payload.get_payload())

    def make(self):
        url = requote_uri(self.get_payload_url())
        requests.get(url, timeout=5)
