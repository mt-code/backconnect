import lib.framework.framework as framework
from lib.framework.core import Command


class Connect(Command):

    name = "connect"
    summary = "Performs the backconnect after the required parameters are set."
    args = []
    description = """
Performs the backconnect after the required parameters are set.

For a list of parameters, type "help set". """

    def __init__(self):
        # TODO: Instantiate the modules in the framework.py file
        self.modules = {
            "params": framework.parameters,
            "payloads": framework.payloads,
        }

    def validate(self, args):
        required = [
            "lhost",
            "lport",
            "url"
        ]

        for param in required:
            if param not in framework.parameters.params:
                return f"The '{param}' parameter must be set."

        return True

    def execute(self, args):
        print("connect execute")

