from terminaltables import AsciiTable
from lib.framework.commands import Help, Quit, Set, Show, Unset
from lib.framework.modules import Parameters
from lib.framework.utility import CommandParser

parameters = Parameters()
available_commands = {
    "help": Help(),
    "quit": Quit(),
    "set": Set(),
    "show": Show(),
    "unset": Unset(),
}


def start():
    output_header()
    parser = CommandParser()
    parser.run()


def output_header():
    print(""" __                __                                       __   
|  |--.---.-.----.|  |--.----.-----.-----.-----.-----.----.|  |_ 
|  _  |  _  |  __||    <|  __|  _  |     |     |  -__|  __||   _|
|_____|___._|____||__|__|____|_____|__|__|__|__|_____|____||____|

Welcome to the backconnect framework, type 'help' to see all commands.""")


def print_available_commands():
    data = [
        ['Command', 'Description']
    ]

    for command in available_commands.values():
        data.append([command.name, command.summary])

    print()
    print(AsciiTable(data).table)
    print("\nFor more information about a command, type {command}")
