#!/usr/bin/python

from gimpfu import *


def plugin_main(src_path):
    src_img = pdb.gimp_file_load(src_path, src_path)
    actual_img = new_image(get_width(src_img), get_height(src_img))
    return src_img, actual_img


def new_image(width, height):
    image_id = gimp.Image(width, height, RGB_IMAGE)
    layer = gimp.Layer(image_id, "layer", width,
                       height, RGB_IMAGE, 100,
                       NORMAL_MODE)
    image_id.add_layer(layer, 0)
    return image_id


def get_width(image):
    return get_drawable(image).width


def get_drawable(image):
    return pdb.gimp_image_active_drawable(image)


def get_height(image):
    return pdb.gimp_image_active_drawable(image).height


register("initialize", "", "", "", "", "", "", "",
         [(PF_STRING, "src_path", "Input", "")],
         [
             (PF_IMAGE, "src_img", "Source image", ""),
             (PF_IMAGE, "result_img", "Result image", "")
         ],
         plugin_main)

main()
