#!/usr/bin/python

import numpy
from gimp_drawer.decorators import timed


@timed
def read_drawable(drawable):
    width = drawable.width
    height = drawable.height
    bpp = drawable.bpp
    pixel_region = drawable.get_pixel_rgn(0, 0, width, height, False)
    array = numpy.fromstring(pixel_region[:, :], "B")
    assert array.size == width * height * bpp
    reshape = array.reshape(height, width, bpp)
    return __get_numpy_array(reshape, "d", bpp), \
           __get_numpy_array(reshape, numpy.uint8, bpp)


@timed
def __get_numpy_array(reshape, data_type, bpp):
    return numpy.array(reshape, dtype=data_type)[:, :, 0:min(bpp, 3)]
