import tqdm

import numpy as np

from gimpfu import *
from gimp import initializer
from gimp.image import Image

RECTANGLE = 1
RED = 0.
GREEN = 0.
BLUE = 0.
ALPHA = 1.
ROTATION = 0.5


def plugin_main(image_size, square_size, image_n, test_part):
    generate_set(int(image_n * (1 - test_part)), image_size, square_size, "train")
    generate_set(int(image_n * test_part), image_size, square_size, "test")


def generate_set(image_n, image_size, square_size, name):
    def scale(x):
        return x / float(image_size)

    def initialize():
        X = np.zeros((image_n, image_size, image_size))
        Y_1 = np.zeros((image_n, 2))
        Y_2 = np.zeros((image_n, 1), dtype=np.int8)
        Y_4 = np.zeros((image_n, 1), dtype=np.int8)
        Y_9 = np.zeros((image_n, 1), dtype=np.int8)
        Y_25 = np.zeros((image_n, 1), dtype=np.int8)
        return X, Y_1, Y_2, Y_25, Y_4, Y_9

    X, Y_1, Y_2, Y_25, Y_4, Y_9 = initialize()

    image = Image(initializer.new_image(image_size, image_size))

    for i in tqdm.tqdm(range(image_n), "Generating %s set" % name):
        square_size = np.random.randint(3, image_size)
        x_coor = np.random.randint(0, image_size - square_size)
        y_coor = np.random.randint(0, image_size - square_size)
        image.perform_action(RECTANGLE, (RED, GREEN, BLUE, ALPHA, scale(x_coor), scale(y_coor), scale(square_size), scale(square_size), ROTATION))
        array = np.sum(image.array, axis=2) / 3
        X[i] = array / 255.
        # draw white rectangle to "reset" image
        image.perform_action_without_array_update(RECTANGLE, (1., 1., 1., ALPHA, scale(x_coor), scale(y_coor), scale(square_size), scale(square_size), ROTATION))
        x_center = x_coor + square_size * 0.5
        y_center = y_coor + square_size * 0.5
        Y_1[i][0] = scale(x_center)
        Y_1[i][1] = scale(y_center)
        Y_2[i] = 0 if x_center <= (image_size / 2) else 1
        Y_4[i] = find_label(x_center, y_center, 2, image_size)
        Y_9[i] = find_label(x_center, y_center, 3, image_size)
        Y_25[i] = find_label(x_center, y_center, 5, image_size)

    path = "./{}_{}.npy"
    np.save(path.format(name, "X"), X)
    np.save(path.format(name, "Y_1"), Y_1)
    np.save(path.format(name, "Y_2"), Y_2)
    np.save(path.format(name, "Y_4"), Y_4)
    np.save(path.format(name, "Y_9"), Y_9)
    np.save(path.format(name, "Y_25"), Y_25)


def find_label(x, y, parts1d, size):
    """Return part of image divided to parts1d * parts1d parts
       where (x, y) point belongs

        >>> find_label(60, 60, 2, 100)
        3
        >>> find_label(42, 28, 5, 100)
        7
        >>> find_label(68, 37, 5, 100)
        8
    """
    size = size // parts1d
    x = x // size
    y = y // size
    return int(x + parts1d * y)


register("square_generator", "", "", "", "", "", "", "",
         [
             (PF_INT, "image", "Image size", 100),
             (PF_INT, "square", "Square size", 20),
             (PF_INT, "number", "Number of images for the whole dataset", 5000),
             (PF_FLOAT, "test", "Percentage of images used for testing", 0.3)
         ], [], plugin_main)

main()
