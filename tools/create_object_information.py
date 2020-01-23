from lib.image import Detector
from lib.data import ObjectDataForVideo
from moviepy.editor import VideoFileClip
import argparse

import cv2
from tqdm import tqdm

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


parser = argparse.ArgumentParser(description='Detects objects in video')
parser.add_argument('--input', help='video stream')
parser.add_argument(
    '--threshold', help='threshold for object detection between 0 and 1', type=float, default=0.1)
parser.add_argument('--filter_threshold',
                    help='threshold for object detection (to be saved) between 0 and 1', type=float, default=None)
parser.add_argument(
    '--starttime', help='start time for video in seconds', type=float, default=0)
parser.add_argument(
    '--endtime', help='end time for video in seconds', type=float, default=None)
parser.add_argument(
    '--model', help='tensorflow hub model for object detection', type=str, default='mobile')
parser.add_argument(
    '--skipframes', help='number of frames to skip for processing', type=int, default=3)
parser.add_argument(
    '--nodisplay', help='flag for not displaying a window with the frame', dest='display', default=True, action='store_false')

args = parser.parse_args()

clip = VideoFileClip(args.input)
clip = clip.subclip(t_start=args.starttime, t_end=args.endtime)

print("Clip duration", clip.duration, "seconds")

module_handles = {
    'mobile': "https://tfhub.dev/google/openimages_v4/ssd/mobilenet_v2/1",
    "inception": "https://tfhub.dev/google/faster_rcnn/openimages_v4/inception_resnet_v2/1"
}

module_handle = module_handles[args.model]

detector = Detector(module_handle=module_handle, threshold=args.threshold)
object_data = ObjectDataForVideo(
    args.input + '.json', filter_threshold=args.filter_threshold)

for frame in tqdm(clip.iter_frames()):
    if len(object_data.data) % args.skipframes == 0:
        result = detector.detect(frame)
        object_data.append_raw_data(result)
        if args.display:
            frame = detector.add_boxes(cv2.cvtColor(
                frame, cv2.COLOR_BGR2RGB), result)
            cv2.imshow('image', frame)
            cv2.waitKey(1)
    else:
        object_data.append_none()

object_data.save()


cv2.destroyAllWindows()
