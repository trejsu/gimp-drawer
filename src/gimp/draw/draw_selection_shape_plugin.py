import os

from gimpfu import *
from src.gimp import initializer
from src.gimp.image import Image
from src.gimp.environment import Environment

PATH = os.path.expandvars("$GIMP_PROJECT/result/gimp_images/nn/shapes")


def plugin_main(name, size, r, g, b, a, x, y, w, h, rotation, shape):
    image = Image(initializer.new_image(size, size))
    action = Environment.Action.ELLIPSE if shape == 'ellipse' else Environment.Action.RECTANGLE
    image.perform_action(action, (r, g, b, a, x, y, w, h, rotation))
    image.save("%s/%s" % (PATH, name))