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

    def perform_action(self, action, args):
        arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8 = self.__just(8, args)
        arg8 = 0.
        if len(args) == 8:
            arg8 = args[7]

        pdb.python_fu_perform_action(self.img, action, arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8)
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

    def __just(self, n, seq):
        it = iter(seq)
        for _ in range(n - 1):
            yield next(it, None)
        yield tuple(it)
