#!/usr/bin/python

from gimpfu import *
import random

WIDTH = None
HEIGHT = None


class Point(object):
    def __init__(self, x=None, y=None):
        super(Point, self).__init__()
        self.x = random.randint(0, WIDTH) if x is None else x
        self.y = random.randint(0, HEIGHT) if y is None else y


class Selection(object):
    def __init__(self, top_left_point, width=None, height=None):
        super(Selection, self).__init__()
        self.top_left_point = top_left_point
        self.width = \
            random.randint(1, self.__validate(WIDTH - self.top_left_point.x)) if width is None else width
        self.height = \
            random.randint(1, self.__validate(HEIGHT - self.top_left_point.y)) if height is None else height

    @staticmethod
    def __validate(points_left):
        return points_left if points_left > 0 else 1


class Image(object):
    def __init__(self, image_id):
        super(Image, self).__init__()
        self.image_id = image_id

    def get_width(self):
        return self.__get_drawable().width

    def get_height(self):
        return self.__get_drawable().height

    def __get_drawable(self):
        return pdb.gimp_image_active_drawable(self.image_id)

    def draw_random_brush_line(self):
        self.__draw_brush_line(Point(), Point())

    def __draw_brush_line(self, start, end, color=None):
        change_foreground_color(color)
        control_points = [start.x, start.y, end.x, end.y]
        pdb.gimp_paintbrush_default(self.__get_drawable(), len(control_points), control_points)

    def draw_random_pencil_line(self):
        self.__draw_pencil_line(Point(), Point())

    def __draw_pencil_line(self, start, end, color=None):
        change_foreground_color(color)
        control_points = [start.x, start.y, end.x, end.y]
        pdb.gimp_pencil(self.__get_drawable(), len(control_points), control_points)

    def draw_random_rectangle(self):
        self.__draw_rectangle(Selection(Point()))

    def __draw_rectangle(self, rectangle, color=None):
        change_foreground_color(color)
        self.__select_rectangle(rectangle)
        self.__stroke_selection()

    def __select_rectangle(self, rectangle):
        pdb.gimp_image_select_rectangle(
            self.image_id,
            CHANNEL_OP_REPLACE,
            rectangle.top_left_point.x,
            rectangle.top_left_point.y,
            rectangle.width,
            rectangle.height
        )

    def __stroke_selection(self):
        pdb.gimp_edit_stroke(self.__get_drawable())

    def draw_random_ellipse(self):
        self.__draw_ellipse(Selection(Point()))

    def __draw_ellipse(self, ellipse, color=None):
        change_foreground_color(color)
        self.__select_ellipse(ellipse)
        self.__stroke_selection()

    def __select_ellipse(self, ellipse):
        pdb.gimp_image_select_ellipse(
            self.image_id,
            CHANNEL_OP_REPLACE,
            ellipse.top_left_point.x,
            ellipse.top_left_point.y,
            ellipse.width,
            ellipse.height
        )

    def draw_random_filled_rectangle(self):
        self.__draw_filled_rectangle(Selection(Point()))

    def __draw_filled_rectangle(self, rectangle, color=None):
        change_foreground_color(color)
        self.__select_rectangle(rectangle)
        self.__fill_selection()
        self.__clear_selection()

    def __fill_selection(self):
        pdb.gimp_edit_fill(self.__get_drawable(), FOREGROUND_FILL)

    def draw_random_filled_ellipse(self):
        self.__draw_filled_ellipse(Selection(Point()))

    def __draw_filled_ellipse(self, ellipse, color=None):
        change_foreground_color(color)
        self.__select_ellipse(ellipse)
        self.__fill_selection()
        self.__clear_selection()

    def __clear_selection(self):
        pdb.gimp_image_select_rectangle(self.image_id, CHANNEL_OP_REPLACE, 0, 0, WIDTH, HEIGHT)


def plugin_main(image_id):
    global WIDTH, HEIGHT
    image = Image(image_id)
    WIDTH = image.get_width()
    HEIGHT = image.get_height()
    actions = [
        lambda: image.draw_random_brush_line(),
        # lambda: image.draw_random_ellipse(),
        lambda: image.draw_random_filled_ellipse(),
        lambda: image.draw_random_filled_rectangle(),
        lambda: image.draw_random_pencil_line()
        # lambda: image.draw_random_rectangle()
    ]
    actions[random.randint(0, len(actions) - 1)]()


def change_foreground_color(color):
    gimp.set_foreground(randomize_if_none(color))


def randomize_if_none(color):
    return random_color() if color is None else color


def random_color():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


register("perform_random_action", "", "", "", "", "", "", "",
         [(PF_IMAGE, "image", "Image", "")], [], plugin_main)

main()
