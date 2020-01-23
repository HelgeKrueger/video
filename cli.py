from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prettytable import PrettyTable

from lib.commands import list_videos, next_video, watch_video, config, upload_video

import sys


def exit():
    sys.exit(0)


def help_text():
    table = PrettyTable()
    table.field_names = ['command', 'description']
    keys = sorted(list(commands.keys()))
    for key in keys:
        table.add_row([key, commands[key]['help']])

    print(table)


commands = {
    'exit': {'func': exit, 'help': 'exists the program'},
    'help': {'func': help_text, 'help': 'displays this help'},
    'list': {'func': list_videos, 'help': 'displays a list of available video segments'},
    'next': {'func': next_video, 'help': 'extracts the next video piece labeled as unseen'},
    'watch': {'func': watch_video, 'help': 'watch current video'},
    'upload': {'func': upload_video, 'help': 'upload current video'},
    'config': {'func': config, 'help': 'runs configuration commands'}
}

cmd_completer = WordCompleter(commands.keys())

while True:
    cmd = prompt(">>> ", completer=cmd_completer)

    if cmd in commands:
        commands[cmd]['func']()
    else:
        print("Unknown command")
