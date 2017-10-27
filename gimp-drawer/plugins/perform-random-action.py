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
        self.width = random.randint(1, self.__validate(WIDTH - self.top_left_point.x)) if width is None else width
        self.height = random.randint(1, self.__validate(HEIGHT - self.top_left_point.y)) if height is None else height

    @staticmethod
    def __validate(points_left):
        return points_left if points_left > 0 else 1


def plugin_main(image):
    global WIDTH, HEIGHT
    WIDTH = get_drawable(image).width
    HEIGHT = get_drawable(image).height
    actions = [lambda img: draw_random_brush_line(img)]
    actions[random.randint(0, len(actions) - 1)](image)


def get_drawable(image):
    return pdb.gimp_image_active_drawable(image)


def draw_random_brush_line(image):
    draw_brush_line(image, Point(), Point())


def draw_brush_line(image, start, end, color=None):
    change_foreground_color(color)
    control_points = [start.x, start.y, end.x, end.y]
    pdb.gimp_paintbrush_default(get_drawable(image), len(control_points), control_points)


def change_foreground_color(color):
    gimp.set_foreground(randomize_if_none(color))


def randomize_if_none(color):
    return random_color() if color is None else color


def random_color():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


register("perform_random_action", "", "", "", "", "", "", "",
         [(PF_IMAGE, "image", "Image", "")], [], plugin_main)

main()
