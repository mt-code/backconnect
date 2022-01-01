import lib.framework.framework as framework
from lib.framework.core import Command
from lib.framework.exceptions import InvalidParameterException
from terminaltables import AsciiTable


class Show(Command):

    name = "show"
    summary = "Show module related information."
    args = ["module"]
    description = """
Show information relating to the specified module.

"show {module}"
"""

    def __init__(self):
        # TODO: Instantiate the modules in the framework.py file
        self.modules = {
            "params": framework.parameters,
            "payloads": framework.payloads,
        }

    def execute(self, args):
        module = args[0]

        if module in self.modules:
            self.modules[module].show()
        else:
            raise InvalidParameterException(f"The {self.name} command does not accept \"{module}\" as a parameter, type \"help show\" for a list of valid parameters.")

    def print_description(self):
        print(self.description)

        data = [
            ['Module', 'Description']
        ]

        for module in self.modules.values():
            data.append([module.name, module.summary])

        print(AsciiTable(data).table)
