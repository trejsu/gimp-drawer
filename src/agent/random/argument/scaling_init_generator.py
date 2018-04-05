from agent.random.argument.argument import Argument
from agent.random.argument.argument_generator import ArgumentGenerator
from common.timed import timed
from config import reducer_rate


class ScalingInitGenerator(ArgumentGenerator, object):
    def __init__(self, eps, rng):
        super(ScalingInitGenerator, self).__init__(eps, rng)

    @timed
    def init(self, ranges, time, space):
        args = ()
        for r in ranges:
            arg_min = r[0]
            arg_max = r[1]
            arg_value = self.rng.uniform(arg_min, arg_max)
            args = args + (Argument(arg_min, arg_max, arg_value),)
        reducer = int(time / 10) * reducer_rate
        scale = 1 - reducer
        scale_action = space.scale_action(scale)
        scale_action(args)
        return args