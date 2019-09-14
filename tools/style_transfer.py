from lib.image import StyleTransfer
from lib.data import ProcessingInformation
from lib.data import VideoFileSegments
import tensorflow as tf
import argparse
import os

from moviepy.editor import *
import cv2

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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


tf.enable_eager_execution()


parser = argparse.ArgumentParser(
    description='Applies style transfer to a video')
parser.add_argument('--input', help='input stream to style transfer to', default=None)
parser.add_argument('--style_image', help='url of image to get style from',
                    default='https://upload.wikimedia.org/wikipedia/commons/0/0a/The_Great_Wave_off_Kanagawa.jpg')
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


pi = ProcessingInformation()
pi.set_style_transfer_image(args.style_image)
pi.save()

st = StyleTransfer(style_image=args.style_image)
vid = VideoFileClip(video_filename)
vid2 = vid.fl_image(st.transform_frame)

if args.output:
    vid2.write_videofile(args.input)
else:
    tmp_file_name = '/tmp/tmp_video_style_transfer.mp4'
    vid2.write_videofile(tmp_file_name)

    os.rename(tmp_file_name, video_filename)
