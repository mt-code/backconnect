import sys
import lib.framework.framework as framework
import lib.framework.utility.logger as logger
from lib.framework.exceptions import FrameworkException


class CommandParser:

    def run(self):
        user_input = ""

        while user_input != "quit" and user_input != "q":
            try:
                user_input = input("\n[>] ")
                self.parse(user_input.split())
            except KeyboardInterrupt:
                sys.exit(0)

    @staticmethod
    def parse(commands):
        try:
            if len(commands) >= 1:
                command = commands.pop(0).lower()

                if command in framework.available_commands:
                    if command == "help" and len(commands) == 0:
                        framework.print_available_commands()
                    else:
                        framework.available_commands[command].run(commands)

        except FrameworkException as e:
            logger.error(e)


