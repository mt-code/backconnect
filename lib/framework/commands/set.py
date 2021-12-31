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

    def execute(self, args):
        framework.parameters.set(args[0], args[1])
        logger.success(f"{args[0]} => {args[1]}")

    def print_description(self):
        print(self.description)

        data = [
            ['Parameter', 'Description'],
            ['lhost', 'The listen host'],
            ['lport', 'The listen port'],
            ['url', 'The target URL, this can include the INJECT placeholder']
        ]

        print(AsciiTable(data).table)
