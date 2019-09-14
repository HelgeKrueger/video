from lib.data import VideoFileSegments
from lib.data import ProcessingInformation
import argparse

from lib.youtube import YouTube

parser = argparse.ArgumentParser(description='Uploads video to youtube')
parser.add_argument('title', help='video to upload')
parser.add_argument('--description', help='description of video', default=None)

args = parser.parse_args()


vfs = VideoFileSegments()
pi = ProcessingInformation()

if vfs.count_with_status('processing') != 1:
    print("Need to process exactly one video")
    sys.exit(1)

processing = vfs.get_first_with_status('processing')
video_filename = processing['video_file']

print("Uploading video", video_filename, "with title", args.title)

youtube = YouTube()
youtube.init()

if args.description:
    description = args.description + \
        "\n\nCode for processing video available at https://github.com/HelgeKrueger/video"
else:
    description = pi.get_description()

youtube.upload_file(video_filename, args.title, description)

vfs.update_status_from_to('processing', 'youtube')
vfs.save()
pi.done()
