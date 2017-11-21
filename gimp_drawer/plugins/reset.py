#!/usr/bin/python

from gimpfu import *


def plugin_main(img):
    pdb.gimp_edit_fill(get_drawable(img), WHITE_FILL)


def get_drawable(image):
    return pdb.gimp_image_active_drawable(image)


def get_height(image):
    return pdb.gimp_image_active_drawable(image).height


register("reset", "", "", "", "", "", "", "",
         [(PF_IMAGE, "img", "Image", "")],
         [],
         plugin_main)

main()
