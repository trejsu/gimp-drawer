import getopt

import numpy as np

from model.conv_network import ConvNetwork
from gimpfu import *
from gimp_drawer.environment.test_model_environment import TestModelEnvironment
from model.dataset.data_set import DataSet


def plugin_main(model_path, tests_number):
    data = DataSet()
    conv_network = ConvNetwork(model_path)
    env = TestModelEnvironment(100)

    for i in range(tests_number):
        print "Test number %d" % (i + 1)
        x, y, label = data.test.random()
        args = conv_network.generate_args(x)
        args = fix_out_of_bounds_args(args)
        action = 0
        env.label_step(action, y)
        env.conv_step(action, args)
        env.render_with(str(label[0]))
        print "mse: %g" % conv_network.eval_error(x, y)
        raw_input("press Enter to continue...")
        env.reset()


def get_model_path(argv):
    model_path = None
    opts, args = getopt.getopt(argv, "m:")
    for opt, arg in opts:
        if opt == '-m':
            model_path = arg
    return model_path


def fix_out_of_bounds_args(args):
    upper_bound = [1., 1., 1., 1., 1., 1., 1., 1., 1.]
    lower_bound = [0., 0., 0., 0., 0., 0., 0., 0., -1.]
    args = np.minimum(args, upper_bound)
    args = np.maximum(args, lower_bound)
    return args


register("test_model", "", "", "", "", "", "", "",
         [
             (PF_STRING, "model_path", "path to the tested model", ""),
             (PF_INT, "tests_number", "number of tests to run", 20)
         ], [], plugin_main)

main()

# gimp -i -b '(python-fu-test-model RUN-NONINTERACTIVE "my-model-1700")' -b '(gimp-quit 1)'
