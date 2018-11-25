from src.gimp.initializer import initialize
from src.gimp.image import Image
from scipy.misc import imsave
from src.common.utils import hex_to_rgb

import src.common.rendering as rendering
import numpy as np


class Environment(object):
    def __init__(self, input_path, output_path, output_size, bg):
        src_img, img = initialize(src_path=input_path, input_path=None, size=output_size)
        self.src_img = Image(src_img)
        self.img = Image(img)
        self.viewer = None
        self.output_path = output_path
        color_to_fill = self.src_img.get_average_color() if bg == 'None' else hex_to_rgb(bg)
        self.img.fill_with(color_to_fill)

    # todo: not working
    def render(self):
        if self.viewer is None:
            self.viewer = rendering.SimpleImageViewer()
        image = np.concatenate((self.src_img.renderable(), self.img.renderable()), axis=1)
        self.viewer.img_show(image)

    def save(self):
        self.img.update_array()
        imsave(self.output_path, self.img.renderable())
