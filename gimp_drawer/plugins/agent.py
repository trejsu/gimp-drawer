import time
import tqdm

from gimpfu import *
from gimp_drawer.plugins.gimp_env import GimpEnv

START = time.time()


def plugin_main(src_path, iterations, acceptable_distance, mode):
    env = GimpEnv(src_path, acceptable_distance, mode)
    env.reset()

    if iterations is 0:
        run_until_done(env)
    else:
        run_finite_times(env, iterations)


def run_until_done(env):
    improvements = 0
    done = False
    while not done:
        done, improvements = execute_iteration(env, improvements)
    end = time.time()
    env.save(end - START)


def run_finite_times(env, iterations):
    improvements = 0
    for _ in tqdm.tqdm(range(iterations)):
        done, improvements = execute_iteration(env, improvements, improvements)
        if done:
            break
    env.save(improvements)


def execute_iteration(env, improvements, save_parameter=None):
    state, reward, done, info = env.step(env.action_space.sample())
    if reward < 0:
        env.restore_state()
    else:
        improvements += 1
        end = time.time()
        env.save(end - START, save_parameter)
        env.render()
    return done, improvements


register("agent", "", "", "", "", "", "", "",
         [
             (PF_STRING, "src_path", "Input", ""),
             (PF_INT, "iterations", "Iterations", 0),
             (PF_INT, "acceptable_distance", "Acceptable distance", 0),
             (PF_INT, "mode", "Mode", 0)
         ], [], plugin_main)

main()
