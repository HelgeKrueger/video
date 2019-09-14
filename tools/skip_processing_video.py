from lib.data import VideoFileSegments
import argparse

parser = argparse.ArgumentParser(description='skips current video')
args = parser.parse_args()


vfs = VideoFileSegments()

if vfs.count_with_status('processing') != 1:
    print("Need to process exactly one video")
    sys.exit(1)

processing = vfs.get_first_with_status('processing')

print("Skipping video", processing['video_file'])

vfs.update_status_from_to('processing', 'skipped')
vfs.save()
