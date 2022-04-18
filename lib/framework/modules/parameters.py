import lib.framework.utility.logger as logger
from terminaltables import AsciiTable
from lib.framework.core import Module
from lib.framework.exceptions import InvalidParameterException
from lib.framework.parameters import LHost, LPort, Payloads, PostData, Url


class Parameters(Module):
    name = "params"
    summary = "All currently set framework parameters."

    def __init__(self):
        self.params = {}
        self.available = {
            "lhost": LHost(),
            "lport": LPort(),
            "payloads": Payloads(),
            "postdata": PostData(),
            "url": Url(),
        }

    @staticmethod
    def validate_parameter(parameter, value):
        valid = parameter.validate(value)

        if not valid:
            raise InvalidParameterException(f"The value \"{value}\" is not valid for parameter \"{parameter.name}\"")

        if type(valid) is str:
            raise InvalidParameterException(valid)

    def set(self, key, value):
        key = key.lower()

        if key not in self.available:
            raise InvalidParameterException(f"Parameter \"{key}\" is not a valid parameter.")

        # value is passed as a list, convert to single if it is the only item
        if len(value) == 1:
            value = value[0]

            # Convert to int if needed
            if value.isdigit():
                value = int(value)

        parameter = self.available[key]

        # Validate the parameter value
        self.validate_parameter(parameter, value)

        # Check that the supplied value is of the correct parameter type
        if type(value) not in parameter.types:
            types = []

            for param_type in parameter.types:
                types.append(param_type.__name__)

            raise InvalidParameterException(f"The \"{key}\" parameter value must be of type: {', '.join(types)}")

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
                if type(value) is list:
                    value = ", ".join(value)

                data.append([key, value])

            print(AsciiTable(data).table)
