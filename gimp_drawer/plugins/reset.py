#!/usr/bin/python

from gimpfu import *
from gimp_drawer.decorators import timed


@timed
def plugin_main(img):
    pdb.gimp_edit_fill(get_drawable(img), WHITE_FILL)


@timed
def get_drawable(image):
    return pdb.gimp_image_active_drawable(image)


@timed
def get_height(image):
    return pdb.gimp_image_active_drawable(image).height


register("reset", "", "", "", "", "", "", "",
         [(PF_IMAGE, "img", "Image", "")],
         [],
         plugin_main)

main()
