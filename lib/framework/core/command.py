from abc import ABCMeta, abstractmethod
from lib.framework.exceptions import CommandValidationException


class Command(metaclass=ABCMeta):

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def summary(self):
        pass

    @property
    @abstractmethod
    def description(self):
        pass

    @property
    @abstractmethod
    def args(self):
        return []

    @abstractmethod
    def execute(self, args):
        pass

    # Validate that the command should be executed.
    def validate(self, args):
        return len(self.args) == len(args)

    # Print the description/help output for this command
    # This can be overridden to provide more information if needed.
    def print_description(self):
        print(self.description)

    # Gets the expected format for a command to be expected.
    def example_format(self):
        example = self.name

        for arg in self.args:
            example += " {" + arg.upper() + "}"

        return example

    # Validates and executes the command.
    def run(self, args):
        if not self.validate(args):
            raise CommandValidationException(f"Expected format: {self.example_format()}")

        self.execute(args)
