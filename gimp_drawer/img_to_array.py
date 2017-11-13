#!/usr/bin/python

import numpy


def convert_to_array(drawable):
    return __convert__(drawable, "d")


def convert_to_displayable_array(drawable):
    return __convert__(drawable, numpy.uint8)


def __convert__(drawable, dtype):
    width = drawable.width
    height = drawable.height
    bytes_per_pixel = drawable.bpp
    pixel_region = drawable.get_pixel_rgn(0, 0, width, height, False)
    array = numpy.fromstring(pixel_region[:, :], "B")
    assert array.size == width * height * bytes_per_pixel
    reshape = array.reshape(height, width, bytes_per_pixel)
    return numpy.array(reshape, dtype=dtype)[:, :, 0:min(bytes_per_pixel, 3)]
