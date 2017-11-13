import random
import sys
from os.path import basename, expandvars, exists
from os import mkdir
from gimpfu import pdb
from scipy import sum
from gimp_drawer import rendering
from numpy import concatenate
from gimp_drawer.image import Image

OUT_PATH = None


class GimpEnv(object):
    def __init__(self, src_path, acceptable_distance):
        self.src_path = src_path
        src_img, img = pdb.python_fu_initialize(src_path)
        self.src_img = Image(src_img)
        self.img = Image(img)
        self.prev_img = None
        self.acceptable_dist = acceptable_distance
        self.state = None
        self.reward = 0
        self.distance = sys.maxint
        self.done = False
        self.action_space = self.Space(4)
        self.actions = {
            0: lambda: self.img.draw_random_brush_line(),
            1: lambda: self.img.draw_random_ellipse(),
            2: lambda: self.img.draw_random_rectangle(),
            3: lambda: self.img.draw_random_pencil_line()
        }
        self.viewer = None

    def reset(self):
        self.__setup_output()
        self.img.reset()
        return self.state

    def __setup_output(self):
        global OUT_PATH
        filename = str(basename(self.src_path).split(".")[0])
        OUT_PATH = expandvars("$GIMP_PROJECT/out/%s/" % filename)
        if not exists(OUT_PATH):
            mkdir(OUT_PATH)

    def render(self):
        if self.viewer is None:
            self.viewer = rendering.SimpleImageViewer()
        images_to_display = (self.src_img.displayable_array, self.img.displayable_array)
        image = concatenate(images_to_display, axis=1)
        self.viewer.img_show(image)

    def save(self, seconds, i=None):
        distance = "_d_" + str(self.distance)
        iterations = "_i_" + str(i)
        time = "_" + self.__format_time(seconds)
        parameter = (distance if i is None else iterations) + time
        filename = basename(self.src_path).split(".")[0] + parameter + ".jpg"
        self.img.save(OUT_PATH + filename)

    @staticmethod
    def __format_time(seconds):
        minutes = seconds / 60
        hours = seconds / 3600
        if minutes < 1:
            return "%.1f" % seconds + "s"
        elif hours < 1:
            return "%.1f" % minutes + "m"
        return "%.1f" % hours + "h"

    def step(self, action):
        self.prev_img = self.img.duplicate()
        self.actions[action]()
        self.__calculate_reward()
        self.__check_if_done()
        return self.state, self.reward, self.done, {
            "current_distance": self.distance}

    def __calculate_reward(self):
        new_distance = sum(abs(self.src_img.array - self.img.array))
        self.reward = int(self.distance) - int(new_distance)
        self.distance = int(new_distance)

    def __check_if_done(self):
        self.done = self.distance <= self.acceptable_dist

    def restore_state(self):
        self.img.delete()
        self.img = Image(self.prev_img.img)
        self.__calculate_reward()

    class Space(object):
        def __init__(self, n):
            self.n = n

        def sample(self):
            return random.randint(0, self.n - 1)
