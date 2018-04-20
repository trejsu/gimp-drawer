#!/usr/bin/python

from gimpfu import *

from src.common.timed import timed


@timed
def initialize(src_path, input_path, size=None):
    src_img = pdb.gimp_file_load(src_path, src_path)
    if size is not None:
        pdb.gimp_image_scale(src_img, size, size)
    src_drawable = pdb.gimp_image_active_drawable(src_img)
    if not pdb.gimp_drawable_is_rgb(src_drawable):
        pdb.gimp_image_convert_rgb(src_img)
    src_width = src_drawable.width
    src_height = src_drawable.height
    actual_img = new_image(src_width, src_height) if input_path == "None" \
        else __load_image(input_path, src_width, src_height)
    return src_img, actual_img


@timed
def initialize_with_scaled_src(src_path, size):
    src_img = pdb.gimp_file_load(src_path, src_path)
    pdb.gimp_image_scale(src_img, size, size)
    src_drawable = pdb.gimp_image_active_drawable(src_img)
    if not pdb.gimp_drawable_is_rgb(src_drawable):
        pdb.gimp_image_convert_rgb(src_img)
    actual_img = new_image(size, size)
    return src_img, actual_img


@timed
def load_scaled_src(src_path, size):
    src_img = pdb.gimp_file_load(src_path, src_path)
    pdb.gimp_image_scale(src_img, size, size)
    src_drawable = pdb.gimp_image_active_drawable(src_img)
    if not pdb.gimp_drawable_is_rgb(src_drawable):
        pdb.gimp_image_convert_rgb(src_img)
    return src_img


@timed
def initialize_for_model_testing(size):
    return new_image(size, size), new_image(size, size)


@timed
def new_image(width, height):
    image_id = gimp.Image(width, height, RGB_IMAGE)
    layer = gimp.Layer(image_id, "layer", width,
                       height, RGB_IMAGE, 100,
                       NORMAL_MODE)
    position = 0
    image_id.add_layer(layer, position)
    pdb.gimp_edit_fill(pdb.gimp_image_active_drawable(image_id), WHITE_FILL)
    return image_id


@timed
def __load_image(input_path, src_width, src_height):
    img = pdb.gimp_file_load(input_path, input_path)
    pdb.gimp_image_scale(img, src_width, src_height)
    return img
