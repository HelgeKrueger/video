import os

from moviepy.editor import VideoFileClip


class VideoFile:
    def __init__(self, data):
        self.data = data

        filename = self._make_filename(data['filename'])
        clip = VideoFileClip(filename)
        self.subclip = clip.without_audio().subclip(
            t_start=data['start'], t_end=data['end'])

    def _make_filename(self, filename):
        filename = os.path.join('videos/incoming', filename)
        if filename.endswith('.json'):
            filename = filename[:-5]

        if not os.path.isfile(filename):
            raise Exception("File does not exist {}".format(filename))

        return filename

    def save_as(self, video_filename):
        self.subclip.write_videofile(video_filename)
