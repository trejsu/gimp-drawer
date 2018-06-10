import tqdm

import numpy as np

from gimpfu import *

from src.gimp import initializer
from src.gimp.image import Image
from src.gimp.environment import Environment


def plugin_main(image_size, image_n, test_part):
    generate_set(int(image_n * (1 - test_part)), image_size, "train")
    generate_set(int(image_n * test_part), image_size, "test")


def generate_set(image_n, image_size, name):
    def initialize():
        X = np.zeros((image_n, image_size, image_size, 3))
        Y = np.zeros((image_n, 9))
        return X, Y

    def rand():
        return np.random.uniform(0., 1.), np.random.uniform(0., 1.), np.random.uniform(0., 1.), \
               np.random.uniform(0., 1.), np.random.uniform(0., 1.), np.random.uniform(0., 1.), \
               np.random.uniform(0., 1.), np.random.uniform(0., 1.), np.random.uniform(0., 1.)

    X, Y = initialize()

    image = Image(initializer.new_image(image_size, image_size))
    white_image_np = np.ones((image_size, image_size, 3))

    action = Environment.Action.LINE

    for i in tqdm.tqdm(range(image_n), "Generating %s set" % name):
        r, g, b, a, x1, y1, x2, y2, size = rand()
        image.perform_action(action, (r, g, b, a, x1, y1, x2, y2, size))
        array = image.array
        X[i] = (array / 255.) - white_image_np
        Y[i] = [r, g, b, a, x1, y1, x2, y2, size]
        image.clear()

    path = "./{}_{}.npy"
    np.save(path.format(name, "X"), X)
    np.save(path.format(name, "Y"), Y)
