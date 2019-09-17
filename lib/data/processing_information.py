import os
import json


class ProcessingInformation:
    def __init__(self, filename='processing_information.json'):
        self.style_transfer_image = None
        self.filename = filename

        if os.path.isfile(self.filename):
            with open(self.filename) as f:
                self.data = json.load(f)
        else:
            self.data = {}

    def get_description(self):
        lines = [
            "Code for processing video available at https://github.com/HelgeKrueger/video"]

        if 'style_transfer_image' in self.data:
            tfhub_url = 'https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/1'
            lines.append("Applied style transfer using {} with image {}".format(
                tfhub_url, self.data['style_transfer_image']))

        return "\n\n".join(lines)

    def set_style_transfer_image(self, image):
        self.data['style_transfer_image'] = image

    def done(self):
        if os.path.isfile(self.filename):
            os.remove(self.filename)

    def save(self):
        with open(self.filename, 'w') as f:
            json.dump(self.data, f)
