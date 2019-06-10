import argparse

from lib.youtube import YouTube

parser = argparse.ArgumentParser(description='Uploads video to youtube')
parser.add_argument('--input', help='video to upload',
                    default='output/tmp.mp4')
parser.add_argument('--title', help='title of video')
parser.add_argument('--description', help='description of video')

args = parser.parse_args()

youtube = YouTube()
youtube.init()

youtube.upload_file(args.input, args.title, args.description)
