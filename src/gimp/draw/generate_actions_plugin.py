import numpy as np
import time

from gimpfu import *
from src.gimp.environment import Environment
from src.agent.random.argument.argument import ArgumentGroup
from src.agent.random.argument.color_picker_generator import ColorPickerGenerator
from src.agent.random.argument.scaling_init_generator import ScalingInitGenerator
from src.config import improvements as imprvs


def plugin_main(output_path, image, actions, render, size):
    def generate_initial_arguments(action):
        subspace = env.action_space.subspace(action)
        position_ranges = subspace.position()
        time_passed = time.time() - start
        init_position = position_generator.init(position_ranges, time_passed, subspace)
        color_ranges = subspace.color()
        init_color = color_generator.init(color_ranges, init_position, subspace)
        args = [ArgumentGroup(init_color, color_generator),
                ArgumentGroup(init_position, position_generator)]
        return args

    def calculate_rewards_for_args(action, args, rewards):
        new_args = []
        for arg_group in args:
            new_arg_group = arg_group.generator.new(arg_group.args)
            new_args.append(ArgumentGroup(new_arg_group, arg_group.generator))
        new_reward, _, _ = env.step(action, transform_args(new_args))
        env.undo()
        rewards[new_reward] = new_args

    def improve_args(action, args, reward):
        rewards = {reward: args}
        attempts = imprvs["attempts"]
        improvements = imprvs["improvements_by_one_attempt"]
        for _ in range(attempts):
            for _ in range(improvements):
                calculate_rewards_for_args(action, args, rewards)
            args = rewards[max(rewards)]
            rewards = {max(rewards): args}
        perform_action_with_the_best_args(action, args)

    def perform_action_with_the_best_args(action, args):
        env.step(action, transform_args(args))
        if render:
            env.render()
        action_vector = [action]
        action_vector.extend(transform_args(args))
        if action != Environment.Action.TRIANGLE:
            action_vector.append(0)
        generated_actions[current_action] = action_vector

    start = time.time()
    env = Environment(image, None, None, actions, size)
    env.reset()
    seed = np.random.randint(0, 100)
    rng = np.random.RandomState(int(seed))
    position_generator = ScalingInitGenerator(imprvs["eps"], rng)
    color_generator = ColorPickerGenerator(imprvs["eps"], env.src_img.img, rng)
    generated_actions = np.zeros((actions, 11))
    current_action = 0
    done = False

    while not done:
        actions = env.action_space()
        action = np.random.choice(actions)
        args = generate_initial_arguments(action)
        reward, done, _ = env.step(action, transform_args(args))
        env.undo()
        if reward > 0:
            improve_args(action, args, reward)
            current_action += 1

    np.save(output_path, generated_actions)


def transform_args(args):
    result = ()
    for arg_group in args:
        for arg in arg_group.to_argument_values():
            result = result + (arg,)
    return result









