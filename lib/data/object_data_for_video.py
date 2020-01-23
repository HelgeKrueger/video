import json
import os
import numpy as np


class ObjectDataForVideo():
    def __init__(self, filename, filter_threshold=None):
        self.filename = filename
        self.filter_threshold = filter_threshold

        if os.path.isfile(self.filename):
            self.data = json.load(open(self.filename, 'r'))
        else:
            self.data = []

    def append_none(self):
        self.data.append(None)

    def append_data(self, data):
        self.data.append(data)

    def append_raw_data(self, result):
        if self.filter_threshold:
            good = result['detection_scores'] > self.filter_threshold
        else:
            good = np.ones_like(result['detection_scores'], dtype=bool)
        boxes = result['detection_boxes'][good].tolist()
        scores = result['detection_scores'][good].tolist()
        entities = [b.decode('ascii')
                    for b in result['detection_class_entities'][good].tolist()]
        self.append_data({
            'boxes': boxes,
            'scores': scores,
            'entities': entities
        })

    def save(self):
        json.dump(self.data, open(self.filename))
