import numpy as np
from gimpfu import pdb, gimp

from gimp_drawer.common.decorators.timed import timed
from gimp_drawer.environment.action_performer import perform_action


class Image(object):
    def __init__(self, img, array=None):
        self.img = img
        self.array = array
        if array is None:
            self.__update_array()

    @timed
    def perform_action(self, action, args):
        perform_action(self.img, action, args)
        self.__update_array()

    @timed
    def delete(self):
        gimp.delete(self.img)

    @timed
    def __update_array(self):
        self.array = self.__to_array()

    @timed
    def __get_drawable(self):
        return pdb.gimp_image_active_drawable(self.img)

    @timed
    def duplicate(self):
        return Image(pdb.gimp_image_duplicate(self.img), self.array)

    @timed
    def save(self, filename):
        quality = 0.9
        smoothing = 0
        optimize = 0
        progressive = 0
        comment = ""
        subsampling = 0
        baseline = 0
        restart = 0
        dct = 0
        pdb.file_jpeg_save(self.img, self.__get_drawable(), filename, filename, quality, smoothing,
                           optimize, progressive, comment, subsampling, baseline, restart, dct)

    @timed
    def __to_array(self):
        bpp, reshape = self.__process_drawable()
        return self.__get_numpy_array(reshape, "d", bpp)

    @timed
    def __to_displayable_array(self):
        bpp, reshape = self.__process_drawable()
        return self.__get_numpy_array(reshape, np.uint8, bpp)

    @timed
    def __process_drawable(self):
        drawable = self.__get_drawable()
        width = drawable.width
        height = drawable.height
        bpp = drawable.bpp
        pixel_region = drawable.get_pixel_rgn(0, 0, width, height, False)
        array = np.fromstring(pixel_region[:, :], "B")
        assert array.size == width * height * bpp
        reshape = array.reshape(height, width, bpp)
        return bpp, reshape

    @timed
    def __get_numpy_array(self, reshape, data_type, bpp):
        return np.array(reshape, dtype=data_type)[:, :, 0:min(bpp, 3)]

    @timed
    def get_displayable_array(self):
        return self.__to_displayable_array()
