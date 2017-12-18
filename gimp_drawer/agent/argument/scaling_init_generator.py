import random

from gimp_drawer.agent.argument.argument import Argument
from gimp_drawer.agent.argument.argument_generator import ArgumentGenerator
from gimp_drawer.common.decorators.timed import timed
from gimp_drawer.config import reducer_rate


class ScalingInitGenerator(ArgumentGenerator, object):
    def __init__(self, eps):
        super(ScalingInitGenerator, self).__init__(eps)

    @timed
    def init(self, ranges, time, space):
        args = ()
        for r in ranges:
            arg_min = r[0]
            arg_max = r[1]
            arg_value = random.uniform(arg_min, arg_max)
            args = args + (Argument(arg_min, arg_max, arg_value),)
        reducer = int(time / 10) * reducer_rate
        scale = 1 - reducer
        scale_action = space.scale_action(scale)
        scale_action(args)
        return args