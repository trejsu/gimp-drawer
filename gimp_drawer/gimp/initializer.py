#!/usr/bin/python

from gimpfu import *

from gimp_drawer.decorators.timed import timed


@timed
def initialize(src_path):
    src_img = pdb.gimp_file_load(src_path, src_path)
    actual_img = __new_image(__get_width(src_img), __get_height(src_img))
    return src_img, actual_img


@timed
def reset(img):
    pdb.gimp_edit_fill(__get_drawable(img), WHITE_FILL)


@timed
def __new_image(width, height):
    image_id = gimp.Image(width, height, RGB_IMAGE)
    layer = gimp.Layer(image_id, "layer", width,
                       height, RGB_IMAGE, 100,
                       NORMAL_MODE)
    position = 0
    image_id.add_layer(layer, position)
    return image_id


@timed
def __get_width(image):
    return __get_drawable(image).width


@timed
def __get_drawable(image):
    return pdb.gimp_image_active_drawable(image)


@timed
def __get_height(image):
    return pdb.gimp_image_active_drawable(image).height
