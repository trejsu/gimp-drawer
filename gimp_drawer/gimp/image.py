from gimp_drawer.convert import read_drawable
from gimpfu import pdb, gimp
from gimp_drawer.decorators import timed
import gimp_drawer.gimp.action_performer as action_performer
import gimp_drawer.gimp.initializer as initializer


class Image(object):
    @timed
    def __init__(self, img):
        self.img = img
        self.array = None
        self.displayable_array = None
        self.__update_arrays()

    @timed
    def save(self, filename):
        pdb.file_jpeg_save(self.img, self.__get_drawable(), filename,
                           filename, 0.9, 0, 0, 0, "", 0, 0, 0, 0)

    @timed
    def perform_action(self, action, args):
        action_performer.perform_action(self.img, action, args)
        self.__update_arrays()

    @timed
    def delete(self):
        gimp.delete(self.img)

    @timed
    def reset(self):
        initializer.reset(self.img)
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
