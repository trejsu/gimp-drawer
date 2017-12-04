import os
import sys

from numpy import concatenate
from scipy import sum

import gimp_drawer.common.utils.format as formatter
import gimp_drawer.environment.initializer as initializer
from gimp_drawer.common.decorators.timed import timed
from gimp_drawer.config import improvements as imprvs
from gimp_drawer.environment import rendering
from gimp_drawer.environment.image import Image
from gimp_drawer.environment.space import ToolSpace


class Environment(object):
    def __init__(self, src_path, acceptable_distance):
        self.src_path = src_path
        src_img, img = initializer.initialize(src_path)
        self.src_img = Image(src_img)
        self.img = Image(img)
        self.prev_img = None
        self.acceptable_dist = acceptable_distance
        self.state = None
        self.reward = 0
        self.prev_reward = 0
        self.distance = sys.maxint
        self.prev_distance = 0
        self.done = False
        self.action_space = ToolSpace()
        self.viewer = None
        self.version_info = self.__construct_version_info()
        self.out_path = None
        self.undo_before_step = False

    @timed
    def __construct_version_info(self):
        return "_{}_{}_{}_space_{}_{}".format(
            imprvs["eps"],
            imprvs["improvements_by_one_attempt"],
            imprvs["attempts"],
            self.action_space.n,
            "color_picker_with_default_render"
        )

    @timed
    def reset(self):
        self.__setup_output()
        self.img.reset()
        return self.state

    @timed
    def __setup_output(self):
        filename = str(os.path.basename(self.src_path).split(".")[0])
        self.out_path = os.path.expandvars("$GIMP_PROJECT/out/%s/" % filename)
        if not os.path.exists(self.out_path):
            os.mkdir(self.out_path)

    @timed
    def render(self):
        if self.viewer is None:
            self.viewer = rendering.SimpleImageViewer()
        images_to_display = (self.src_img.get_displayable_array(), self.img.get_displayable_array())
        image = concatenate(images_to_display, axis=1)
        self.viewer.img_show(image)

    @timed
    def save(self, seconds):
        distance = "_d_" + str(self.distance)
        time = "_" + formatter.format_time(seconds)
        parameter = distance + time + self.version_info
        filename = os.path.basename(self.src_path).split(".")[0] + parameter + "_" + ".jpg"
        self.img.save(self.out_path + filename)

    @timed
    def step(self, action, args):
        if self.prev_img is not None and not self.undo_before_step:
            self.prev_img.delete()
        self.prev_img = self.img
        self.img = self.img.duplicate()
        self.prev_reward = self.reward
        self.prev_distance = self.distance
        self.img.perform_action(action, args)
        self.__update_reward_and_distance()
        self.__check_if_done()
        self.undo_before_step = False
        return self.reward, self.done

    @timed
    def __update_reward_and_distance(self):
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
        self.reward = self.prev_reward
        self.distance = self.prev_distance
        self.undo_before_step = True
