from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from lib.commands import commands

cmd_completer = WordCompleter(commands.keys())

while True:
    cmd = prompt(">>> ", completer=cmd_completer)

    if cmd in commands:
        commands[cmd]['func']()
    else:
        print("Unknown command")
