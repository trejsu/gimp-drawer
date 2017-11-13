from gimp_drawer.convert import read_drawable
from gimpfu import pdb, gimp


class Image(object):
    def __init__(self, img):
        self.img = img
        self.array = None
        self.displayable_array = None
        self.__update_arrays()

    def save(self, filename):
        pdb.file_jpeg_save(self.img, self.__get_drawable(), filename,
                           filename, 0.9, 0, 0, 0, "", 0, 0, 0, 0)

    def draw_random_brush_line(self):
        self.__perform_action(0)

    def draw_random_ellipse(self):
        self.__perform_action(1)

    def draw_random_rectangle(self):
        self.__perform_action(2)

    def draw_random_pencil_line(self):
        self.__perform_action(3)

    def __perform_action(self, action):
        pdb.python_fu_perform_action(self.img, action)
        self.__update_arrays()

    def delete(self):
        gimp.delete(self.img)

    def reset(self):
        pdb.python_fu_reset(self.img)
        self.__update_arrays()

    def __update_arrays(self):
        self.array, self.displayable_array = read_drawable(self.__get_drawable())

    def __get_drawable(self):
        return pdb.gimp_image_active_drawable(self.img)

    def duplicate(self):
        return Image(pdb.gimp_image_duplicate(self.img))
