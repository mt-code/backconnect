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

[*] If a parameter is marked as required, that parameter must be set.
[*] If a parameter is marked as injectable, that parameter can contain the 'INJECT' placeholder.
"""

    def validate(self, args):
        return len(args) >= 2

    def execute(self, args):
        key = args.pop(0)
        framework.parameters.set(key, args)
        logger.success(f"{key} => {', '.join(args)}")

    def print_description(self):
        print(self.description)

        data = [
            ['Parameter', 'Description', 'Required?', 'Injectable?'],
        ]

        for param in framework.parameters.available.values():
            data.append([
                param.name,
                param.description,
                'YES' if param.required else '-',
                'YES' if param.injectable else '-',
            ])

        print(AsciiTable(data).table)
