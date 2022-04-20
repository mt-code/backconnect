import sys
from enum import Enum
from string import whitespace
import lib.framework.framework as framework
import lib.framework.utility.logger as logger
from lib.framework.exceptions import FrameworkException


class State(Enum):
    SPACE = 0
    WORD = 1
    QUOTE = 2


class CommandParser:

    def run(self):
        while True:
            try:
                user_input = input("\n[>] ")
                commands = self.parse(user_input)
                print(commands)
                self.process(commands)
            except KeyboardInterrupt:
                sys.exit(0)

    @staticmethod
    def parse(user_input):
        words = []
        word = []
        state = State.SPACE
        quote = ''
        quotes = '\'"'
        allow_blank = False

        text_ = iter(user_input)
        for char in text_:
            if state is State.SPACE:
                if char in whitespace:
                    continue
                state = State.WORD

            if state is State.WORD:
                if char in whitespace:
                    state = State.SPACE
                    if allow_blank or word:
                        words.append(''.join(word).strip("'").strip('"'))
                    word = []
                    allow_blank = False
                    continue
                if char in quotes:
                    quote = char
                    allow_blank = True
                    state = State.QUOTE
            elif state is State.QUOTE:
                if char == quote:
                    state = State.WORD

            if char == '\\' and ((state is State.WORD) or (state is State.QUOTE and quote != '\'')):
                new_char = next(text_, StopIteration)
                if new_char is StopIteration:
                    break
                word.append(char)
                char = new_char

            word.append(char)

        if state is State.WORD or state is State.QUOTE:
            if allow_blank or word:
                words.append(''.join(word).strip("'").strip('"'))

        return words

    @staticmethod
    def process(commands):
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


