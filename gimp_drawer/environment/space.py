from gimp_drawer.environment.selection import Selection, Point
from gimpfu import *


class ToolSpace(object):
    def __init__(self):
        self.n = 4

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
        elif i == 3:
            return TriangleSpace()


class Space(object):
    def position(self):
        raise NotImplementedError()

    def color(self):
        return [(0., 1.), (0., 1.), (0., 1.)]

    def action_to_create_selection_on_given_image(self, image):
        raise NotImplementedError()


class LineSpace(Space):
    def action_to_create_selection_on_given_image(self, image):
        return lambda (x1, y1, x2, y2, size): 0

    def position(self):
        return [(0., 1.), (0., 1.), (0., 1.), (0., 1.), (.1, 1.)]


class SelectionSpace(Space):
    def action_to_create_selection_on_given_image(self, image):
        raise NotImplementedError()

    def position(self):
        return [(0., .9), (0., .9), (.1, 1.), (.1, 1.), (-1., 1.)]


class TriangleSpace(Space):
    def position(self):
        return [(0., 1.), (0., 1.), (0., 1.), (0., 1.), (0., 1.), (0., 1.)]

    def action_to_create_selection_on_given_image(self, image):
        # todo: remove logic from here
        def create_selection((x1, y1, x2, y2, x3, y3)):
            drawable = pdb.gimp_image_active_drawable(image)
            layer = gimp.Layer(image, "layer", drawable.width, drawable.height, RGBA_IMAGE, 100, NORMAL_MODE)
            position = 0
            image.add_layer(layer, position)
            Selection(image).select_triangle(x1.value, y1.value, x2.value, y2.value, x3.value, y3.value)
            image.remove_layer(layer)

        return create_selection


class RectangleSelectionSpace(SelectionSpace):
    def action_to_create_selection_on_given_image(self, image):
        return lambda (x, y, width, height, angle): Selection(image, Point(x.value, y.value), width.value, height.value).select_rectangle()


class EllipseSelectionSpace(SelectionSpace):
    def action_to_create_selection_on_given_image(self, image):
        return lambda (x, y, width, height, angle): Selection(image, Point(x.value, y.value), width.value, height.value).select_ellipse()