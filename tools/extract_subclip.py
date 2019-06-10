import argparse

from moviepy.editor import VideoFileClip

parser = argparse.ArgumentParser(description='Extracts subclip from video')
parser.add_argument('--input', help='video stream')
parser.add_argument('--output', help='output video file', default='output/tmp.mp4')
parser.add_argument('--start', help='start time in seconds',  type=float)
parser.add_argument('--end', help='end time in seconds',  type=float)
parser.add_argument('--length', help='length of clip',  type=float, default=60)

args = parser.parse_args()
clip = VideoFileClip(args.input)

start_time = args.start
end_time = args.end

if end_time is None:
    end_time = start_time + args.length - 1

subclip = clip.without_audio().subclip(t_start=start_time, t_end=end_time)
subclip.write_videofile(args.output)
