import lib.framework.framework as framework
from lib.framework.core import Command


class Unset(Command):

    name = "unset"
    summary = "Unsets a framework parameter."
    args = ["param"]
    description = """
Unsets a framework parameter.

"unset {param}" """

    def execute(self, args):
        framework.parameters.unset(args[0])
