import numpy as np

from gimpfu import *
from src.gimp.environment import Environment
from src.gimp.image import Image
import src.gimp.initializer as initializer


def plugin_main(action_args, size, output_path):
    action_args_np = np.load(action_args)
    image = Image(initializer.new_image(size, size))
    print(action_args_np)
    action_args_tuples = [(int(x[0]), remove_last_arg(x[0], x[1:])) for x in action_args_np]
    for action, args in action_args_tuples:
        image.perform_action(action, args)
    image.save(output_path)


def remove_last_arg(action, args):
    if action != Environment.Action.TRIANGLE:
        return args[:-1]
    return args








