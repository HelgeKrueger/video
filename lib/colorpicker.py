import hashlib

from PIL import ImageColor

class Colorpicker:
    def __init__(self):
        self.colormap = list(ImageColor.colormap.keys())
        self.colormap.sort()
        self.number_of_colors = len(self.colormap)

    def for_title(self, title):
        m = hashlib.sha256()
        m.update(title.encode('ascii'))
        h = int(m.hexdigest(), 16)
        color_name = self.colormap[h % self.number_of_colors]
        return ImageColor.getrgb(color_name)
