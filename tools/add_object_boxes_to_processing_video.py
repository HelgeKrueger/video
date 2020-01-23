from lib.image import Detector
from lib.data import ProcessingInformation
from lib.data import VideoFileSegments
import argparse
import os
import json
import sys

from moviepy.editor import VideoFileClip

import logging

# get TF logger
log = logging.getLogger('tensorflow')
log.setLevel(logging.DEBUG)

# create formatter and add it to the handlers
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# create file handler which logs even debug messages
fh = logging.FileHandler('tensorflow.log')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
log.addHandler(fh)

parser = argparse.ArgumentParser(
    description='Adds boxes from object detection to images')
parser.add_argument(
    '--input', help='input stream to style transfer to, default use processing video', default=None)
parser.add_argument('--output', help='output mp4 file',
                    default=None)

args = parser.parse_args()

if args.input:
    video_filename = args.input

else:
    vfs = VideoFileSegments()

    if vfs.count_with_status('processing') != 1:
        print("Need to process exactly one video")
        sys.exit(1)

    processing = vfs.get_first_with_status('processing')
    video_filename = processing['video_file']
    start_time = processing['start']
    data_filename = processing['filename']


pi = ProcessingInformation()
pi.save()

detector = Detector(
    module_handle="https://tfhub.dev/google/openimages_v4/ssd/mobilenet_v2/1", threshold=0.2)

vid = VideoFileClip(video_filename)
fps = vid.fps

object_data = json.load(
    open(os.path.join('videos/incoming', data_filename), 'r'))


def transform(get_frame, time):
    frame = get_frame(time)

    idx = int(time * fps + start_time)
    result = object_data[idx]

    if result is None:
        result = detector.detect(frame)

    return detector.add_boxes(frame, result)


vid2 = vid.fl(transform)


if args.output:
    vid2.write_videofile(args.output)
else:
    tmp_file_name = '/tmp/tmp_video_style_transfer.mp4'
    vid2.write_videofile(tmp_file_name)

    os.rename(tmp_file_name, video_filename)
