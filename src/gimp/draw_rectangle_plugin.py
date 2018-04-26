import os

from gimpfu import *
from src.gimp import initializer
from src.gimp.image import Image

RECTANGLE = 1
PATH = os.path.expandvars("$GIMP_PROJECT/result/gimp_images/nn/square_parameters")


def plugin_main(name, size, r, g, b, a, x, y, w, h, rotation):
    image = Image(initializer.new_image(size, size))
    image.perform_action(RECTANGLE, (r, g, b, a, x, y, w, h, rotation))
    image.save("%s/%s" % (PATH, name))


register("draw_rectangle", "", "", "", "", "", "", "",
         [
             (PF_STRING, "name", "result name", ""),
             (PF_INT, "size", "image size", 100),
             (PF_FLOAT, "r", "red part of rgba (0 - 1)", 0.),
             (PF_FLOAT, "g", "green part of rgba (0 - 1)", 0.),
             (PF_FLOAT, "b", "blue part of rgba (0 - 1)", 0.),
             (PF_FLOAT, "a", "alpha part of rgba (0 - 1)", 1.),
             (PF_FLOAT, "x", "x coordinate of left upper corner (0 - 1)", 0),
             (PF_FLOAT, "y", "y coordinate of left upper corner (0 - 1)", 0),
             (PF_FLOAT, "w", "rectangle width (0 - 1)", 0),
             (PF_FLOAT, "h", "rectangle height (0 - 1)", 0),
             (PF_FLOAT, "rotation",
              "rectangle rotation (0 - 1) - 0 means -180 roation, 0.5 - 0, 1 - 180", 0.5)
         ], [], plugin_main)

main()
