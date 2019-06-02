import numpy as np
import cv2

import tensorflow as tf
import tensorflow_hub as hub

class Detector:
    def __init__(self, module_handle="https://tfhub.dev/google/faster_rcnn/openimages_v4/inception_resnet_v2/1", threshold=0.1):
        self.session = tf.Session()
        self.module = hub.Module(module_handle)
        input_image = tf.placeholder(tf.float32)
        self.result = self.module(input_image, as_dict=True)
        self.threshold = threshold

        self.session.run([
            tf.global_variables_initializer(), tf.tables_initializer()
                ])

    def detect(self, frame):
        input_frame = np.array(np.expand_dims(frame, 0)/256)

        return self.session.run(self.result, feed_dict={
            'Placeholder:0': input_frame})

    def add_boxes(self, frame, result):
        frame = frame.copy()
        height, width, _ = frame.shape

        good_frames = result['detection_scores'] >  self.threshold
        entities = [b.decode('ascii') for b in result['detection_class_entities'][good_frames]]
        boxes = result['detection_boxes'][good_frames]
        print("entities", entities, "boxes", boxes)

        count = len(entities)

        for j in range(count):
            box = self.convert_box(boxes[j], width, height)
            self.add_box_to_frame(frame, box, entities[j], (0, 255, 0))

        return frame

    def convert_box(self, box, width, height):
        y1, x1, y2, x2 = box
        return (int(x1 * width), int(y1 * height)), (int(x2 * width), int(y2 * height))

    def add_box_to_frame(self, frame, box, title, color):
        c1, c2 = box
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame,title,(c1[0] + 20, c1[1] + 100), font, 1, color,3,cv2.LINE_AA)
        cv2.rectangle(frame, c1, c2, color, 3)


