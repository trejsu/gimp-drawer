class Space(object):
    def __call__(self):
        raise NotImplementedError()

    def subspace(self, *args, **kwargs):
        raise NotImplementedError()

    def position(self):
        raise NotImplementedError()

    def color(self):
        raise NotImplementedError()


class ToolSpace(Space):
    def __init__(self):
        self.n = 3

    def __call__(self):
        return list(range(self.n))

    def subspace(self, i):
        if (i == 0) or (i == 1):
            return SelectionSpace()
        elif i == 2:
            return LineSpace()

    def color(self):
        return None

    def position(self):
        return None


class LineSpace(Space):
    def __call__(self):
        pass

    def subspace(self, i):
        return None

    def color(self):
        return [(0., 1.), (0., 1.), (0., 1.)]

    def position(self):
        return [(0., 1.), (0., 1.), (0., 1.), (0., 1.), (.1, 1.)]


class SelectionSpace(Space):
    def __call__(self):
        pass

    def subspace(self, i):
        return None

    def color(self):
        return [(0., 1.), (0., 1.), (0., 1.)]

    def position(self):
        return [(0., .9), (0., .9), (.1, 1.), (.1, 1.), (-1., 1.)]

