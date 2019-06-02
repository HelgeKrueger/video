import argparse

import cv2
import numpy as np

import tensorflow as tf
import tensorflow_hub as hub

from moviepy.editor import VideoFileClip

from detector import Detector

parser = argparse.ArgumentParser(description='Detects objects in video')
parser.add_argument('--input', help='video stream')
parser.add_argument('--threshold', help='threshold for object detection between 0 and 1', type=float, default=0.1)
parser.add_argument('--starttime', help='start time for video in seconds', type=float, default=0)

args = parser.parse_args()

clip = VideoFileClip(args.input)

print("Clip duration", clip.duration, "seconds")


module_handle = "https://tfhub.dev/google/faster_rcnn/openimages_v4/inception_resnet_v2/1"
# module_handle = "https://tfhub.dev/google/openimages_v4/ssd/mobilenet_v2/1"
detector = Detector(module_handle=module_handle, threshold=args.threshold)

for t in range(args.starttime, int(clip.duration), 1):
    print("time", t)
    frame = clip.get_frame(t)
    result = detector.detect(frame)
    frame = detector.add_boxes(cv2.cvtColor(clip.get_frame(t), cv2.COLOR_BGR2RGB), result)
    cv2.imshow('image', frame)
    cv2.waitKey(1)

cv2.destroyAllWindows()
