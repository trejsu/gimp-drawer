import json
import time
import numpy as np
import scipy.misc
import os

from gimpfu import *

from gimp_drawer.environment.image import Image
from gimp_drawer.environment.initializer import initialize_with_scaled_src


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    import re
    return [atoi(c) for c in re.split('(\d+)', text)]


def extract_number(name):
    return name.split("_")[-1].split(".")[0]


class ImageGenerator(object):
    def __init__(self, src_path, action_type, limit, output_size, diffs):
        self.src_path = src_path
        src_image, image = initialize_with_scaled_src(self.src_path + "/src.jpg", output_size)
        self.src_image = Image(src_image)
        self.image = Image(image)
        self.diffs = diffs
        if self.diffs:
            self.action_type_limited = True if action_type >= 0 else False
            if self.action_type_limited:
                self.action_type = action_type
            self.action_number_limited = True if limit >= 0 else False
            if self.action_number_limited:
                self.limit = limit
        self.out_path = None

    def setup_diffs_output(self):
        image_number = self.src_path.split("/")[-2]
        image_dir = os.path.expandvars("$GIMP_PROJECT/diffs/%s" % image_number)
        if not os.path.exists(image_dir):
            os.mkdir(image_dir)
        self.out_path = image_dir

    def run(self):
        start = time.time()
        if self.diffs:
            self.setup_diffs_output()
        actions = self.parse_actions()
        for index, (action_type, action_args, action_json) in enumerate(actions):
            if self.should_save(action_type):
                self.save(index)
            self.image.perform_action_without_array_update(action_type, action_args)
            if self.should_save(action_type):
                os.system("cp {} {}".format(action_json, self.out_path))
        if not self.diffs:
            self.image.save(self.src_path + "/generated_image.jpg")
        end = time.time()
        print "Script executed in {} seconds".format(end - start)

    def should_save(self, action_type):
        return self.diffs and (not self.action_type_limited or action_type == self.action_type)

    def save(self, index):
        diff_image_array = abs(self.src_image.array - self.image.get_updated_array())
        path = "{}/diff_before_action_{}.npy".format(self.out_path, index + 1)
        np.save(path, diff_image_array)

    def parse_actions(self):
        import glob
        path_to_actions = self.src_path + "/*.json"
        action_files = glob.glob(path_to_actions)
        if self.diffs and self.action_number_limited:
            action_files = [f for f in action_files if int(extract_number(f)) <= self.limit]
        action_files.sort(key=natural_keys)

        actions = []

        for action_file in action_files:
            with open(action_file) as json_file:
                data = json.load(json_file)["action"]
                actions.append((data["actionNumber"], tuple(data["args"]), action_file))

        return actions


def plugin_main(src_path, action_type, limit, output_size, diffs):
    image_generator = ImageGenerator(src_path, action_type, limit, output_size, diffs)
    image_generator.run()


register("image_generator", "", "", "", "", "", "", "",
         [
             (PF_STRING, "src_path", "Path to the directory with data", ""),
             (PF_INT, "action_type", "Number of action for which diffs will be generated", ""),
             (PF_INT, "limit", "Upper bound for the number of actions which will be processed", ""),
             (PF_INT, "size", "Size to which output data will be scaled", ""),
             (PF_BOOL, "diffs", "Flag indicated if script should generate final image or diffs of performed actions", "")
         ], [], plugin_main)

main()
