import pandas as pd
import sys
import os

from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prettytable import PrettyTable

from lib.data import VideoFileSegments
from lib.youtube import YouTube

from .video import commands as video_commands


def list_videos():
    vfs = VideoFileSegments()

    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(vfs.data)


def config():
    completer = WordCompleter(['youtube'])

    option = prompt('Configure >>> ', completer=completer)
    if option == 'youtube':
        youtube = YouTube()
        youtube.init()
        result = youtube.video_categories()

        if len(result['items']) > 1:
            print("Sample request succesful; all seems to be working.")


def exit():
    sys.exit(0)


def help_text():
    table = PrettyTable()
    table.field_names = ['command', 'description']
    keys = sorted(list(commands.keys()))
    for key in keys:
        table.add_row([key, commands[key]['help']])

    print(table)


def download():
    os.system("./tools/download.sh")


commands = {
    **video_commands,
    'exit': {'func': exit, 'help': 'exists the program'},
    'help': {'func': help_text, 'help': 'displays this help'},
    'list': {'func': list_videos, 'help': 'displays a list of available video segments'},
    'config': {'func': config, 'help': 'runs configuration commands'},
    'download': {'func': download, 'help': 'downloads videos form sd card'},
}
