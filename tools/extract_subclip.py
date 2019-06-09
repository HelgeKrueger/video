import argparse

from moviepy.editor import VideoFileClip

parser = argparse.ArgumentParser(description='Extracts subclip from video')
parser.add_argument('--input', help='video stream')
parser.add_argument('--output', help='output video file', default='output/tmp.mp4')
parser.add_argument('--start', help='start time in seconds',  type=float)
parser.add_argument('--end', help='end time in seconds',  type=float)

args = parser.parse_args()
clip = VideoFileClip(args.input)

subclip = clip.without_audio().subclip(t_start=args.start, t_end=args.end)
subclip.write_videofile(args.output)
