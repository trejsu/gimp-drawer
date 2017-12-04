import random

import numpy as np

from gimp_drawer.argument.argument import Argument
from gimp_drawer.common.decorators.timed import timed


class ArgumentGenerator(object):
    @timed
    def new(self, args):
        new_arg_group = ()
        for arg in args:
            new_arg_value = self._new_arg(arg)
            new_arg_group = new_arg_group + (Argument(arg.min, arg.max, new_arg_value),)
        return new_arg_group

    def _new_arg(self, arg):
        pass


class PositionGenerator(ArgumentGenerator):
    def __init__(self, eps):
        self.eps = eps

    @timed
    def _new_arg(self, arg):
        random_arg = np.random.normal(arg.value, self.eps * (arg.max - arg.min))
        return min(arg.max, max(arg.min, random_arg))

    @timed
    def init(self, ranges):
        args = ()
        for r in ranges:
            arg_min = r[0]
            arg_max = r[1]
            arg_value = random.uniform(arg_min, arg_max)
            args = args + (Argument(arg_min, arg_max, arg_value),)
        return args


class ColorGenerator(ArgumentGenerator):
    def __init__(self, eps):
        self.eps = eps

    # will be different from position one soon
    @timed
    def _new_arg(self, arg):
        random_arg = np.random.normal(arg.value, self.eps * (arg.max - arg.min))
        return min(arg.max, max(arg.min, random_arg))

    # will be different from position one soon
    @timed
    def init(self, ranges):
        args = ()
        for r in ranges:
            arg_min = r[0]
            arg_max = r[1]
            arg_value = random.uniform(arg_min, arg_max)
            args = args + (Argument(arg_min, arg_max, arg_value),)
        return args
