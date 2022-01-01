import base64
import lib.framework.framework as framework
from abc import ABCMeta, abstractmethod


class Payload(metaclass=ABCMeta):

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def platform(self):
        pass

    @property
    @abstractmethod
    def payload(self):
        # base64 encoded to prevent issues with quotation marks
        pass

    def get_payload(self):
        payload = base64.b64decode(self.payload).decode("utf-8")

        if "lhost" in framework.parameters.params:
            payload = payload.replace("{LHOST}", framework.parameters.params["lhost"])

        if "lport" in framework.parameters.params:
            payload = payload.replace("{LPORT}", framework.parameters.params["lport"])

        return payload
