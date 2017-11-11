import random
import sys
from os.path import basename, expandvars, exists
from os import mkdir
from gimpfu import pdb, gimp
import numpy
from scipy import sum

OUT_PATH = None


class GimpEnv(object):
    def __init__(self, src_path, acceptable_distance):
        self.src_path = src_path
        self.src_img, self.img = pdb.python_fu_initialize(src_path)
        self.prev_img = None
        self.src_array = self.__read(self.src_img)
        self.acceptable_dist = acceptable_distance
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

    def reset(self):
        self.__setup_output()
        pdb.python_fu_reset(self.img)
        self.__update_state()
        return self.state

    def __setup_output(self):
        global OUT_PATH
        filename = str(basename(self.src_path).split(".")[0])
        OUT_PATH = expandvars("$GIMP_PROJECT/out/%s/" % filename)
        if not exists(OUT_PATH):
            mkdir(OUT_PATH)

    @staticmethod
    def __read(image):
        drawable = pdb.gimp_image_active_drawable(image)
        width = drawable.width
        height = drawable.height
        bytes_per_pixel = drawable.bpp
        pixel_region = drawable.get_pixel_rgn(0, 0, width, height, False)
        array = numpy.fromstring(pixel_region[:, :], "B")
        assert array.size == width * height * bytes_per_pixel
        reshape = array.reshape(height, width, bytes_per_pixel)
        return numpy.array(reshape, "d")[:, :, 0:min(bytes_per_pixel, 3)]

    def __update_state(self):
        self.array = GimpEnv.__read(self.img)
        self.state = (self.src_array, self.array)

    def render(self):
        print "current distance:", self.distance

    def save(self, seconds, iterations=None):
        distance = "_d_" + str(self.distance)
        iterations = "_i_" + str(iterations)
        time = "_" + self.__format_time(seconds)
        parameter = (distance if iterations is None else iterations) + time
        filename = basename(self.src_path).split(".")[0] + parameter + ".jpg"
        self.__save_img(OUT_PATH + filename)

    def __save_img(self, filename):
        pdb.file_jpeg_save(self.img, self.__get_drawable(), filename,
                           filename, 0.9, 0, 0, 0, "", 0, 0, 0, 0)

    @staticmethod
    def __format_time(seconds):
        minutes = seconds / 60
        hours = seconds / 3600
        if minutes < 1:
            return "%.1f" % seconds + "s"
        elif hours < 1:
            return "%.1f" % minutes + "m"
        return "%.1f" % hours + "h"

    def __get_drawable(self):
        return pdb.gimp_image_active_drawable(self.img)

    def step(self, action):
        self.prev_img = pdb.gimp_image_duplicate(self.img)
        self.actions[action]()
        self.__update_state()
        self.__calculate_reward()
        self.__check_if_done()
        return self.state, self.reward, self.done, {
            "current_distance": self.distance}

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
