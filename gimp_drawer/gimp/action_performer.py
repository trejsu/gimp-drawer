#!/usr/bin/python

import random

from gimpfu import *

from gimp_drawer.decorators.timed import timed

MIN_SELECTION_SIZE = 0.0001
MAX_BRUSH_SIZE = 1/5.


class Point(object):
    def __init__(self, x=None, y=None):
        super(Point, self).__init__()
        self.x = random.random() if x is None else x
        self.y = random.random() if y is None else y

    def __str__(self):
        return str("(" + str(self.x) + "," + str(self.y) + ")")


class Selection(object):
    def __init__(self, top_left, width=None, height=None):
        super(Selection, self).__init__()
        self.top_left = top_left
        self.width = random.random() if width is None else width
        self.height = random.random() if height is None else height

    def __str__(self):
        return str(str(self.top_left) + " " + str(self.width) + "x" + str(self.height))


class Image(object):
    def __init__(self, image_id):
        super(Image, self).__init__()
        self.image = image_id
        pdb.gimp_context_set_brush("2. Hardness 075")
        self.drawable = pdb.gimp_image_active_drawable(self.image)

    @timed
    def get_width(self):
        return self.drawable.width

    @timed
    def get_height(self):
        return self.drawable.height

    @timed
    def draw_brush_line(self, (x1, y1, x2, y2, red, green, blue)):
        change_foreground_color((red, green, blue))
        # change_size(size)
        points = self.__convert_points(Point(x1, y1), Point(x2, y2))
        self.__add_opacity_layer()
        pdb.gimp_paintbrush_default(self.drawable, len(points), points)
        self.__merge_layers()

    @timed
    def __merge_layers(self):
        pdb.gimp_image_merge_visible_layers(self.image, CLIP_TO_IMAGE)
        self.drawable = pdb.gimp_image_active_drawable(self.image)

    @timed
    def __add_opacity_layer(self):
        layer = gimp.Layer(self.image, "layer", self.get_width(),
                           self.get_height(), RGBA_IMAGE,
                           self.__random_opacity(), NORMAL_MODE)
        position = 0
        self.image.add_layer(layer, position)
        self.drawable = pdb.gimp_image_active_drawable(self.image)
        return layer

    @timed
    def __convert_points(self, end, start):
        start = self.__from_normalized_point(start)
        end = self.__from_normalized_point(end)
        points = [start.x, start.y, end.x, end.y]
        return points

    @timed
    def __from_normalized_point(self, point):
        return Point(point.x * self.get_width(), point.y * self.get_height())

    @timed
    def draw_pencil_line(self, (x1, y1, x2, y2, red, green, blue)):
        change_foreground_color((red, green, blue))
        # change_size(size)
        points = self.__convert_points(Point(x1, y1), Point(x2, y2))
        self.__add_opacity_layer()
        pdb.gimp_pencil(self.drawable, len(points), points)
        self.__merge_layers()

    @timed
    def __select_rectangle(self, rectangle):
        height, top_left, width = self.__convert_selection(rectangle)
        pdb.gimp_image_select_rectangle(
            self.image, CHANNEL_OP_REPLACE, top_left.x,
            top_left.y, width, height
        )

    @timed
    def __convert_selection(self, rectangle):
        top_left = self.__from_normalized_point(rectangle.top_left)
        width = self.__from_normalized_width(rectangle.width, top_left.x)
        height = self.__from_normalized_height(rectangle.height, top_left.y)
        return height, top_left, width

    @timed
    def __from_normalized_width(self, width, boundary):
        return width * (self.get_width() - boundary)

    @timed
    def __from_normalized_height(self, height, boundary):
        return height * (self.get_height() - boundary)

    @timed
    def __select_ellipse(self, ellipse):
        height, top_left, width = self.__convert_selection(ellipse)
        pdb.gimp_image_select_ellipse(
            self.image, CHANNEL_OP_REPLACE, top_left.x,
            top_left.y, width, height
        )

    @timed
    def draw_rectangle(self, (x, y, width, height, angle, red, green, blue)):
        change_foreground_color((red, green, blue))
        self.__add_opacity_layer()
        self.__select_rectangle(Selection(Point(x, y), width, height))
        self.__fill_selection()
        self.__rotate_and_merge(angle)

    @timed
    def draw_ellipse(self, (x, y, width, height, angle, red, green, blue)):
        change_foreground_color((red, green, blue))
        opacity_layer = self.__add_opacity_layer()
        self.__select_ellipse(Selection(Point(x, y), width, height))
        self.__fill_selection()
        self.__rotate_and_merge(angle, opacity_layer)

    @timed
    def __rotate_and_merge(self, angle, opacity_layer=None):
        self.__rotate(angle)
        if opacity_layer is not None:
            pdb.gimp_image_remove_layer(self.image, opacity_layer)
        self.__merge_layers()
        self.drawable = pdb.gimp_image_active_drawable(self.image)

    @timed
    def __rotate(self, normalized_angle):
        angle = self.__from_normalized_angle(normalized_angle)
        auto_center = True
        center_x = 0
        center_y = 0
        pdb.gimp_floating_sel_to_layer(pdb.gimp_item_transform_rotate(self.drawable, angle, auto_center, center_x, center_y))
        pdb.gimp_layer_set_opacity(pdb.gimp_image_get_active_layer(self.image), self.__random_opacity())

    @timed
    def __from_normalized_angle(self, angle):
        return angle * 180

    @timed
    def __random_angle(self):
        return random.randint(-180, 180)

    @timed
    def __fill_selection(self):
        pdb.gimp_edit_fill(self.drawable, FOREGROUND_FILL)

    @timed
    # todo: add opacity as arg
    def __random_opacity(self):
        return 75.

    @timed
    def __clear_selection(self):
        pdb.gimp_image_select_rectangle(self.image, CHANNEL_OP_REPLACE, x=0,
                                        y=0, width=self.get_width(), height=self.get_height())


@timed
def perform_action(image_id, action, args):
    image = Image(image_id)
    actions = [
        lambda: image.draw_ellipse(args),
        lambda: image.draw_rectangle(args),
        lambda: image.draw_brush_line(args),
        lambda: image.draw_pencil_line(args)
    ]
    actions[action]()


@timed
def change_foreground_color(color):
    gimp.set_foreground(randomize_color_if_none(color))


@timed
def randomize_color_if_none(color):
    return random_color() if color is None else color


@timed
def random_color():
    return random_byte(), random_byte(), random_byte()


@timed
def random_byte():
    return random.randint(0, 255)


@timed
def change_size(size):
    pdb.gimp_context_set_brush_size(randomize_size_if_none(size))


@timed
def randomize_size_if_none(size):
    return random_size() if size is None else size


@timed
def random_size():
    return random.randint(1, MAX_BRUSH_SIZE)
