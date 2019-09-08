import os
import sys

from moviepy.editor import VideoFileClip

from lib.data import VideoFileSegments

vfs = VideoFileSegments()

unseen = vfs.get_first_unseen()

if unseen is None:
    print("No more interesting pieces detected")
    sys.exit(0)

filename = os.path.join('videos/incoming', unseen['filename'])

if filename.endswith('.json'):
    filename = filename[:-5]

if not os.path.isfile(filename):
    print("File does not exist", filename)
    sys.exit(1)

clip = VideoFileClip(filename)

subclip = clip.without_audio().subclip(
    t_start=unseen['start'], t_end=unseen['end'])

subclip.write_videofile("output/video{}.mp4".format(unseen['index']))

vfs.set_status(unseen['index'], 'processing')
vfs.save()
