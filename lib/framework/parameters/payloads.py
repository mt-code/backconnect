from lib.framework import framework
from lib.framework.core import Parameter


class Payloads(Parameter):
    name = "payloads"
    description = "The payloads to use, if this is not set all payloads will be tried."
    types = [str, list]

    def validate(self, payloads):
        if type(payloads) is list:
            for payload in payloads:
                if payload not in framework.payloads.available_payloads:
                    return f"\"{payload}\" is not a valid payload name."
        elif type(payloads) is str:
            if payloads not in framework.payloads.available_payloads:
                return f"\"{payloads}\" is not a valid payload name."
        else:
            return False

        return True



