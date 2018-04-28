import os
import json
import datetime
import numpy as np

from numpy import concatenate
from scipy import sum, misc
from gimpfu import pdb

import src.common.format as formatter
import src.gimp.initializer as initializer
from src.common.timed import timed
from src.config import improvements as imprvs
from src.config import reducer_rate
from src.common import rendering
from src.gimp.image import Image
from src.gimp.space import ToolSpace


class Environment(object):
    def __init__(self, src_path, acceptable_distance, input_path, actions, size):
        self.src_path = src_path
        src_img, img = initializer.initialize(src_path, input_path, size)
        self.src_img = Image(src_img)
        self.img = Image(img)
        self.prev_img = None
        self.acceptable_dist = acceptable_distance
        self.state = None
        self.reward = 0
        self.prev_reward = 0
        self.distance = sum(abs(self.src_img.array - self.img.array))
        self.prev_distance = 0
        self.done = False
        self.action_space = ToolSpace()
        self.viewer = None
        self.version_info = self.construct_version_info()
        self.out_path = None
        self.undo_before_step = False
        self.action = None
        self.args = None
        self.successful_actions = 0
        self.actions_before_success = 0
        self.actions = actions

    @timed
    def construct_version_info(self):
        additional_info = ""
        return "{}_{}_{}_{}_space_{}_{}".format(
            imprvs["eps"],
            imprvs["improvements_by_one_attempt"],
            imprvs["attempts"],
            reducer_rate,
            self.action_space.n, additional_info
        )

    @timed
    def reset(self):
        # self.__setup_output()
        return (self.src_img.array - self.img.array) / 255.

    @timed
    def setup_output(self):
        filename = str(os.path.basename(self.src_path).split(".")[0])
        image_dir = os.path.expandvars("$GIMP_PROJECT/out/drawing/%s" % filename)
        date = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        execution_dirname = date + "_" + self.version_info
        if not os.path.exists(image_dir):
            os.mkdir(image_dir)
        self.out_path = "%s/%s" % (image_dir, execution_dirname)
        os.mkdir(self.out_path)
        self.src_img.save(self.out_path + "/src.jpg")

    @timed
    def render(self):
        if self.viewer is None:
            self.viewer = rendering.SimpleImageViewer()
        image = self.get_concatenated_src_with_image(self.img)
        self.viewer.img_show(image)

    @timed
    def get_concatenated_src_with_image(self, image_to_concatenate):
        images_to_display = (self.src_img.get_displayable_array(),
                             image_to_concatenate.get_displayable_array())
        image = concatenate(images_to_display, axis=1)
        return image

    @timed
    def save(self, seconds_from_start, seconds_for_action):
        data = self.construct_json_data(seconds_from_start, seconds_for_action)
        action_string = "action_{}".format(self.successful_actions)
        with open(self.out_path + "/{}.json".format(action_string), "w") as outfile:
            json.dump(data, outfile, sort_keys=True, indent=4, separators=(',', ': '))
        if self.successful_actions % 100 == 0:
            np.save(self.out_path + "/{}.npy".format(action_string), self.img.array)
        self.actions_before_success = 0

    @timed
    def save_jpg(self, path):
        misc.imsave(path, self.get_concatenated_src_with_image(self.img))

    @timed
    def construct_json_data(self, seconds_from_start, seconds_for_action):
        return {
            "distanceBefore": self.prev_distance,
            "distanceAfter": self.distance,
            "reward": self.reward,
            "time": int(seconds_from_start * 1000),
            "timeString": formatter.format_time(seconds_from_start),
            "actionTime": int(seconds_for_action * 1000),
            "actionTimeString": formatter.format_time(seconds_for_action),
            "action": {
                "actionNumber": self.action,
                "actionString": self.action_space.subspace_name(self.action),
                "args": self.args,
            },
            "configuration": {
                "epsilon": imprvs["eps"],
                "improvementsByOneAttempt": imprvs["improvements_by_one_attempt"],
                "attempts": imprvs["attempts"]
            },
            "numberOfActionsBeforeSuccess": self.actions_before_success - 1
        }

    @timed
    def step(self, action, args):
        self.successful_actions += 1
        self.actions_before_success += 1
        if self.prev_img is not None and not self.undo_before_step:
            self.prev_img.delete()
        self.prev_img = self.img
        self.img = self.img.duplicate()
        self.prev_reward = self.reward
        self.prev_distance = self.distance
        self.img.perform_action(action, args)
        self.update_reward_and_distance()
        self.check_if_done()
        self.undo_before_step = False
        self.action = action
        self.args = args
        diff = (self.src_img.array - self.img.array) / 255.
        return self.reward, self.done, diff

    @timed
    def update_reward_and_distance(self):
        new_distance = np.sum(np.abs(self.src_img.array - self.img.array))
        self.reward = int(self.distance) - int(new_distance)
        self.distance = int(new_distance)

    @timed
    def check_if_done(self):
        self.done = self.distance <= self.acceptable_dist or self.successful_actions >= self.actions

    @timed
    def undo(self):
        self.successful_actions -= 1
        self.img.delete()
        self.img = Image(self.prev_img.img, self.prev_img.array)
        self.reward = self.prev_reward
        self.distance = self.prev_distance
        self.undo_before_step = True

    @timed
    def generate_image(self):
        pdb.python_fu_image_generator(self.out_path)
        results_dir = os.path.expandvars("$GIMP_PROJECT/results")
        if not os.path.exists(results_dir):
            os.mkdir(results_dir)
        filename = str(os.path.basename(self.src_path).split(".")[0])
        image_result_dir = results_dir + "/" + filename
        if not os.path.exists(image_result_dir):
            os.mkdir(image_result_dir)
        os.system("cp {} {}".format(self.out_path + "/generated_image.jpg", image_result_dir))
        os.system("cp {} {}".format(self.out_path + "/src.jpg", image_result_dir))

    class Action(object):
        ELLIPSE = 0
        RECTANGLE = 1
        LINE = 2
        TRIANGLE = 3

