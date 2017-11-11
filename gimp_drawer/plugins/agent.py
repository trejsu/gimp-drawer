from gimpfu import *
from gimp_env import GimpEnv
import tqdm
import time

START = 0


def plugin_main(src_path, iterations, acceptable_distance):
    env = GimpEnv(src_path, acceptable_distance)
    env.reset()

    if iterations is 0:
        run_until_done(env)
    else:
        run_finite_times(env, iterations)


def run_until_done(env):
    global START
    START = time.time()
    successful_iteration = 0
    done = False
    while not done:
        done, successful_iteration = execute_iteration(env, successful_iteration)
    end = time.time()
    env.save(end - START)


def run_finite_times(env, iterations):
    successful_iteration = 0
    for _ in tqdm.tqdm(range(iterations)):
        done, successful_iteration = execute_iteration(env, successful_iteration, successful_iteration)
        if done:
            break
    env.save(successful_iteration)


def execute_iteration(env, successful_iteration, save_parameter=None):
    state, reward, done, info = env.step(env.action_space.sample())
    if reward < 0:
        env.restore_state()
    else:
        successful_iteration += 1
        if successful_iteration % 50 == 0:
            env.render_img()
        end = time.time()
        env.save(end - START)
    return done, successful_iteration


register("agent", "", "", "", "", "", "", "",
         [
             (PF_STRING, "src_path", "Input", ""),
             (PF_INT, "iterations", "Iterations", 0),
             (PF_INT, "acceptable_distance", "Acceptable distance", 0)
         ], [], plugin_main)

main()
