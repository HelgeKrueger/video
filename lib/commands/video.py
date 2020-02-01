import os
import sys

from prompt_toolkit import prompt
from prompt_toolkit.validation import Validator

from moviepy.editor import VideoFileClip

from lib.data import VideoFile
from lib.data import VideoFileSegments
from lib.data import ProcessingInformation
from lib.youtube import YouTube


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


def upload_video():
    vfs = VideoFileSegments()
    pi = ProcessingInformation()

    if vfs.count_with_status('processing') != 1:
        print("Need to process exactly one video")
        sys.exit(1)

    processing = vfs.get_first_with_status('processing')
    video_filename = processing['video_file']

    print("Uploading video to YouTube")
    print("")

    title = prompt("Title >>> ")

    print("Uploading video", video_filename, "with title", title)

    youtube = YouTube()
    youtube.init()

    description = pi.get_description()

    youtube.upload_file(video_filename, title, description)

    vfs.update_status_from_to('processing', 'youtube')
    vfs.save()
    pi.done()


def cut_start():
    vfs = VideoFileSegments()

    if vfs.count_with_status('processing') != 1:
        print("Need to process exactly one video")
        sys.exit(1)

    validator = Validator.from_callable(
        lambda text: text.isdigit(),
        error_message='This input contains non-numeric characters',
        move_cursor_to_end=True)

    time_to_cut = prompt("Seconds to remove from start >>> ", validator=validator)
    time_to_cut = int(time_to_cut)

    processing = vfs.get_first_with_status('processing')
    video_filename = processing['video_file']

    clip = VideoFileClip(video_filename)
    subclip = clip.without_audio().subclip(t_start=time_to_cut)

    subclip.write_videofile('/tmp/video.mp4')
    os.rename('/tmp/video.mp4', video_filename)


def cut_end():
    vfs = VideoFileSegments()

    if vfs.count_with_status('processing') != 1:
        print("Need to process exactly one video")
        sys.exit(1)

    validator = Validator.from_callable(
        lambda text: text.isdigit(),
        error_message='This input contains non-numeric characters',
        move_cursor_to_end=True)

    time_to_cut = prompt("Seconds to remove from end >>> ", validator=validator)
    time_to_cut = int(time_to_cut)

    processing = vfs.get_first_with_status('processing')
    video_filename = processing['video_file']

    clip = VideoFileClip(video_filename)
    subclip = clip.without_audio().subclip(t_end=clip.duration - time_to_cut)

    subclip.write_videofile('/tmp/video.mp4')
    os.rename('/tmp/video.mp4', video_filename)


commands = {
    'next': {'func': next_video, 'help': 'extracts the next video piece labeled as unseen'},
    'watch': {'func': watch_video, 'help': 'watch current video'},
    'upload': {'func': upload_video, 'help': 'upload current video'},
    'cut_start': {'func': cut_start, 'help': 'removes piece from start of video'},
    'cut_end': {'func': cut_end, 'help': 'removes piece from end of video'}
}
