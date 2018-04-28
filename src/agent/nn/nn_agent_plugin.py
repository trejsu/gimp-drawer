import time
import numpy as np
import os

from gimpfu import *

from src.gimp.environment import Environment
from src.nn.model.conv_network import ConvNetwork
from src.common.numpy_image_utils import flatten_channels
from src.common.math import sigmoid


class Agent(object):

    def __init__(self, source, render, actions, model, save, size, channels, sigmoid, sleep):
        self.render = render
        self.env = Environment(source, 0, "None", actions, size)
        self.done = False
        self.start = None
        self.nn = ConvNetwork(model)
        self.save = save
        self.model_path = model
        self.channels = channels
        self.sigmoid = sigmoid
        self.sleep = sleep

    def run(self):
        diff = self.env.reset()
        action = Environment.Action.RECTANGLE
        while not self.done:
            if self.channels == 1:
                diff = flatten_channels(diff)
            print('agent')
            print(diff[0][0])
            args = self.nn.generate_args(diff)
            if self.sigmoid:
                args = sigmoid(np.array(args, dtype=np.float128))
            _, self.done, diff = self.env.step(action, args)
            if self.render:
                self.env.render()
                time.sleep(self.sleep)
        self.__finish()

    def __finish(self):
        if self.save:
            model_name = str(os.path.basename(self.model_path))
            image_dir = os.path.expandvars("$GIMP_PROJECT/result/gimp_images/nn/")
            self.env.save_jpg(image_dir + model_name + "_" + str(time.time()) + ".jpg")


def plugin_main(source, render, actions, model, save, size, channels, sigmoid, sleep):
    agent = Agent(source, render, actions, model, save, size, channels, sigmoid, sleep)
    agent.run()


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