import numpy as np
import os

from gimpfu import pdb, WHITE_FILL, HISTOGRAM_RED, HISTOGRAM_GREEN, HISTOGRAM_BLUE, FILL_FOREGROUND

from src.common.timed import timed
from src.gimp.action_performer import perform_action


class Image(object):
    def __init__(self, img, array=None):
        self.img = img
        self.array = array
        if array is None:
            self.update_array()

    @timed
    def perform_action(self, action, args):
        perform_action(self.img, action, args)
        self.update_array()

    def perform_action_without_array_update(self, action, args):
        perform_action(self.img, action, args)

    def get_updated_array(self):
        self.update_array()
        return self.array

    @timed
    def update_array(self):
        self.array = self.to_array()

    @timed
    def get_drawable(self):
        return pdb.gimp_image_active_drawable(self.img)

    @timed
    def duplicate(self):
        return Image(pdb.gimp_image_duplicate(self.img), self.array)

    @timed
    def save(self, filename):
        directory = os.path.dirname(filename)
        if not os.path.exists(directory):
            os.makedirs(directory)
        pdb.gimp_file_save(self.img, self.get_drawable(), filename, filename)

    @timed
    def to_array(self):
        drawable = self.get_drawable()
        width = drawable.width
        height = drawable.height
        bpp = drawable.bpp
        pixel_region = drawable.get_pixel_rgn(0, 0, width, height, False)
        array = np.fromstring(pixel_region[:, :], "B")
        return np.array(array.reshape(height, width, bpp), dtype="d")[:, :, 0:min(bpp, 3)]

    @timed
    def renderable(self):
        return self.array.astype(np.uint8)

    @timed
    def clear(self):
        pdb.gimp_edit_fill(pdb.gimp_image_active_drawable(self.img), WHITE_FILL)

    @timed
    def delete(self):
        pdb.gimp_image_delete(self.img)

    def get_average_color(self):
        drawable = self.get_drawable()
        red = pdb.gimp_histogram(drawable, HISTOGRAM_RED, 0, 255)[0]
        green = pdb.gimp_histogram(drawable, HISTOGRAM_GREEN, 0, 255)[0]
        blue = pdb.gimp_histogram(drawable, HISTOGRAM_BLUE, 0, 255)[0]
        return red, green, blue

    def fill_with(self, color):
        pdb.gimp_context_set_foreground(tuple(c / 255. for c in color))
        pdb.gimp_drawable_fill(self.get_drawable(), FILL_FOREGROUND)
