import argparse
import os

import numpy as np
from tqdm import tqdm
import cv2

from moviepy.editor import VideoFileClip

from lib.object_data import ObjectData

def extract_box_from_frame(frame, box):
    height, width, _ = frame.shape
    x1 = int(box[1] * width)
    y1 = int(box[0] * height)
    x2 = int(box[3] * width)
    y2 = int(box[2] * height)

    return frame[y1:y2,x1:x2, :]

parser = argparse.ArgumentParser(description='Extracts traffic signs')
parser.add_argument('--input', help='video stream')
parser.add_argument('--output', help='output folder', default='output/traffic_signs')

args = parser.parse_args()

clip = VideoFileClip(args.input)
object_data = ObjectData()
object_data.load(args.input + '.json')

instances = object_data.get_instances_key_appears('Traffic sign')

idx = 0
signs = []


for i, data in tqdm(enumerate(instances)):
    frame = clip.get_frame(float(data['time']) / clip.fps)
    for box in data['boxes']:
        sign = extract_box_from_frame(frame, box)
        cv2.imwrite(os.path.join(args.output, "sign{:05d}.jpg".format(i)), cv2.cvtColor(sign, cv2.COLOR_RGB2BGR))
