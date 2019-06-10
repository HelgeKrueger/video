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

    def load(self, filename):
        input_data = json.load(open(filename, 'r'))

        entities = [safe_entities(d) for d in input_data]
        self._fill_dataframe(entities)

    def _fill_dataframe(self, entities):
        self.data = pd.DataFrame()
        self.data['s'] = range(int(len(entities) / 30))
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
        merged_intervals = interval(*self.compute_intervals(keys[0]))
        for key in keys[1:]:
            merged_intervals = merged_intervals | interval(*self.compute_intervals(key))

        return [i for i in merged_intervals]

    def get_keys(self):
        return [k for k in self.data.keys() if k != 's']
