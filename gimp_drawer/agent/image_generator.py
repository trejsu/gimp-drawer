import json
import time

from gimpfu import *

from gimp_drawer.environment.image import Image
from gimp_drawer.environment.initializer import initialize


class ImageGenerator(object):
    def __init__(self, src_path):
        self.src_path = src_path
        src_image, image = initialize(self.src_path + "/src.jpg", "None")
        self.image = Image(image)

    def run(self):
        start = time.time()
        actions = self.__parse_actions()
        for action in actions:
            self.image.perform_action(action[0], action[1])
        self.image.save(self.src_path + "/generated_image.jpg")
        end = time.time()
        print "Image generated in {} seconds".format(end - start)

    def __parse_actions(self):
        import glob
        path_to_actions = self.src_path + "/*.json"
        action_files = glob.glob(path_to_actions)
        action_files.sort(key=self.__natural_keys)

        actions = []

        for action_file in action_files:
            with open(action_file) as json_file:
                action_data = json.load(json_file)["action"]
                actions.append((action_data["actionNumber"], tuple(action_data["args"])))

        return actions

    def __atoi(self, text):
        return int(text) if text.isdigit() else text

    def __natural_keys(self, text):
        import re
        return [self.__atoi(c) for c in re.split('(\d+)', text)]


def plugin_main(src_path):
    image_generator = ImageGenerator(src_path)
    image_generator.run()


register("image_generator", "", "", "", "", "", "", "",
         [
             (PF_STRING, "src_path", "Source", "")
         ], [], plugin_main)

main()
