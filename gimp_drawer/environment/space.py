from gimp_drawer.environment.selection import Selection
from gimp_drawer.common.figures import Point, Line, Triangle
from gimpfu import *
from gimp_drawer.common.decorators.timed import timed


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

    @staticmethod
    def subspace_name(i):
        if i == 0:
            return "ellipse"
        elif i == 1:
            return "rectangle"
        elif i == 2:
            return "brush"
        elif i == 3:
            return "triangle"


class Space(object):
    def position(self):
        raise NotImplementedError()

    def color(self):
        return [(0., 1.), (0., 1.), (0., 1.), (0., 1.)]

    def create_selection_action(self, image):
        raise NotImplementedError()

    def scale_action(self, scale):
        raise NotImplementedError()


class LineSpace(Space):
    def scale_action(self, scale):
        # todo: remove logic from here
        @timed
        def scale_shape((x1, y1, x2, y2, size)):
            scaled_line = Line(Point(x1.value, y1.value), Point(x2.value, y2.value)).scale(scale)
            x1.value = scaled_line.start.x
            y1.value = scaled_line.start.y
            x2.value = scaled_line.end.x
            y2.value = scaled_line.end.y
            size.value = size.value * scale

        return scale_shape

    def position(self):
        return [(0., 1.), (0., 1.), (0., 1.), (0., 1.), (0., 1.)]

    def create_selection_action(self, image):
        # todo: remove logic from here
        @timed
        def create_selection((x1, y1, x2, y2, size)):
            drawable = pdb.gimp_image_active_drawable(image)
            layer = gimp.Layer(image, "layer", drawable.width, drawable.height, RGBA_IMAGE, 100, NORMAL_MODE)
            position = 0
            image.add_layer(layer, position)
            Selection(image).select_brush_line(x1.value, y1.value, x2.value, y2.value, size.value)
            image.remove_layer(layer)

        return create_selection


class SelectionSpace(Space):
    def scale_action(self, scale):
        # todo: remove logic from her
        @timed
        def scale_shape((x, y, width, height, angle)):
            width.value = width.value * scale
            height.value = height.value * scale

        return scale_shape

    def create_selection_action(self, image):
        raise NotImplementedError()

    def position(self):
        return [(0., 1.), (0., 1.), (0., 1.), (0., 1.), (0., 1.)]


class TriangleSpace(Space):
    def scale_action(self, scale):
        # todo: remove logic from here
        @timed
        def scale_shape((x1, y1, x2, y2, x3, y3)):
            scaled_triangle = Triangle(Point(x1.value, y1.value), Point(x2.value, y2.value), Point(x3.value, y3.value)).scale(scale)
            x1.value = scaled_triangle.a.x
            y1.value = scaled_triangle.a.y
            x2.value = scaled_triangle.b.x
            y2.value = scaled_triangle.b.y
            x3.value = scaled_triangle.c.x
            y3.value = scaled_triangle.c.y

        return scale_shape

    def position(self):
        return [(0., 1.), (0., 1.), (0., 1.), (0., 1.), (0., 1.), (0., 1.)]

    def create_selection_action(self, image):
        # todo: remove logic from here
        @timed
        def create_selection((x1, y1, x2, y2, x3, y3)):
            drawable = pdb.gimp_image_active_drawable(image)
            layer = gimp.Layer(image, "layer", drawable.width, drawable.height, RGBA_IMAGE, 100, NORMAL_MODE)
            position = 0
            image.add_layer(layer, position)
            Selection(image).select_triangle(x1.value, y1.value, x2.value, y2.value, x3.value, y3.value)
            image.remove_layer(layer)

        return create_selection


class RectangleSelectionSpace(SelectionSpace):
    def create_selection_action(self, image):
        @timed
        def create_selection((x, y, width, height, angle)):
            Selection(image, Point(x.value, y.value), width.value, height.value).select_rectangle()

        return create_selection


class EllipseSelectionSpace(SelectionSpace):
    def create_selection_action(self, image):
        @timed
        def create_selection((x, y, width, height, angle)):
            Selection(image, Point(x.value, y.value), width.value, height.value).select_ellipse()

        return create_selection
