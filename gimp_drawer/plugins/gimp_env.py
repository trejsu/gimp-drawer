import random
import sys
from os.path import basename, expandvars, exists
from os import mkdir
from gimpfu import pdb, gimp
from gimp_drawer.img_to_array import *
from scipy import sum
from gimp_drawer import rendering
from numpy import concatenate

OUT_PATH = None


class GimpEnv(object):
    def __init__(self, src_path, acceptable_distance):
        self.src_path = src_path
        self.src_img, self.img = pdb.python_fu_initialize(src_path)
        self.prev_img = None
        self.src_array, self.src_displayable_array = \
            convert_to_array(self.__get_drawable(self.src_img))
        self.acceptable_dist = acceptable_distance
        self.array = None
        self.displayable_array = None
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
        self.viewer = None

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

    def __update_state(self):
        self.array, self.displayable_array = \
            convert_to_array(self.__get_drawable(self.img))
        self.state = (self.src_array, self.array)

    def render(self):
        if self.viewer is None:
            self.viewer = rendering.SimpleImageViewer()
        images_to_display = (self.src_displayable_array, self.displayable_array)
        image = concatenate(images_to_display, axis=1)
        self.viewer.img_show(image)

    def save(self, seconds, i=None):
        distance = "_d_" + str(self.distance)
        iterations = "_i_" + str(i)
        time = "_" + self.__format_time(seconds)
        parameter = (distance if i is None else iterations) + time
        filename = basename(self.src_path).split(".")[0] + parameter + ".jpg"
        self.__save_img(OUT_PATH + filename)

    def __save_img(self, filename):
        pdb.file_jpeg_save(self.img, self.__get_drawable(self.img), filename,
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

    def __get_drawable(self, img):
        return pdb.gimp_image_active_drawable(img)

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
        self.distance = int(new_distance)

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
