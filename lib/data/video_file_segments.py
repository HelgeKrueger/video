import os
import pandas as pd

class VideoFileSegments:
    def  __init__(self, filename='interesting_video_parts.csv'):
        self.filename = filename

        self._load()

    def _load(self):
        if os.path.isfile(self.filename):
            self.data = pd.read_csv(self.filename, index_col=0)
        else:
            self.data = pd.DataFrame(columns = ['filename', 'start', 'end', 'status'])

    def append_entry(self, video_filename, interval):
        self.data = self.data.append({
            'filename': video_filename,
            'start': interval[0],
            'end': interval[1],
            'status': 'unseen'
            }, ignore_index=True)

    def save(self):
        self.data.to_csv(self.filename, index_label='index')
