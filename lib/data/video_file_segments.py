import os
import pandas as pd


class VideoFileSegments:
    def __init__(self, filename='interesting_video_parts.csv'):
        self.filename = filename

        self._load()

    def _load(self):
        if os.path.isfile(self.filename):
            self.data = pd.read_csv(self.filename, index_col=0)
        else:
            self.data = pd.DataFrame(
                columns=['filename', 'start', 'end', 'status', 'video_file'])

    def append_entry(self, video_filename, interval):
        self.data = self.data.append({
            'filename': video_filename,
            'start': interval[0],
            'end': interval[1],
            'status': 'unseen',
            'video_file': None
        }, ignore_index=True)

    def save(self):
        self.data.to_csv(self.filename, index_label='index')

    def get_first_unseen(self):
        return self.get_first_with_status('unseen')


    def get_first_with_status(self, status):
        unseen_data = self.data[self.data['status'] == status]
        if len(unseen_data) == 0:
            return

        first_entry = unseen_data.head(1)
        first_entry_as_dict = first_entry.iloc[0].to_dict()
        first_entry_as_dict['index'] = first_entry.index[0]

        return first_entry_as_dict

    def count_with_status(self, status):
        return (self.data['status'] == status).sum()

    def set_status(self, index, status):
        self.data.at[index, 'status'] = status

    def set_video_filename(self, index, video_file):
        self.data.at[index, 'video_file'] = video_file

    def update_status_from_to(self, old_status, new_status):
        self.data = self.data.replace({'status': {old_status: new_status}})
