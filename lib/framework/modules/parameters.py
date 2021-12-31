import lib.framework.utility.logger as logger
from terminaltables import AsciiTable
from lib.framework.core import Module


class Parameters(Module):
    name = "params"
    summary = "All currently set framework parameters."

    def __init__(self):
        self.params = {}

    def set(self, key, value):
        self.params[key] = value

    def unset(self, key):
        if key not in self.params:
            logger.error(f"Parameter \"{key}\" does not exist.")
        else:
            del self.params[key]
            logger.success(f"Parameter \"{key}\" was unset.")

    def show(self):
        if len(self.params) <= 0:
            logger.log("There are no parameters currently set.")
        else:
            data = [
                ["Parameter", "Value"]
            ]

            for key, value in self.params.items():
                data.append([key, value])

            print(AsciiTable(data).table)
