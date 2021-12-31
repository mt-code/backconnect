import lib.framework.framework as framework
from lib.framework.core import Command


class Help(Command):

    name = "help"
    summary = "Shows all available commands."
    args = ["command"]
    description = """
Shows detailed help information about a specified command.

help {command}"""

    def validate(self, args):
        return len(self.args) == len(args)

    def execute(self, args):
        command = args[0]

        if command in framework.available_commands:
            framework.available_commands[command].print_description()
