import time
import numpy as np
import os

from gimpfu import *

from common.timed import timed, print_result
from config import timers
from gimp.environment import Environment
from nn.model.conv_network import ConvNetwork


class Agent(object):

    def __init__(self, src_path, render, input_path, actions, model_path, save, size):
        self.render = render
        self.env = Environment(src_path, 0, input_path, actions, size)
        self.done = False
        self.start = None
        self.action_start = None
        self.conv_network = ConvNetwork(model_path)
        self.save = save
        self.model_path = model_path

    @timed
    def run(self):
        self.__initialize()
        upper_bound = [1., 1., 1., 1., 1., 1., 1., 1., 1.]
        lower_bound = [0., 0., 0., 0., 0., 0., 0., 0., 0.]
        self.action_start = time.time()
        diff = self.env.reset()
        # only action 0 (ellipse) for now
        action = 0
        prev_args = (0, 0, 0, 0, 0, 0, 0, 0, 0)
        while not self.done:
            args = self.conv_network.generate_args(diff)
            # assert (all(0. <= arg <= 1. for arg in args))
            if all(prev_args == args):
                args += np.random.normal(size=9, scale=0.4)
            prev_args = args
            args = np.minimum(args, upper_bound)
            args = np.maximum(args, lower_bound)
            print args
            reward, self.done, diff = self.env.step(action, args)
            if self.render:
                self.env.render()
        self.__finish()

    @timed
    def __finish(self):
        # self.env.generate_image()
        if timers:
            print_result()
        if self.save:
            model_name = str(os.path.basename(self.model_path))
            image_dir = os.path.expandvars("$GIMP_PROJECT/out/model/test/")
            self.env.save_jpg(image_dir + model_name + "_" + str(time.time()) + ".jpg")

    @timed
    def __initialize(self):
        self.start = time.time()


def plugin_main(src_path, render, input_path, actions, model_path, save):
    agent = Agent(src_path, render, input_path, actions, model_path, save)
    agent.run()


register("conv_agent", "", "", "", "", "", "", "",
         [
             (PF_STRING, "src_path", "Path to the source image", ""),
             (PF_BOOL, "render", "render image during drawing", True),
             (PF_STRING, "input_path", "Path to the input image - None means starting from white blank image", ""),
             (PF_FLOAT, "Actions", "Number of actions which will be performed", 0),
             (PF_STRING, "model_path", "Path to the model which will be computing action parameters", ""),
             (PF_BOOL, "save", "Save drawn image", False),
             (PF_INT, "size", "Size of drawn image", False)
         ], [], plugin_main)

main()