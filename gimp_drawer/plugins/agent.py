import random
import time

import numpy as np
from gimpfu import *

from gimp_drawer.config import improvements as imprvs
from gimp_drawer.decorators.timed import timed, print_result
from gimp_drawer.gimp.environment import Environment

START = time.time()
DEFAULT_RENDER = 0
NO_RENDER = 1
RENDER_EVERYTHING = 2
RENDER_MODE = 0


def plugin_main(src_path, acceptable_distance, mode, render_mode):
    global RENDER_MODE
    RENDER_MODE = render_mode
    env = Environment(src_path, acceptable_distance, mode)
    env.reset()
    run_until_done(env)
    print_result()


def run_until_done(env):
    done = False
    while not done:
        done = execute_iteration(env)
    end = time.time()
    env.save(end - START)


def execute_iteration(env):
    actions = env.action_space()
    action = random.choice(actions)
    subspace = env.action_space.subspace(action)
    ranges = subspace()

    args = generate_initial_args(ranges)
    reward, done = env.step(action, tuple(map(lambda a: a.value, args)))
    env.undo()

    if reward > 0:
        improve_args(args, reward, env, action)

    return done


@timed
def generate_initial_args(ranges):
    args = ()
    for r in ranges:
        arg_min = r[0]
        arg_max = r[1]
        arg_value = random.uniform(arg_min, arg_max)
        args = args + (Argument(arg_min, arg_max, arg_value),)
    return args


@timed
def improve_args(args, reward, env, action):
    modified_args_with_rewards = {reward: args}

    for _ in range(imprvs["attempts"]):
        find_similar_shapes(args, env, action, modified_args_with_rewards)
        args = modified_args_with_rewards[max(modified_args_with_rewards)]
        reward, done = env.step(action, tuple(map(lambda a: a.value, args)))
        if render_everything():
            env.render()
        env.undo()
        modified_args_with_rewards = {reward: args}
    env.step(action, tuple(map(lambda a: a.value, args)))
    if render_default():
        env.render()
    end = time.time()
    env.save(end - START)


@timed
def find_similar_shapes(args, env, action, modified_args_with_rewards):
    for _ in range(imprvs["improvements_by_one_attempt"]):
        new_args = calculate_new_args(args)
        new_reward, _ = env.step(action, tuple(map(lambda a: a.value, new_args)))
        if render_everything():
            env.render()
        env.undo()
        modified_args_with_rewards[new_reward] = new_args


@timed
def calculate_new_args(old_args):
    new_args = ()
    for arg in old_args:
        random_arg = np.random.normal(arg.value, imprvs["eps"] * (arg.max - arg.min))
        new_arg_value = min(arg.max, max(arg.min, random_arg))
        new_args = new_args + (Argument(arg.min, arg.max, new_arg_value),)
    return new_args


def render_everything():
    return RENDER_MODE == RENDER_EVERYTHING


def render_default():
    return RENDER_MODE == RENDER_EVERYTHING or RENDER_MODE == DEFAULT_RENDER


class Argument(object):
    def __init__(self, arg_min, arg_max, value):
        self.min = arg_min
        self.max = arg_max
        self.value = value


register("agent", "", "", "", "", "", "", "",
         [
             (PF_STRING, "src_path", "Input", ""),
             (PF_INT, "acceptable_distance", "Acceptable distance", 0),
             (PF_INT, "mode", "Mode", 0),
             (PF_INT, "render_mode", "Render mode", 0)
         ], [], plugin_main)

main()
