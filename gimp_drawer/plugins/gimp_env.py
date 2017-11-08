from gimpfu import pdb, gimp
import numpy
from PIL import Image
import random
from scipy import sum
import sys


class GimpEnv(object):
    def __init__(self, src_path, acceptable_dist):
        self.src_img, self.img = GimpEnv.__init_images(src_path)
        self.prev_img = None
        self.src_array = self.__read(self.src_img)
        self.acceptable_dist = acceptable_dist
        self.array = None
        self.state = None
        self.reward = 0
        self.distance = sys.maxint
        self.done = False
        self.action_space = self.Space(4)
        self.actions = {
            0: lambda: self.__draw_random_brush_line(),
            1: lambda: self.__draw_random_ellipse(),
            2: lambda: self.__draw_random_rectangle(),
            3: lambda: self.__draw_random_pencil_line()
        }
        self.displayed_src = None
        self.displayed_img = None

    @staticmethod
    def __init_images(src_path):
        return pdb.python_fu_initialize(src_path)

    def reset(self):
        pdb.python_fu_reset(self.img)
        self.__update_state()
        return self.state

    @staticmethod
    def __read(image):
        drawable = pdb.gimp_image_active_drawable(image)
        width = drawable.width
        height = drawable.height
        bpp = drawable.bpp
        pixel_region = drawable.get_pixel_rgn(0, 0, width, height, False)
        array = numpy.fromstring(pixel_region[:, :], "B")
        assert array.size == width * height * bpp
        return numpy.array(array.reshape(height, width, bpp), dtype=numpy.uint8)[:, :, 0:min(bpp, 3)]

    def __update_state(self):
        self.array = GimpEnv.__read(self.img)
        self.state = (self.src_array, self.array)

    def render(self):
        print "current distance:", self.distance

    def render_img(self):
        if self.displayed_src is None:
            self.displayed_src = Image.fromarray(self.src_array, 'RGB')
            self.displayed_src.show()
        self.displayed_img = Image.fromarray(self.array, 'RGB')
        self.displayed_img.show()

    def step(self, action):
        self.prev_img = pdb.gimp_image_duplicate(self.img)
        self.actions[action]()
        self.__update_state()
        self.__calculate_reward()
        self.__check_if_done()
        return self.state, self.reward, self.done, {}

    def __draw_random_brush_line(self):
        pdb.python_fu_perform_action(self.img, 0)

    def __draw_random_ellipse(self):
        pdb.python_fu_perform_action(self.img, 1)

    def __draw_random_rectangle(self):
        pdb.python_fu_perform_action(self.img, 2)

    def __draw_random_pencil_line(self):
        pdb.python_fu_perform_action(self.img, 3)

    def __calculate_reward(self):
        new_distance = sum(abs(self.src_array - self.array))
        self.reward = int(self.distance) - int(new_distance)
        self.distance = new_distance

    def __check_if_done(self):
        self.done = self.distance <= self.acceptable_dist

    def restore_state(self):
        gimp.delete(self.img)
        self.img = self.prev_img
        self.__update_state()
        self.__calculate_reward()

    class Space(object):
        def __init__(self, n):
            self.n = n

        def sample(self):
            return random.randint(0, self.n - 1)







