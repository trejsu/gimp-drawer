import numpy as np
from gimpfu import pdb, WHITE_FILL

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
    def get_displayable_array(self):
        return self.array.astype(np.uint8)

    @timed
    def clear(self):
        pdb.gimp_edit_fill(pdb.gimp_image_active_drawable(self.img), WHITE_FILL)

    @timed
    def delete(self):
        pdb.gimp_image_delete(self.img)
