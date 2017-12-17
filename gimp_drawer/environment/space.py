from gimp_drawer.environment.selection import Selection, Point
from gimpfu import *


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

    def size(self):
        raise NotImplementedError()

    def color(self):
        return [(0., 1.), (0., 1.), (0., 1.), (0., 1.)]

    def create_selection_action(self, image):
        raise NotImplementedError()

    def create_pixel_rgn_action(self, image):
        raise NotImplementedError()


class LineSpace(Space):
    def size(self):
        pass

    def create_pixel_rgn_action(self, image):
        # todo: remove logic from here
        # todo: adjust arguments for position and size
        def create_pixel_rgn((x1, y1, x2, y2, size)):
            pixel_rgn = None
            drawable = pdb.gimp_image_active_drawable(image)
            width = x2 - x1
            height = y2 - y1
            pdb.gimp_pixel_rgn_init(pixel_rgn, drawable, x1, y1, width, height, 0, 0)
            return pixel_rgn

        return create_pixel_rgn

    def position(self):
        return [(0., 1.), (0., 1.), (0., 1.), (0., 1.), (0., 1.)]

    def create_selection_action(self, image):
        # todo: remove logic from here
        # todo: adjust arguments for position and size
        def create_selection((x1, y1, x2, y2, size)):
            drawable = pdb.gimp_image_active_drawable(image)
            layer = gimp.Layer(image, "layer", drawable.width, drawable.height, RGBA_IMAGE, 100, NORMAL_MODE)
            position = 0
            image.add_layer(layer, position)
            Selection(image).select_brush_line(x1.value, y1.value, x2.value, y2.value, size.value)
            image.remove_layer(layer)

        return create_selection


class SelectionSpace(Space):
    def size(self):
        return [(0., 1.), (0., 1.)]

    def create_pixel_rgn_action(self, image):
        # todo: remove logic from her
        def create_pixel_rgn((x, y, angle), (width, height)):
            pixel_rgn = None
            drawable = pdb.gimp_image_active_drawable(image)
            pdb.gimp_pixel_rgn_init(pixel_rgn, drawable, x, y, width, height, 0, 0)
            return pixel_rgn

        return create_pixel_rgn

    def create_selection_action(self, image):
        raise NotImplementedError()

    def position(self):
        return [(0., 1.), (0., 1.), (-1., 1.)]


class TriangleSpace(Space):
    def size(self):
        pass

    def create_pixel_rgn_action(self, image):
        # todo: remove logic from here
        # todo: adjust arguments for position and size
        def create_pixel_rgn((x1, y1, x2, y2, x3, y3)):
            pixel_rgn = None
            drawable = pdb.gimp_image_active_drawable(image)
            x = min(x1, x2, x3)
            y = min(y1, y2, y3)
            width = max(x1, x2, x3) - x
            height = max(y1, y2, y3) - y
            pdb.gimp_pixel_rgn_init(pixel_rgn, drawable, x, y, width, height, 0, 0)
            return pixel_rgn

        return create_pixel_rgn

    def position(self):
        return [(0., 1.), (0., 1.), (0., 1.), (0., 1.), (0., 1.), (0., 1.)]

    def create_selection_action(self, image):
        # todo: remove logic from here
        # todo: adjust arguments for position and size
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
        return lambda (x, y, angle), (width, height): Selection(image, Point(x.value, y.value), width.value, height.value).select_rectangle()


class EllipseSelectionSpace(SelectionSpace):
    def create_selection_action(self, image):
        return lambda (x, y, angle), (width, height): Selection(image, Point(x.value, y.value), width.value, height.value).select_ellipse()