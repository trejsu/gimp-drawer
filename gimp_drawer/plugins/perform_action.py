#!/usr/bin/python

from gimpfu import *
from random import randint

WIDTH = 0
HEIGHT = 0


class Point(object):
    def __init__(self, x=None, y=None):
        super(Point, self).__init__()
        self.x = randint(0, WIDTH) if x is None else x
        self.y = randint(0, HEIGHT) if y is None else y


class Selection(object):
    def __init__(self, top_left, width=None, height=None):
        super(Selection, self).__init__()
        self.top_left = top_left
        self.width = randint(1, self.validate(WIDTH - self.top_left.x)) \
            if width is None else width
        self.height = randint(1, self.validate(HEIGHT - self.top_left.y)) \
            if height is None else height

    @staticmethod
    def validate(points_left):
        return points_left if points_left > 0 else 1


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
        points = [start.x, start.y, end.x, end.y]
        pdb.gimp_paintbrush_default(self.__get_drawable(), len(points), points)

    def draw_random_pencil_line(self):
        self.__draw_pencil_line(Point(), Point())

    def __draw_pencil_line(self, start, end, color=None, size=None):
        change_foreground_color(color)
        # change_size(size)
        points = [start.x, start.y, end.x, end.y]
        pdb.gimp_pencil(self.__get_drawable(), len(points), points)

    def __select_rectangle(self, rectangle):
        pdb.gimp_image_select_rectangle(
            self.image_id,
            CHANNEL_OP_REPLACE,
            rectangle.top_left.x,
            rectangle.top_left.y,
            rectangle.width,
            rectangle.height
        )

    def __select_ellipse(self, ellipse):
        pdb.gimp_image_select_ellipse(
            self.image_id,
            CHANNEL_OP_REPLACE,
            ellipse.top_left.x,
            ellipse.top_left.y,
            ellipse.width,
            ellipse.height
        )

    def draw_random_rectangle(self):
        self.__draw_rectangle(Selection(Point()))

    def __draw_rectangle(self, rectangle, color=None):
        change_foreground_color(color)
        self.__select_rectangle(rectangle)
        self.__fill_selection()
        self.__clear_selection()

    def __fill_selection(self):
        pdb.gimp_edit_fill(self.__get_drawable(), FOREGROUND_FILL)

    def draw_random_ellipse(self):
        self.__draw_ellipse(Selection(Point()))

    def __draw_ellipse(self, ellipse, color=None):
        change_foreground_color(color)
        self.__select_ellipse(ellipse)
        self.__fill_selection()
        self.__clear_selection()

    def __clear_selection(self):
        pdb.gimp_image_select_rectangle(self.image_id, CHANNEL_OP_REPLACE, 0,
                                        0, WIDTH, HEIGHT)


def plugin_main(image_id, action):
    global WIDTH, HEIGHT
    image = Image(image_id)
    WIDTH = image.get_width()
    HEIGHT = image.get_height()
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
    return randint(0, 255), randint(0, 255), randint(0, 255)


def change_size(size):
    pdb.gimp_context_set_brush_size(randomize_size_if_none(size))


def randomize_size_if_none(size):
    return random_size() if size is None else size


def random_size():
    return randint(1, min(WIDTH / 5, HEIGHT / 5))


register("perform_action", "", "", "", "", "", "", "",
         [(PF_IMAGE, "image", "Image", ""), (PF_INT, "action", "Action", 0)],
         [], plugin_main)

main()
