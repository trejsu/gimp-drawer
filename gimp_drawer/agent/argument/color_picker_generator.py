from gimpfu import pdb, HISTOGRAM_RED, HISTOGRAM_GREEN, HISTOGRAM_BLUE

from gimp_drawer.agent.argument.argument import Argument
from gimp_drawer.agent.argument.argument_generator import ArgumentGenerator
from gimp_drawer.common.decorators.timed import timed


class ColorPickerGenerator(ArgumentGenerator, object):
    def __init__(self, eps, src_image):
        super(ColorPickerGenerator, self).__init__(eps)
        self.src_image = src_image

    @timed
    def init(self, ranges, position, space):
        select_action = space.create_selection_action(self.src_image)
        select_action(position)
        drawable = pdb.gimp_image_get_active_drawable(self.src_image)
        red = pdb.gimp_histogram(drawable, HISTOGRAM_RED, 0, 255)[0] / 255
        green = pdb.gimp_histogram(drawable, HISTOGRAM_GREEN, 0, 255)[0] / 255
        blue = pdb.gimp_histogram(drawable, HISTOGRAM_BLUE, 0, 255)[0] / 255
        # todo: think about this 100 opacity, is it a good idea?
        return Argument(0, 1, red), Argument(0, 1, green), Argument(0, 1, blue), Argument(0, 1, 0.8)