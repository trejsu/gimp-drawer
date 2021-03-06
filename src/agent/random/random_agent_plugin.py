import time
import numpy as np

from gimpfu import *

from agent.random.argument.argument import ArgumentGroup
from agent.random.argument.color_picker_generator import ColorPickerGenerator
from agent.random.argument.scaling_init_generator import ScalingInitGenerator
from agent.random.mode import RenderMode
from common.timed import timed, print_result
from config import improvements as imprvs, timers
from gimp.environment import Environment


class Agent(object):

    RENDER_DEFAULT_MODES = {RenderMode.ALL, RenderMode.STANDARD}
    RENDER_EVERYTHING_MODES = {RenderMode.ALL}

    def __init__(self, src_path, acceptable_distance, render_mode, input_path, seed, actions):
        self.render_mode = RenderMode(render_mode)
        self.env = Environment(src_path, acceptable_distance, input_path, actions)
        self.done = False
        self.start = None
        self.action_start = None
        self.rng = np.random.RandomState(int(seed))
        self.color_generator = ColorPickerGenerator(imprvs["eps"], self.env.src_img.img, self.rng)
        self.position_generator = ScalingInitGenerator(imprvs["eps"], self.rng)

    @timed
    def run(self):
        self.__initialize()
        while not self.done:
            self.action_start = time.time()
            actions = self.env.action_space()
            action = self.rng.choice(actions)
            args = self.__generate_initial_arguments(action)
            reward, self.done, _ = self.env.step(action, self.__transform_args(args))
            if self.__render_everything():
                self.env.render()
            self.env.undo()
            if reward > 0:
                self.__improve_args(action, args, reward)
        self.__finish()

    @timed
    def __improve_args(self, action, args, reward):
        rewards = {reward: args}
        attempts = imprvs["attempts"]
        improvements = imprvs["improvements_by_one_attempt"]
        for _ in range(attempts):
            for _ in range(improvements):
                self.__calculate_rewards_for_args(action, args, rewards)
            args = rewards[max(rewards)]
            rewards = {max(rewards): args}
        self.__perform_action_with_the_best_args(action, args)

    @timed
    def __perform_action_with_the_best_args(self, action, args):
        end = time.time()
        self.env.step(action, self.__transform_args(args))
        if self.__render_default():
            self.env.render()
        # self.env.save(end - self.start, end - self.action_start)

    @timed
    def __calculate_rewards_for_args(self, action, args, rewards):
        new_args = []
        for arg_group in args:
            new_arg_group = arg_group.generator.new(arg_group.args)
            new_args.append(ArgumentGroup(new_arg_group, arg_group.generator))
        new_reward, _, _ = self.env.step(action, self.__transform_args(new_args))
        if self.__render_everything():
            self.env.render()
        self.env.undo()
        rewards[new_reward] = new_args

    @timed
    def __generate_initial_arguments(self, action):
        subspace = self.env.action_space.subspace(action)
        position_ranges = subspace.position()
        time_passed = time.time() - self.start
        init_position = self.position_generator.init(position_ranges, time_passed, subspace)
        color_ranges = subspace.color()
        init_color = self.color_generator.init(color_ranges, init_position, subspace)
        args = [ArgumentGroup(init_color, self.color_generator),
                ArgumentGroup(init_position, self.position_generator)]
        return args

    @timed
    def __finish(self):
        self.env.generate_image()
        if timers:
            print_result()

    @timed
    def __initialize(self):
        self.start = time.time()
        self.env.reset()

    @timed
    def __transform_args(self, args):
        result = ()
        for arg_group in args:
            for arg in arg_group.to_argument_values():
                result = result + (arg,)
        return result

    @timed
    def __render_everything(self):
        return self.render_mode in Agent.RENDER_EVERYTHING_MODES

    @timed
    def __render_default(self):
        return self.render_mode in Agent.RENDER_DEFAULT_MODES


def plugin_main(src_path, acceptable_distance, render_mode, input_path, seed, actions):
    agent = Agent(src_path, acceptable_distance, render_mode, input_path, seed, actions)
    agent.run()


register("agent", "", "", "", "", "", "", "",
         [
             (PF_STRING, "src_path", "Source", ""),
             (PF_INT, "acceptable_distance", "Acceptable distance", 0),
             (PF_INT, "render_mode", "Render mode", 0),
             (PF_STRING, "input_path", "Input", ""),
             (PF_FLOAT, "Seed", "seed", 0),
             (PF_FLOAT, "Actions", "actions", 0)
         ], [], plugin_main)

main()
