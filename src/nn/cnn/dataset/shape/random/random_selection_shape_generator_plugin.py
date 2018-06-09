import tqdm

import numpy as np

from gimpfu import *

from src.gimp import initializer
from src.gimp.image import Image
from src.gimp.environment import Environment


def plugin_main(image_size, image_n, test_part, shape, without_rotation):
    generate_set(int(image_n * (1 - test_part)), image_size, "train", shape,
                 without_rotation)
    generate_set(int(image_n * test_part), image_size, "test", shape,
                 without_rotation)


def generate_set(image_n, image_size, name, shape, without_rotation):
    def initialize():
        X = np.zeros((image_n, image_size, image_size, 3))
        Y = np.zeros((image_n, 9))
        return X, Y

    def rand():
        return np.random.uniform(0., 1.), np.random.uniform(0., 1.), np.random.uniform(0., 1.), \
               np.random.uniform(0., 1.), np.random.uniform(0., 1.), np.random.uniform(0., 1.), \
               np.random.uniform(0. + (1. / image_size), 1.), \
               np.random.uniform(0. + (1. / image_size), 1.), np.random.uniform(0., 1.)

    X, Y = initialize()

    image = Image(initializer.new_image(image_size, image_size))
    white_image_np = np.ones((image_size, image_size, 3))

    action = Environment.Action.ELLIPSE if shape == 'ellipse' else Environment.Action.RECTANGLE

    for i in tqdm.tqdm(range(image_n), "Generating %s set" % name):
        r, g, b, a, x, y, w, h, rotation = rand()
        w = min(w, 1 - x)
        h = min(h, 1 - y)
        rotation = 0.5 if without_rotation else rotation
        image.perform_action(action, (r, g, b, a, x, y, w, h, rotation))
        array = image.array
        X[i] = (array / 255.) - white_image_np
        Y[i] = [r, g, b, a, x, y, w, h, rotation]
        image.clear()

    path = "./{}_{}.npy"
    np.save(path.format(name, "X"), X)
    np.save(path.format(name, "Y"), Y)
