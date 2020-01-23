import sys

from lib.data import VideoFileSegments
from lib.data import VideoFile


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
