import pandas as pd

from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

from lib.data import VideoFileSegments
from lib.youtube import YouTube

from .video import next_video, watch_video, upload_video


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
