class Space(object):
    def __call__(self):
        raise NotImplementedError()

    def subspace(self, *args, **kwargs):
        raise NotImplementedError()


class SelectionSpace(Space):
    def __init__(self):
        self.n = 8

    def __call__(self):
        return [(0., .9), (0., .9), (.1, 1.), (.1, 1.), (-1., 1.), (0., 1.), (0., 1.),
                          (0., 1.)]

    def subspace(self, i):
        return None


class ToolSpace(Space):
    def __init__(self):
        self.n = 3

    def __call__(self):
        return list(range(self.n))

    def subspace(self, i):
        if (i == 0) or (i == 1):
            return SelectionSpace()
        elif (i == 2) or (i == 3):
            return LineSpace()


class LineSpace(Space):
    def __init__(self):
        self.n = 8

    def __call__(self):
        return [(0., 1.), (0., 1.), (0., 1.), (0., 1.), (0., 1.), (0., 1.), (0., 1.), (.1, 1.)]

    def subspace(self, i):
        return None
