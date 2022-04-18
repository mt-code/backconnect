from terminaltables import AsciiTable

from lib.framework.core import Module
from lib.framework.payloads import *


class Payloads(Module):
    name = "payloads"
    summary = "All available backconnect payloads."

    def __init__(self):
        self.available_payloads = {
            "bash_tcp_1": bash_tcp_1(),
            "bash_tcp_2": bash_tcp_2(),
            "bash_tcp_3": bash_tcp_3(),
            "bash_udp_1": bash_udp_1(),
            "bash_udp_2": bash_udp_2(),
            "bash_udp_3": bash_udp_3(),
            "python_1": python_1(),
            "python_2": python_2(),
            "python_3": python_3(),
            "python_4": python_4(),
        }

    def show(self):
        data = [
            ["Payload", "Platform"]
        ]

        for payload in self.available_payloads.values():
            data.append([payload.name, ", ".join(payload.platform)])

        print(AsciiTable(data).table)

        print("\nTo view a payloads output, use the \"view {payload}\" command.")


