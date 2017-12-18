import json

from gimpfu import *

from gimp_drawer.environment.image import Image
from gimp_drawer.environment.initializer import initialize


class ImageGenerator(object):
    def __init__(self, src_path):
        self.src_path = src_path
        src_image, image = initialize(self.src_path + "/src.jpg", "None")
        self.image = Image(image)

    def run(self):
        actions = self.parse_actions()
        for action in actions:
            self.image.perform_action(action[0], action[1])
        self.image.save(self.src_path + "/generated_image.jpg")

    def parse_actions(self):
        import glob
        path_to_actions = self.src_path + "/*.json"
        action_files = glob.glob(path_to_actions)

        actions = []

        for action_file in action_files:
            with open(action_file) as json_file:
                action_data = json.load(json_file)["action"]
                actions.append((action_data["actionNumber"], tuple(action_data["args"])))

        return actions


def plugin_main(src_path):
    image_generator = ImageGenerator(src_path)
    image_generator.run()


register("image_generator", "", "", "", "", "", "", "",
         [
             (PF_STRING, "src_path", "Source", "")
         ], [], plugin_main)

main()
