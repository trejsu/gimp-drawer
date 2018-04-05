from common.timed import timed


class Argument(object):
    def __init__(self, arg_min, arg_max, value):
        self.min = arg_min
        self.max = arg_max
        self.value = value


class ArgumentGroup(object):
    def __init__(self, args, generator):
        self.args = args
        self.generator = generator

    @timed
    def to_argument_values(self):
        return [a.value for a in self.args]
