import json

import numpy as np
import pandas as pd

from tqdm import tqdm
from interval import interval


def safe_entities(d):
    if d is None:
        return []
    else:
        return d['entities']


class ObjectData:
    def __init__(self):
        self.data = pd.DataFrame()
        self.entities = []
        self.input_data = None

    def load(self, filename):
        self.input_data = json.load(open(filename, 'r'))

        entities = [safe_entities(d) for d in self.input_data]
        self._fill_dataframe(entities)

    def _fill_dataframe(self, entities):
        self.data = pd.DataFrame()
        self.data['s'] = range(int(len(entities) / 30) + 1)
        for idx, ent in tqdm(enumerate(entities)):
            names, counts = np.unique(ent, return_counts=True)
            for name, count in zip(names, counts):
                if name not in self.data:
                    self.data[name] = 0
                self.data.at[int(idx / 30), name] += count

    def compute_intervals(self, key):
        last_seen = None
        intervals = []

        for idx, count in self.data[key].items():
            if count > 0 and last_seen is None:
                last_seen = idx

            if count == 0 and last_seen is not None:
                intervals.append([last_seen, idx])
                last_seen = None

        if last_seen is not None:
            intervals.append([last_seen, len(self.data)])

        return intervals

    def intervals_for_list(self, keys):
        keys = [k for k in keys if k in self.get_keys()]
        merged_intervals = interval(*self.compute_intervals(keys[0]))
        for key in keys[1:]:
            merged_intervals = merged_intervals | interval(
                *self.compute_intervals(key))

        return [i for i in merged_intervals]

    def intervals_not_containing(self, keys, length=60):
        intervals_containing = interval(*self.intervals_for_list(keys))
        intervals_containing = intervals_containing + interval([0, length])

        intervals_not_containing = []
        start_point = None

        for i in intervals_containing:
            if start_point is not None:
                intervals_not_containing.append([start_point, i[0]])

            start_point = i[1] - 60

        return intervals_not_containing

    def get_keys(self):
        return [k for k in self.data.keys() if k != 's']

    def times_object_appears(self, key):
        return self.data[self.data[key] > 0]['s'].to_list()

    def determine_frame_containing_key(self, s, key, fps=30):
        result = []
        for t in range(0, int(fps)):
            tt = s * int(fps) + t
            data = self.input_data[tt]
            if data and key in data['entities']:
                indices = [i for i, k in enumerate(
                    data['entities']) if k == key]
                boxes = [data['boxes'][i] for i in indices]
                result.append({'time': s * fps + t, 'boxes': boxes})

        return result

    def get_instances_key_appears(self, key, fps=30):
        times = self.times_object_appears(key)
        instances = []
        for t in times:
            instances = instances + \
                self.determine_frame_containing_key(t, key, fps=fps)

        return instances
