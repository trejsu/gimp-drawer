import time
import numpy as np
import os

from gimpfu import *

from src.gimp.environment import Environment
from src.nn.model.conv_network import ConvNetwork
from src.common.numpy_image_utils import flatten_channels
from src.common import math


def plugin_main(source, render, actions, model, save, size, channels, sigmoid, sleep):
    env = Environment(source, 0, "None", actions, size)
    done = False
    nn = ConvNetwork(model)

    diff = env.reset()
    action = Environment.Action.RECTANGLE

    while not done:
        if channels == 1:
            diff = flatten_channels(diff)
        args = nn.generate_args(diff)
        if sigmoid:
            args = math.sigmoid(np.array(args, dtype=np.float128))
        _, done, diff = env.step(action, args)
        if render:
            env.render()
            time.sleep(sleep)
    finish(save, model, env)


def finish(save, model, env):
    if save:
        model_name = str(os.path.basename(model))
        image_dir = os.path.expandvars("$GIMP_PROJECT/result/gimp_images/nn/")
        env.save_jpg(image_dir + model_name + "_" + str(time.time()) + ".jpg")


register("nn_agent", "", "", "", "", "", "", "",
         [
             (PF_STRING, "source", "", ""),
             (PF_BOOL, "render", "render image during drawing", False),
             (PF_INT, "actions", "number of shapes to draw", 0),
             (PF_STRING, "model", "", ""),
             (PF_BOOL, "save", "", False),
             (PF_INT, "size", "size of result image - must match network input", 0),
             (PF_INT, "channels", "", 0),
             (PF_BOOL, "sigmoid", "", False),
             (PF_INT, "sleep", "", 0)
         ], [], plugin_main)

main()