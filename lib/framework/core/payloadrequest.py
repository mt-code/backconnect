import requests
from requests.utils import requote_uri
from urllib import parse


class PayloadRequest:
    def __init__(self, url, payload):
        self.url = url
        self.payload = payload
        self.postdata = None
        self.headers = {}

    def inject_payload(self, string):
        return string.replace("INJECT", self.payload.get_payload())

    # Converts the post data query string into a dictionary and injects any payloads
    def set_postdata(self, postdata):
        self.postdata = {}
        postdata = parse.parse_qs(postdata)

        for key, values in postdata.items():
            postdata_values = []

            # values is a list type even if there is only 1 item as multiple keys
            # could be provided in the query string
            for value in values:
                postdata_values.append(self.inject_payload(value))

            self.postdata[key] = postdata_values

    def set_headers(self, headers):
        for header in headers:
            header = header.split(":", 1)
            key, value = header[0], header[1]
            self.headers[key.strip(" ")] = value.strip(" ")

    def make(self):
        url = requote_uri(self.inject_payload(self.url))

        if self.postdata:
            requests.post(url, timeout=5, data=self.postdata, headers=self.headers)
        else:
            requests.get(url, timeout=5, headers=self.headers)
