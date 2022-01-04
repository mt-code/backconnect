import lib.framework.framework as framework
import lib.framework.utility.logger as logger
from lib.framework.core import Command
from terminaltables import AsciiTable


class Set(Command):

    name = "set"
    summary = "Sets a framework parameter."
    args = ["param", "value"]
    description = """
Sets a framework parameter.

"set {param} {value}"
"""

    def validate(self, args):
        return len(args) >= 2

    def execute(self, args):
        key = args.pop(0).lower()
        framework.parameters.set(key, args)
        logger.success(f"{key} => {', '.join(args)}")

    def print_description(self):
        print(self.description)

        data = [
            ['Parameter', 'Description'],
        ]

        for param in framework.parameters.available.values():
            data.append([param.name, param.description])

        print(AsciiTable(data).table)
