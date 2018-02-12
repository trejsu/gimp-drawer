import os

from numpy import concatenate

import gimp_drawer.environment.initializer as initializer
from gimp_drawer.common.decorators.timed import timed
from gimp_drawer.environment import rendering
from gimp_drawer.environment.image import Image


class TestModelEnvironment(object):
    def __init__(self, size):
        label_img, conv_img = initializer.initialize_for_model_testing(size)
        self.label_img = Image(label_img)
        self.conv_img = Image(conv_img)
        self.viewer = None
        self.size = size

    @timed
    def render_with(self, src_name):
        images_dir = os.path.expandvars("$GIMP_PROJECT/resources/scaled_images/")
        src_img = initializer.load_scaled_src(images_dir + src_name + ".jpg", self.size)
        if self.viewer is None:
            self.viewer = rendering.SimpleImageViewer()
        image = self.__get_concatenated_label_with_conv(Image(src_img))
        self.viewer.img_show(image)

    @timed
    def __get_concatenated_label_with_conv(self, src_img):
        images_to_display = (src_img.get_displayable_array(),
                             self.label_img.get_displayable_array(),
                             self.conv_img.get_displayable_array())
        image = concatenate(images_to_display, axis=1)
        return image

    @timed
    def label_step(self, action, args):
        self.label_img.perform_action(action, args)

    @timed
    def conv_step(self, action, args):
        self.conv_img.perform_action(action, args)

    @timed
    def reset(self):
        self.label_img.clear()
        self.conv_img.clear()
