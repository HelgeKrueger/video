import os
import numpy as np
import matplotlib.pyplot as plt

import tensorflow as tf
import tensorflow_hub


class StyleTransfer():
    def __init__(self,
                 style_image='https://upload.wikimedia.org/wikipedia/commons/0/0a/The_Great_Wave_off_Kanagawa.jpg',
                 hub_handle='https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/1'):
        self.hub_module = tensorflow_hub.load(hub_handle)
        self.style_image_url = style_image
        self.style_image = self._load_style_image()

    def _load_style_image(self):
        image_path = tf.keras.utils.get_file(
            os.path.basename(self.style_image_url)[-128:], self.style_image_url)

        return self._resize_image(plt.imread(image_path), (256, 256))

    def _resize_image(self, image, size):
        img = image.astype(np.float32)[np.newaxis, ...] / 255.
        return tf.image.resize(img, size, preserve_aspect_ratio=True)

    def transform_frame(self, frame, new_size=(480, 270)):
        for_tf = self._resize_image(frame, new_size)
        outputs = self.hub_module(for_tf, self.style_image)

        return outputs[0][0, :, :, :].numpy() * 256
