import random
import time

from gimp_drawer.agent.argument_generator import ColorPickerGenerator, RandomInitGenerator
from gimpfu import *

from gimp_drawer.agent.argument import ArgumentGroup
from gimp_drawer.agent.mode import RenderMode
from gimp_drawer.agent.mode import ShapeMode
from gimp_drawer.common.decorators.timed import timed, print_result
from gimp_drawer.config import improvements as imprvs
from gimp_drawer.environment.environment import Environment


class Agent(object):

    RENDER_DEFAULT_MODES = {RenderMode.ALL, RenderMode.STANDARD}
    RENDER_EVERYTHING_MODES = {RenderMode.ALL}

    def __init__(self, src_path, acceptable_distance, shape_mode, render_mode, input_path):
        self.shape_mode = ShapeMode(shape_mode)
        self.render_mode = RenderMode(render_mode)
        self.env = Environment(src_path, acceptable_distance, input_path)
        self.done = False
        self.start = None
        self.action_start = None
        self.color_generator = ColorPickerGenerator(imprvs["eps"], self.env.src_img.img)
        self.position_generator = RandomInitGenerator(imprvs["eps"])

    @timed
    def run(self):
        self.__initialize()
        while not self.done:
            self.action_start = time.time()
            actions = self.env.action_space()
            action = random.choice(actions)
            args = self.__generate_initial_arguments(action)
            reward, self.done = self.env.step(action, self.__transform_args(args))
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
        self.env.step(action, self.__transform_args(args))
        if self.__render_default():
            self.env.render()
        end = time.time()
        self.env.save(end - self.start, end - self.action_start)

    @timed
    def __calculate_rewards_for_args(self, action, args, rewards):
        new_args = []
        for arg_group in args:
            new_arg_group = arg_group.generator.new(arg_group.args)
            new_args.append(ArgumentGroup(new_arg_group, arg_group.generator))
        new_reward, _ = self.env.step(action, self.__transform_args(new_args))
        if self.__render_everything():
            self.env.render()
        self.env.undo()
        rewards[new_reward] = new_args

    @timed
    def __generate_initial_arguments(self, action):
        subspace = self.env.action_space.subspace(action)
        position_ranges = subspace.position()
        init_position = self.position_generator.init(position_ranges)
        color_ranges = subspace.color()
        init_color = self.color_generator.init(color_ranges, init_position, subspace)
        args = [ArgumentGroup(init_color, self.color_generator),
                ArgumentGroup(init_position, self.position_generator)]
        return args

    @timed
    def __finish(self):
        end = time.time()
        self.env.save(end - self.start)
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


def plugin_main(src_path, acceptable_distance, shape_mode, render_mode, input_path):
    agent = Agent(src_path, acceptable_distance, shape_mode, render_mode, input_path)
    agent.run()


register("agent", "", "", "", "", "", "", "",
         [
             (PF_STRING, "src_path", "Source", ""),
             (PF_INT, "acceptable_distance", "Acceptable distance", 0),
             (PF_INT, "shape_mode", "Shape mode", 0),
             (PF_INT, "render_mode", "Render mode", 0),
             (PF_STRING, "input_path", "Input", "")
         ], [], plugin_main)

main()
