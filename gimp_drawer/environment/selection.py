from gimpfu import *
from gimp_drawer.common.decorators.timed import timed
from gimp_drawer.common.figures import Point


class Selection(object):
    def __init__(self, image, top_left=None, width=None, height=None):
        self.image = image
        top_left = self.__from_normalized_point(top_left) if top_left is not None else None
        if top_left is not None:
            if top_left.x == self.image.width:
                top_left.x -= 1
            if top_left.y == self.image.height:
                top_left.y -= 1
        self.top_left = top_left
        self.width = self.__from_normalized_width(width, self.top_left.x) if width is not None else None
        self.height = self.__from_normalized_height(height, self.top_left.y) if height is not None else None

    @timed
    def select_rectangle(self):
        pdb.gimp_image_select_rectangle(self.image, CHANNEL_OP_REPLACE, self.top_left.x, self.top_left.y, self.width, self.height)

    @timed
    def select_ellipse(self):
        pdb.gimp_image_select_ellipse(self.image, CHANNEL_OP_REPLACE, self.top_left.x, self.top_left.y, self.width, self.height)

    @timed
    def __from_normalized_point(self, point):
        return Point(max(1, point.x * self.image.width), max(1, point.y * self.image.height))

    @timed
    def __from_normalized_width(self, width, boundary):
        return max(1, width * (self.image.width - boundary))

    @timed
    def __from_normalized_height(self, height, boundary):
        return max(1, height * (self.image.height - boundary))

    @timed
    def select_triangle(self, x1, y1, x2, y2, x3, y3):
        drawable = pdb.gimp_image_active_drawable(self.image)
        pdb.gimp_context_set_brush_size(1)
        point1, point2, point3 = self.__draw_triangle_edges(drawable, x1, x2, x3, y1, y2, y3)
        center = Point((point1.x + point2.x + point3.x) / 3, (point1.y + point2.y + point3.y) / 3)
        pdb.gimp_image_select_contiguous_color(self.image, CHANNEL_OP_REPLACE, drawable,
                                               center.x, center.y)

    @timed
    def __draw_triangle_edges(self, drawable, x1, x2, x3, y1, y2, y3):
        point1 = self.__from_normalized_point(Point(x1, y1))
        point2 = self.__from_normalized_point(Point(x2, y2))
        point3 = self.__from_normalized_point(Point(x3, y3))
        first_line = [point1.x, point1.y, point2.x, point2.y]
        second_line = [point3.x, point3.y, point2.x, point2.y]
        third_line = [point1.x, point1.y, point3.x, point3.y]
        pdb.gimp_pencil(drawable, len(first_line), first_line)
        pdb.gimp_pencil(drawable, len(second_line), second_line)
        pdb.gimp_pencil(drawable, len(third_line), third_line)
        return point1, point2, point3

    @timed
    def select_brush_line(self, x1, y1, x2, y2, size):
        point1 = self.__from_normalized_point(Point(x1, y1))
        point2 = self.__from_normalized_point(Point(x2, y2))
        drawable = pdb.gimp_image_active_drawable(self.image)
        size_to_change = max(drawable.height, drawable.width) * size
        pdb.gimp_context_set_brush_size(size_to_change)
        points = [point1.x, point1.y, point2.x, point2.y]
        pdb.gimp_paintbrush_default(drawable, len(points), points)
        center = Point((point1.x + point2.x) / 2, (point1.y + point2.y) / 2)
        pdb.gimp_image_select_contiguous_color(self.image, CHANNEL_OP_REPLACE, drawable, center.x,
                                               center.y)

