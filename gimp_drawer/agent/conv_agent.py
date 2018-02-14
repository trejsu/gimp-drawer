import time
import numpy as np

from gimpfu import *

from gimp_drawer.agent.mode import RenderMode
from gimp_drawer.common.decorators.timed import timed, print_result
from gimp_drawer.config import timers
from gimp_drawer.environment.environment import Environment
from model.conv_network import ConvNetwork


class Agent(object):

    RENDER_DEFAULT_MODES = {RenderMode.ALL, RenderMode.STANDARD}

    def __init__(self, src_path, render_mode, input_path, actions, model_path):
        self.render_mode = RenderMode(render_mode)
        self.env = Environment(src_path, 0, input_path, actions)
        self.done = False
        self.start = None
        self.action_start = None
        self.conv_network = ConvNetwork(model_path)

    @timed
    def run(self):
        self.__initialize()
        upper_bound = [1., 1., 1., 1., 1., 1., 1., 1., 1.]
        lower_bound = [0., 0., 0., 0., 0., 0., 0., 0., -1.]
        # for _ in range(1000):
        #     args = np.random.normal(size=9)
        #     args = np.minimum(args, upper_bound)
        #     args = np.maximum(args, lower_bound)
        #     # print args
        #     self.env.step(0, args)

        self.action_start = time.time()
        diff = self.env.reset()
        # only action 0 (ellipse) for now
        action = 0
        prev_args = (0, 0, 0, 0, 0, 0, 0, 0, 0)
        while not self.done:
            args = self.conv_network.generate_args(diff)
            # args += np.random.normal(size=9, scale=0.4)
            # print "original args:", args
            args = np.minimum(args, upper_bound)
            args = np.maximum(args, lower_bound)
            # print "fixed args:", args
            if all(prev_args == args):
                args += np.random.normal(size=9, scale=0.4)
            args = np.minimum(args, upper_bound)
            args = np.maximum(args, lower_bound)
            reward, self.done, diff = self.env.step(action, args)
            self.env.render()
            prev_args = args
        self.__finish()

    @timed
    def __finish(self):
        # self.env.generate_image()
        if timers:
            print_result()

    @timed
    def __initialize(self):
        self.start = time.time()

    @timed
    def __render_default(self):
        return self.render_mode in Agent.RENDER_DEFAULT_MODES


def plugin_main(src_path, render_mode, input_path, actions, model_path):
    agent = Agent(src_path, render_mode, input_path, actions, model_path)
    agent.run()


register("conv_agent", "", "", "", "", "", "", "",
         [
             (PF_STRING, "src_path", "Path to the source image", ""),
             (PF_INT, "render_mode", "Render mode", 0),
             (PF_STRING, "input_path", "Path to the input image - None means starting from white blank image", ""),
             (PF_FLOAT, "Actions", "Number of actions which will be performed", 0),
             (PF_STRING, "model_path", "Path to the model which will be computing action parameters", "")
         ], [], plugin_main)

main()
