import sys
import lib.framework.framework as framework
from lib.framework.core import Command


class Quit(Command):

    name = "quit"
    summary = "Quits the application."
    args = []
    description = """
Quits the application."""

    def validate(self, args):
        return len(self.args) == len(args)

    def execute(self, args):
        sys.exit(0)
