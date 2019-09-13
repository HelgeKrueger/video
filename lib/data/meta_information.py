import os
import pandas as pd


class MetaInformation:
    def __init__(self, filename='meta_information.csv'):
        self.filename = filename

        self._load()

    def _load(self):
        if os.path.isfile(self.filename):
            self.data = pd.read_csv(self.filename, index_col=0)
        else:
            self.data = pd.DataFrame(
                columns=['filename', 'data_type', 'data'])

    def append_entry(self, video_filename, data_type, data):
        self.data = self.data.append({
            'filename': video_filename,
            'data_type': data_type,
            'data': data
        }, ignore_index=True)

    def save(self):
        self.data.to_csv(self.filename, index_label='index')
