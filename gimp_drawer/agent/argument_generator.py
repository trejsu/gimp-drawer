import random

import numpy as np
from gimpfu import pdb, HISTOGRAM_RED, HISTOGRAM_GREEN, HISTOGRAM_BLUE

from gimp_drawer.agent.argument import Argument
from gimp_drawer.common.decorators.timed import timed
from gimp_drawer.config import reducer_rate


class ArgumentGenerator(object):
    def __init__(self, eps):
        self.eps = eps

    @timed
    def new(self, args):
        new_arg_group = ()
        for arg in args:
            new_arg_value = self._new_arg(arg)
            new_arg_group = new_arg_group + (Argument(arg.min, arg.max, new_arg_value),)
        return new_arg_group

    @timed
    def _new_arg(self, arg):
        random_arg = np.random.normal(arg.value, self.eps * (arg.max - arg.min))
        return min(arg.max, max(arg.min, random_arg))

    def init(self, *args):
        pass


class RandomInitGenerator(ArgumentGenerator, object):
    def __init__(self, eps):
        super(RandomInitGenerator, self).__init__(eps)

    @timed
    def init(self, ranges):
        args = ()
        for r in ranges:
            arg_min = r[0]
            arg_max = r[1]
            arg_value = random.uniform(arg_min, arg_max)
            args = args + (Argument(arg_min, arg_max, arg_value),)
        return args


class ColorPickerGenerator(ArgumentGenerator, object):
    def __init__(self, eps, src_image):
        super(ColorPickerGenerator, self).__init__(eps)
        self.src_image = src_image

    @timed
    def init(self, ranges, position, size, space):
        select_action = space.create_selection_action(self.src_image)
        select_action(position, size)
        drawable = pdb.gimp_image_get_active_drawable(self.src_image)
        red = pdb.gimp_histogram(drawable, HISTOGRAM_RED, 0, 255)[0] / 255
        green = pdb.gimp_histogram(drawable, HISTOGRAM_GREEN, 0, 255)[0] / 255
        blue = pdb.gimp_histogram(drawable, HISTOGRAM_BLUE, 0, 255)[0] / 255
        # todo: think about this 100 opacity, is it a good idea?
        return Argument(0, 1, red), Argument(0, 1, green), Argument(0, 1, blue), Argument(0, 1, 0.8)


class SmallerInTimeInitGenerator(ArgumentGenerator, object):
    def __init__(self, eps):
        super(SmallerInTimeInitGenerator, self).__init__(eps)

    @timed
    def init(self, ranges, time):
        arg_reducer = (time / 10) * reducer_rate
        args = ()
        for r in ranges:
            arg_min = r[0]
            arg_max = r[1] - arg_reducer
            arg_value = random.uniform(arg_min, arg_max)
            args = args + (Argument(arg_min, arg_max, arg_value),)
        return args
