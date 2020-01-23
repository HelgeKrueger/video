import os
import sys
import pandas as pd

from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

from lib.data import VideoFile
from lib.data import VideoFileSegments
from lib.data import ProcessingInformation
from lib.youtube import YouTube


def list_videos():
    vfs = VideoFileSegments()

    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(vfs.data)


def next_video():
    vfs = VideoFileSegments()

    if vfs.count_with_status('processing') > 0:
        print("Already procesising a video")
        sys.exit(1)

    unseen = vfs.get_first_unseen()

    if unseen is None:
        print("No more interesting pieces detected")
        sys.exit(1)

    video_file = VideoFile(unseen)
    video_filename = "output/video{}.mp4".format(unseen['index'])
    video_file.save_as(video_filename)

    vfs.set_status(unseen['index'], 'processing')
    vfs.set_video_filename(unseen['index'], video_filename)
    vfs.save()


def watch_video():
    vfs = VideoFileSegments()

    if vfs.count_with_status('processing') != 1:
        print("Need to process exactly one video")
        sys.exit(1)

    processing = vfs.get_first_with_status('processing')

    os.system("xdg-open {}".format(processing['video_file']))


def config():
    completer = WordCompleter(['youtube'])

    option = prompt('Configure >>> ', completer=completer)
    if option == 'youtube':
        youtube = YouTube()
        youtube.init()
        result = youtube.video_categories()

        if len(result['items']) > 1:
            print("Sample request succesful; all seems to be working.")


def upload_video():
    vfs = VideoFileSegments()
    pi = ProcessingInformation()

    if vfs.count_with_status('processing') != 1:
        print("Need to process exactly one video")
        sys.exit(1)

    processing = vfs.get_first_with_status('processing')
    video_filename = processing['video_file']

    title = prompt("Title >>> ")

    print("Uploading video", video_filename, "with title", title)

    youtube = YouTube()
    youtube.init()

    description = pi.get_description()

    youtube.upload_file(video_filename, title, description)

    vfs.update_status_from_to('processing', 'youtube')
    vfs.save()
    pi.done()
