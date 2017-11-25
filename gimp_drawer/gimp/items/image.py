from gimp_drawer.convert import read_drawable
from gimpfu import pdb, gimp

from gimp_drawer.decorators import timed
from gimp_drawer.gimp.action_performer import perform_action
from gimp_drawer.gimp.initializer import reset


class Image(object):
    @timed
    def __init__(self, img):
        self.img = img
        self.array = None
        self.displayable_array = None
        self.__update_arrays()

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
                           optimize, progressive, comment, subsampling, baseline,restart, dct)

    @timed
    def perform_action(self, action, args):
        perform_action(self.img, action, args)
        self.__update_arrays()

    @timed
    def delete(self):
        gimp.delete(self.img)

    @timed
    def reset(self):
        reset(self.img)
        self.__update_arrays()

    @timed
    def __update_arrays(self):
        self.array, self.displayable_array = read_drawable(self.__get_drawable())

    @timed
    def __get_drawable(self):
        return pdb.gimp_image_active_drawable(self.img)

    @timed
    def duplicate(self):
        return Image(pdb.gimp_image_duplicate(self.img))
