#!/usr/bin/python

import random

from gimpfu import *

from gimp_drawer.common.decorators.timed import timed
from gimp_drawer.environment.selection import Point, Selection


class Image(object):
    def __init__(self, image_id):
        super(Image, self).__init__()
        self.image = image_id
        self.drawable = pdb.gimp_image_active_drawable(self.image)
        pdb.gimp_context_set_brush("2. Hardness 100")
        pdb.gimp_context_set_sample_transparent(True)
        pdb.gimp_context_set_sample_merged(False)

    @timed
    def get_width(self):
        return self.drawable.width

    @timed
    def get_height(self):
        return self.drawable.height

    @timed
    def draw_brush_line(self, (red, green, blue, opacity, x1, y1, x2, y2, size)):
        change_foreground_color((red, green, blue))
        change_size(self.__from_normalized_size(size))
        points = self.__convert_points(Point(x1, y1), Point(x2, y2))
        self.__add_opacity_layer(opacity)
        pdb.gimp_paintbrush_default(self.drawable, len(points), points)
        self.__merge_layers()

    @timed
    def __from_normalized_size(self, size):
        return max(self.get_height(), self.get_width()) * size

    @timed
    def __merge_layers(self):
        pdb.gimp_image_merge_visible_layers(self.image, CLIP_TO_IMAGE)
        self.drawable = pdb.gimp_image_active_drawable(self.image)

    @timed
    def __add_opacity_layer(self, opacity):
        layer = gimp.Layer(self.image, "layer", self.get_width(),
                           self.get_height(), RGBA_IMAGE, self.__from_normalized_opacity(opacity), NORMAL_MODE)
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
    def draw_rectangle(self, (red, green, blue, opacity, x, y, width, height, angle)):
        change_foreground_color((red, green, blue))
        self.__add_opacity_layer(opacity)
        selection = Selection(self.image, Point(x, y), width, height)
        selection.select_rectangle()
        self.__fill_selection()
        self.__rotate_and_merge(angle, opacity)

    @timed
    def draw_ellipse(self, (red, green, blue, opacity, x, y, width, height, angle)):
        change_foreground_color((red, green, blue))
        opacity_layer = self.__add_opacity_layer(opacity)
        selection = Selection(self.image, Point(x, y), width, height)
        selection.select_ellipse()
        self.__fill_selection()
        self.__rotate_and_merge(angle, opacity, opacity_layer)

    @timed
    def __rotate_and_merge(self, angle, opacity, opacity_layer=None):
        self.__rotate(angle, opacity)
        if opacity_layer is not None:
            pdb.gimp_image_remove_layer(self.image, opacity_layer)
        self.__merge_layers()
        self.drawable = pdb.gimp_image_active_drawable(self.image)

    @timed
    def __rotate(self, normalized_angle, opacity):
        angle = self.__from_normalized_angle(normalized_angle)
        auto_center = True
        center_x = 0
        center_y = 0
        rotated_shape = pdb.gimp_item_transform_rotate(self.drawable,
                                                       angle,
                                                       auto_center,
                                                       center_x,
                                                       center_y)
        pdb.gimp_floating_sel_to_layer(rotated_shape)
        active_layer = pdb.gimp_image_get_active_layer(self.image)
        pdb.gimp_layer_set_opacity(active_layer, self.__from_normalized_opacity(opacity))

    @timed
    def __from_normalized_angle(self, angle):
        return angle * 180

    @timed
    def __from_normalized_opacity(self, opacity):
        return opacity * 100

    @timed
    def __random_angle(self):
        return random.randint(-180, 180)

    @timed
    def __fill_selection(self):
        pdb.gimp_edit_fill(self.drawable, FOREGROUND_FILL)

    @timed
    def __clear_selection(self):
        pdb.gimp_image_select_rectangle(self.image, CHANNEL_OP_REPLACE, 0,
                                        0, self.get_width(), self.get_height())

    @timed
    def draw_triangle(self, (red, green, blue, opacity, x1, y1, x2, y2, x3, y3)):
        change_foreground_color((red, green, blue))
        self.__add_opacity_layer(opacity)
        Selection(self.image).select_triangle(x1, y1, x2, y2, x3, y3)
        self.__fill_selection()
        self.__clear_selection()
        self.__merge_layers()


@timed
def perform_action(image_id, action, args):
    image = Image(image_id)
    actions = [
        lambda: image.draw_ellipse(args),
        lambda: image.draw_rectangle(args),
        lambda: image.draw_brush_line(args),
        lambda: image.draw_triangle(args)
    ]
    actions[action]()


@timed
def change_foreground_color(color):
    gimp.set_foreground(color)


@timed
def change_size(size):
    pdb.gimp_context_set_brush_size(size)



