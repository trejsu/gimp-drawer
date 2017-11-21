#!/usr/bin/python

import random
from gimpfu import *
import time

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
        self.image_id = image_id
        pdb.gimp_context_set_brush("2. Hardness 075")

    def get_width(self):
        return self.__get_drawable().width

    def get_height(self):
        return self.__get_drawable().height

    def __get_drawable(self):
        return pdb.gimp_image_active_drawable(self.image_id)

    def draw_random_brush_line(self):
        self.__draw_brush_line(Point(), Point())

    def __draw_brush_line(self, start, end, color=None, size=None):
        change_foreground_color(color)
        # change_size(size)
        points = self.__convert_points(end, start)
        self.__add_opacity_layer()
        pdb.gimp_paintbrush_default(self.__get_drawable(), len(points), points)
        self.__merge_layers()

    def __merge_layers(self):
        pdb.gimp_image_merge_visible_layers(self.image_id, CLIP_TO_IMAGE)

    def __add_opacity_layer(self):
        layer = gimp.Layer(self.image_id, "layer", self.get_width(),
                           self.get_height(), RGBA_IMAGE,
                           self.__random_opacity(), NORMAL_MODE)
        self.image_id.add_layer(layer, 0)

    def __convert_points(self, end, start):
        start = self.__from_normalized_point(start)
        end = self.__from_normalized_point(end)
        points = [start.x, start.y, end.x, end.y]
        return points

    def __from_normalized_point(self, point):
        return Point(point.x * self.get_width(), point.y * self.get_height())

    def draw_random_pencil_line(self):
        self.__draw_pencil_line(Point(), Point())

    def __draw_pencil_line(self, start, end, color=None, size=None):
        change_foreground_color(color)
        # change_size(size)
        points = self.__convert_points(end, start)
        self.__add_opacity_layer()
        pdb.gimp_pencil(self.__get_drawable(), len(points), points)
        self.__merge_layers()

    def __select_rectangle(self, rectangle):
        height, top_left, width = self.__convert_selection(rectangle)
        pdb.gimp_image_select_rectangle(
            self.image_id, CHANNEL_OP_REPLACE, top_left.x,
            top_left.y, width, height
        )

    def __convert_selection(self, rectangle):
        top_left = self.__from_normalized_point(rectangle.top_left)
        width = self.__from_normalized_width(rectangle.width, top_left.x)
        height = self.__from_normalized_height(rectangle.height, top_left.y)
        return height, top_left, width

    def __from_normalized_width(self, width, boundary):
        return width * (self.get_width() - boundary)

    def __from_normalized_height(self, height, boundary):
        return height * (self.get_height() - boundary)

    def __select_ellipse(self, ellipse):
        height, top_left, width = self.__convert_selection(ellipse)
        pdb.gimp_image_select_ellipse(
            self.image_id, CHANNEL_OP_REPLACE, top_left.x,
            top_left.y, width, height
        )

    def draw_random_rectangle(self):
        self.__draw_rectangle(Selection(Point()))

    def __draw_rectangle(self, rectangle, color=None):
        change_foreground_color(color)
        self.__add_opacity_layer()
        self.__select_rectangle(rectangle)
        self.__fill_selection()
        self.__rotate_and_merge()
        # self.__clear_selection()

    def __rotate_and_merge(self):
        sel = pdb.gimp_item_transform_rotate(self.__get_drawable(), self.__random_angle(), True, 0, 0)
        # todo: why sometimes sel is not floating selection?
        if pdb.gimp_layer_is_floating_sel(sel):
            pdb.gimp_floating_sel_anchor(sel)
        self.__merge_layers()

    def __random_angle(self):
        return random.randint(-180, 180)

    def __fill_selection(self):
        pdb.gimp_edit_fill(self.__get_drawable(), FOREGROUND_FILL)

    def __random_opacity(self):
        return random.randint(25, 75)

    def draw_random_ellipse(self):
        self.__draw_ellipse(Selection(Point()))

    def __draw_ellipse(self, ellipse, color=None):
        change_foreground_color(color)
        self.__add_opacity_layer()
        self.__select_ellipse(ellipse)
        self.__fill_selection()
        self.__rotate_and_merge()

    def __clear_selection(self):
        pdb.gimp_image_select_rectangle(self.image_id, CHANNEL_OP_REPLACE, 0,
                                        0, self.get_width(), self.get_height())


def plugin_main(image_id, action):
    image = Image(image_id)
    actions = [
        lambda: image.draw_random_brush_line(),
        lambda: image.draw_random_ellipse(),
        lambda: image.draw_random_rectangle(),
        lambda: image.draw_random_pencil_line()
    ]
    actions[action]()


def change_foreground_color(color):
    gimp.set_foreground(randomize_color_if_none(color))


def randomize_color_if_none(color):
    return random_color() if color is None else color


def random_color():
    return random_byte(), random_byte(), random_byte()


def random_byte():
    return random.randint(0, 255)


def change_size(size):
    pdb.gimp_context_set_brush_size(randomize_size_if_none(size))


def randomize_size_if_none(size):
    return random_size() if size is None else size


def random_size():
    return random.randint(1, MAX_BRUSH_SIZE)


register("perform_action", "", "", "", "", "", "", "",
         [(PF_IMAGE, "image", "Image", ""), (PF_INT, "action", "Action", 0)],
         [], plugin_main)

main()
