from gimpfu import *
from gimp_env import GimpEnv


def plugin_main(src_path):
    env = GimpEnv(src_path, 1000000)
    env.reset()

    done = False
    iteration = 0
    successful_iteration = 0

    while not done:
        state, reward, done, info = env.step(env.action_space.sample())
        if reward < 0:
            env.restore_state()
        else:
            successful_iteration += 1
            if successful_iteration % 10 == 0:
                env.render()
            if successful_iteration % 50 == 0:
                env.render_img()
        iteration += 1

    print "Environment solved after {} iterations".format(iteration)


register("agent", "", "", "", "", "", "", "", [(PF_STRING, "src_path", "Input", "")], [], plugin_main)

main()
