import os

from gimpfu import *
from src.gimp import initializer
from src.gimp.image import Image
from src.gimp.environment import Environment

PATH = os.path.expandvars("$GIMP_PROJECT/result/gimp_images/nn/shapes")


def plugin_main(name, size, r, g, b, a, x1, y1, x2, y2, x3, y3):
    image = Image(initializer.new_image(size, size))
    action = Environment.Action.TRIANGLE
    image.perform_action(action, (r, g, b, a, x1, y1, x2, y2, x3, y3))
    image.save("%s/%s" % (PATH, name))


register("draw_triangle", "", "", "", "", "", "", "",
         [
             (PF_STRING, "name", "result name", ""),
             (PF_INT, "size", "image size", 100),
             (PF_FLOAT, "r", "red part of rgba (0 - 1)", 0.),
             (PF_FLOAT, "g", "green part of rgba (0 - 1)", 0.),
             (PF_FLOAT, "b", "blue part of rgba (0 - 1)", 0.),
             (PF_FLOAT, "a", "alpha part of rgba (0 - 1)", 1.),
             (PF_FLOAT, "x1", "x1", 0),
             (PF_FLOAT, "y1", "y1", 0),
             (PF_FLOAT, "x2", "x2", 0),
             (PF_FLOAT, "y2", "y2", 0),
             (PF_FLOAT, "x3", "x3", 0),
             (PF_FLOAT, "y3", "y3", 0)
         ], [], plugin_main)

main()
