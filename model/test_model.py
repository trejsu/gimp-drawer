import getopt

import numpy as np

from model.conv_network import ConvNetwork
from gimpfu import *
from gimp_drawer.environment.test_model_environment import TestModelEnvironment


def read_test_set(data_dir):
    X = np.load(data_dir + "/test_X.npy", mmap_mode="r")
    Y = np.load(data_dir + "/test_Y.npy", mmap_mode="r")
    labels = np.load(data_dir + "/test_labels.npy", mmap_mode="r")
    return {
        "X": X,
        "Y": Y,
        "labels": labels
    }


def plugin_main(model_path):
    data_dir = "data/1125"
    data = read_test_set(data_dir)
    conv_network = ConvNetwork(model_path)
    env = TestModelEnvironment(100)

    for i in range(20):
        print "Test number %d" % (i + 1)
        index = np.random.randint(0, 22019)
        X = data["X"][index]
        Y = data["Y"][index]
        label = data["labels"][index]
        args = conv_network.generate_args(X)
        action = 0
        env.label_step(action, Y)
        env.conv_step(action, args)
        env.render_with(str(label[0]))
        print "mse: %g" % conv_network.eval_error(X, Y)
        raw_input("press Enter to continue...")
        env.reset()


def get_model_path(argv):
    model_path = None
    opts, args = getopt.getopt(argv, "m:")
    for opt, arg in opts:
        if opt == '-m':
            model_path = arg
    return model_path


register("test_model", "", "", "", "", "", "", "",
         [
             (PF_STRING, "model_path", "Path to the trained model", ""),
         ], [], plugin_main)

main()

# gimp -i -b '(python-fu-test-model RUN-NONINTERACTIVE "my-model-1700")' -b '(gimp-quit 1)'
