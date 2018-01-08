import json
import time
import numpy as np
import scipy.misc
import os

from gimpfu import *

from gimp_drawer.environment.image import Image
from gimp_drawer.environment.initializer import initialize


class ImageGenerator(object):
    def __init__(self, src_path, action_type, limit):
        self.src_path = src_path
        src_image, image = initialize(self.src_path + "/src.jpg", "None")
        self.src_image = Image(src_image)
        self.image = Image(image)
        self.action_type_limited = True if action_type >= 0 else False
        if self.action_type_limited:
            self.action_type = action_type
        self.action_number_limited = True if limit >= 0 else False
        if self.action_number_limited:
            self.limit = limit
        self.out_path = None

    def __setup_output(self):
        image_number = self.src_path.split("/")[-2]
        image_dir = os.path.expandvars("$GIMP_PROJECT/diffs/%s" % image_number)
        if not os.path.exists(image_dir):
            os.mkdir(image_dir)
        self.out_path = image_dir

    def run(self):
        start = time.time()
        self.__setup_output()
        actions = self.__parse_actions()
        for index, (action_type, action_args, action_json) in enumerate(actions):
            if self.should_save(action_type):
                self.save(index)
            self.image.perform_action_without_array_update(action_type, action_args)
            if self.should_save(action_type):
                os.system("cp {} {}".format(action_json, self.out_path))
        self.image.save(self.src_path + "/generated_image.jpg")
        end = time.time()
        print "Image generated in {} seconds".format(end - start)

    def should_save(self, action_type):
        return not self.action_type_limited or action_type == self.action_type

    def save(self, index):
        # self.image.save(self.src_path + "/image_for_action_{}.jpg".format(index + 1))
        diff_image_array = abs(self.src_image.array - self.image.get_updated_array())
        path = "{}/diff_before_action_{}.npy".format(self.out_path, index + 1)
        np.save(path, diff_image_array)
        # scipy.misc.imsave(self.src_path + "/diff_for_action_{}.jpg".format(index + 1), diff_image_array)

    def __parse_actions(self):
        import glob
        path_to_actions = self.src_path + "/*.json"
        action_files = glob.glob(path_to_actions)
        if self.action_number_limited:
            action_files = [f for f in action_files if int(f.split("_")[-1].split(".")[0]) <= self.limit]
        action_files.sort(key=self.__natural_keys)

        actions = []

        for action_file in action_files:
            with open(action_file) as json_file:
                action_data = json.load(json_file)["action"]
                actions.append((action_data["actionNumber"], tuple(action_data["args"]), action_file))

        return actions

    def __atoi(self, text):
        return int(text) if text.isdigit() else text

    def __natural_keys(self, text):
        import re
        return [self.__atoi(c) for c in re.split('(\d+)', text)]


def plugin_main(src_path, action_type, limit):
    print "plugin main?"
    image_generator = ImageGenerator(src_path, action_type, limit)
    image_generator.run()


register("image_generator", "", "", "", "", "", "", "",
         [
             (PF_STRING, "src_path", "Source", ""),
             (PF_INT, "action_type", "Action", ""),
             (PF_INT, "limit", "Limit", "")
         ], [], plugin_main)

main()
