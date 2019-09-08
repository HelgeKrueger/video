import argparse

from lib.data import VideoFileSegments

parser = argparse.ArgumentParser(description='Sets the status of all processing videos')
parser.add_argument('--status', help='new status',
                    default='done')

args = parser.parse_args()

vfs = VideoFileSegments()

vfs.update_status_from_to('processing', args.status)

vfs.save()
