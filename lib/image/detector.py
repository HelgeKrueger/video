import numpy as np
import cv2

from PIL import ImageColor

import tensorflow as tf
import tensorflow_hub as hub


class Detector:
    def __init__(self, module_handle="https://tfhub.dev/google/faster_rcnn/openimages_v4/inception_resnet_v2/1", threshold=0.1):
        self.module = hub.load(module_handle).signatures['default']
        self.threshold = threshold

        self.colormap = list(ImageColor.colormap.keys())
        self.number_of_colors = len(self.colormap)

    def detect(self, frame):
        input_frame = np.array(np.expand_dims(frame, 0)/256)
        input_frame = tf.convert_to_tensor(input_frame, dtype=tf.float32)
        return self.module(input_frame)

    def add_boxes(self, frame, result):
        frame = frame.copy()
        height, width, _ = frame.shape

        if 'boxes' in result:
            boxes = result['boxes']
            entities = result['entities']
        else:
            good_frames = result['detection_scores'] > self.threshold
            entities = [b.numpy().decode('ascii')
                        for b in result['detection_class_entities'][good_frames]]
            boxes = result['detection_boxes'][good_frames]

        for raw_box, entity in zip(boxes, entities):
            box = self.convert_box(raw_box, width, height)
            self.add_box_to_frame(frame, box, entity)

        return frame

    def convert_box(self, box, width, height):
        y1, x1, y2, x2 = box
        return (int(x1 * width), int(y1 * height)), (int(x2 * width), int(y2 * height))

    def add_box_to_frame(self, frame, box, title):
        c1, c2 = box
        font = cv2.FONT_HERSHEY_SIMPLEX
        color = self.determine_color(title)
        cv2.putText(
            frame, title, (c1[0] + 20, c1[1] + 100), font, 1, color, 3, cv2.LINE_AA)
        cv2.rectangle(frame, c1, c2, color, 3)

    def determine_color(self, title):
        color_name = self.colormap[hash(title) % self.number_of_colors]
        return ImageColor.getrgb(color_name)
