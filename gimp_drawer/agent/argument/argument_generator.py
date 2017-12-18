from gimp_drawer.agent.argument.argument import Argument
from gimp_drawer.common.decorators.timed import timed


class ArgumentGenerator(object):
    def __init__(self, eps, rng):
        self.eps = eps
        self.rng = rng

    @timed
    def new(self, args):
        new_arg_group = ()
        for arg in args:
            new_arg_value = self._new_arg(arg)
            new_arg_group = new_arg_group + (Argument(arg.min, arg.max, new_arg_value),)
        return new_arg_group

    @timed
    def _new_arg(self, arg):
        random_arg = self.rng.normal(arg.value, self.eps * (arg.max - arg.min))
        return min(arg.max, max(arg.min, random_arg))

    def init(self, *args):
        pass

