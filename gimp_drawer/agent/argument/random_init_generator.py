from gimp_drawer.agent.argument.argument import Argument
from gimp_drawer.agent.argument.argument_generator import ArgumentGenerator
from gimp_drawer.common.decorators.timed import timed


class RandomInitGenerator(ArgumentGenerator, object):
    def __init__(self, eps, rng):
        super(RandomInitGenerator, self).__init__(eps, rng)

    @timed
    def init(self, ranges):
        args = ()
        for r in ranges:
            arg_min = r[0]
            arg_max = r[1]
            arg_value = self.rng.uniform(arg_min, arg_max)
            args = args + (Argument(arg_min, arg_max, arg_value),)
        return args