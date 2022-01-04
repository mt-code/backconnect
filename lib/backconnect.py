import requests
import lib.framework.utility.logger as logger
from threading import Lock


class Backconnect:
    thread_lock = Lock()

    def __init__(self, url, listen_hort, listen_port):
        self.url = url
        self.listen_host = listen_hort
        self.listen_port = listen_port
        self.payloads = {}

    @staticmethod
    def send_payload(data):
        payload_name = data[0]
        payload_url = data[1]

        with Backconnect.thread_lock:
            logger.success(f"Sending payload: {payload_name}")

        try:
            requests.get(payload_url, timeout=5)
        except TimeoutError:
            logger.error("Timeout, this should be success?")
        except:
            logger.error("Another error occurred")

    def set_payloads(self, payloads):
        pass

