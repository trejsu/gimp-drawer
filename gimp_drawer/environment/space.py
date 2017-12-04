from gimp_drawer.environment.selection import Selection, Point


class ToolSpace(object):
    def __init__(self):
        self.n = 2

    def __call__(self):
        return list(range(self.n))

    @staticmethod
    def subspace(i):
        if i == 0:
            return EllipseSelectionSpace()
        elif i == 1:
            return RectangleSelectionSpace()
        elif i == 2:
            return LineSpace()


class Space(object):
    def position(self):
        raise NotImplementedError()

    def color(self):
        raise NotImplementedError()

    def action_to_create_selection_on_given_image(self, image):
        raise NotImplementedError()


class LineSpace(Space):
    def action_to_create_selection_on_given_image(self, image):
        pass

    def color(self):
        return [(0., 1.), (0., 1.), (0., 1.)]

    def position(self):
        return [(0., 1.), (0., 1.), (0., 1.), (0., 1.), (.1, 1.)]


class SelectionSpace(Space):
    def action_to_create_selection_on_given_image(self, image):
        raise NotImplementedError()

    def color(self):
        return [(0., 1.), (0., 1.), (0., 1.)]

    def position(self):
        return [(0., .9), (0., .9), (.1, 1.), (.1, 1.), (-1., 1.)]


class RectangleSelectionSpace(SelectionSpace):
    def action_to_create_selection_on_given_image(self, image):
        return lambda (x, y, width, height, angle): Selection(image, Point(x.value, y.value), width.value, height.value).select_rectangle()


class EllipseSelectionSpace(SelectionSpace):
    def action_to_create_selection_on_given_image(self, image):
        return lambda (x, y, width, height, angle): Selection(image, Point(x.value, y.value), width.value, height.value).select_ellipse()