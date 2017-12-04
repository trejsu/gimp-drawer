from gimpfu import *
from gimp_drawer.common.decorators.timed import timed


class Selection(object):
    def __init__(self, image, top_left, width, height):
        self.image = image
        self.top_left = self.__from_normalized_point(top_left)
        self.width = self.__from_normalized_width(width, self.top_left.x)
        self.height = self.__from_normalized_height(height, self.top_left.y)

    @timed
    def select_rectangle(self):
        pdb.gimp_image_select_rectangle(self.image, CHANNEL_OP_REPLACE, self.top_left.x, self.top_left.y, self.width, self.height)

    @timed
    def select_ellipse(self):
        pdb.gimp_image_select_ellipse(self.image, CHANNEL_OP_REPLACE, self.top_left.x, self.top_left.y, self.width, self.height)

    @timed
    def __from_normalized_point(self, point):
        return Point(point.x * self.image.width, point.y * self.image.height)

    @timed
    def __from_normalized_width(self, width, boundary):
        return width * (self.image.width - boundary)

    @timed
    def __from_normalized_height(self, height, boundary):
        return height * (self.image.height - boundary)


class Point(object):
    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y

