import sys
from os import mkdir
from os.path import basename, expandvars, exists

from numpy import concatenate
from scipy import sum

import gimp_drawer.gimp.initializer as initializer
from gimp_drawer import rendering
from gimp_drawer.config import improvements as imprvs
from gimp_drawer.decorators import timed
from gimp_drawer.gimp.items.image import Image
from gimp_drawer.space import ToolSpace

OUT_PATH = None


class Environment(object):
    @timed
    def __init__(self, src_path, acceptable_distance, mode):
        self.src_path = src_path
        src_img, img = initializer.initialize(src_path)
        self.src_img = Image(src_img)
        self.img = Image(img)
        self.prev_img = None
        self.acceptable_dist = acceptable_distance
        self.state = None
        self.reward = 0
        self.distance = sys.maxint
        self.done = False
        self.action_space = ToolSpace()
        self.viewer = None
        self.version_info = self.__construct_version_info()

    @timed
    def __construct_version_info(self):
        return "_{}_{}_{}".format(
            imprvs["eps"],
            imprvs["improvements_by_one_attempt"],
            imprvs["attempts"]
        )

    @timed
    def reset(self):
        self.__setup_output()
        self.img.reset()
        return self.state

    @timed
    def __setup_output(self):
        global OUT_PATH
        filename = str(basename(self.src_path).split(".")[0])
        OUT_PATH = expandvars("$GIMP_PROJECT/out/%s/" % filename)
        if not exists(OUT_PATH):
            mkdir(OUT_PATH)

    @timed
    def render(self):
        if self.viewer is None:
            self.viewer = rendering.SimpleImageViewer()
        images_to_display = (self.src_img.displayable_array, self.img.displayable_array)
        image = concatenate(images_to_display, axis=1)
        self.viewer.img_show(image)

    @timed
    def save(self, seconds):
        distance = "_d_" + str(self.distance)
        time = "_" + self.__format_time(seconds)
        parameter = distance + time + self.version_info
        filename = basename(self.src_path).split(".")[0] + parameter + "_" + ".jpg"
        self.img.save(OUT_PATH + filename)

    @staticmethod
    @timed
    def __format_time(seconds):
        minutes = seconds / 60
        hours = seconds / 3600
        if minutes < 1:
            return "%.1f" % seconds + "s"
        elif hours < 1:
            return "%.1f" % minutes + "m"
        return "%.1f" % hours + "h"

    @timed
    def step(self, action, args):
        self.prev_img = self.img.duplicate()
        self.img.perform_action(action, args)
        self.__calculate_reward()
        self.__check_if_done()
        return self.reward, self.done

    @timed
    def __calculate_reward(self):
        new_distance = sum(abs(self.src_img.array - self.img.array))
        self.reward = int(self.distance) - int(new_distance)
        self.distance = int(new_distance)

    @timed
    def __check_if_done(self):
        self.done = self.distance <= self.acceptable_dist

    @timed
    def undo(self):
        self.img.delete()
        self.img = Image(self.prev_img.img)
        self.__calculate_reward()
