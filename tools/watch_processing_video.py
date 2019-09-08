import os
import sys

from lib.data import VideoFileSegments

vfs = VideoFileSegments()

if vfs.count_with_status('processing') != 1:
    print("Need to process exactly one video")
    sys.exit(1)

processing = vfs.get_first_with_status('processing')

os.system("xdg-open {}".format(processing['video_file']))
