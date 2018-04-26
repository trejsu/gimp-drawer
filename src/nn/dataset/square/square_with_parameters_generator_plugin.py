import tqdm

import numpy as np

from gimpfu import *

from src.gimp import initializer
from src.gimp.image import Image

RECTANGLE = 1
RED = 0.
GREEN = 0.
BLUE = 0.
ALPHA = 1.
ROTATION = 0.5


def plugin_main(image_size, image_n, test_part):
    generate_set(int(image_n * (1 - test_part)), image_size, "train")
    generate_set(int(image_n * test_part), image_size, "test")


def generate_set(image_n, image_size, name):
    def scale(x):
        return x / float(image_size)

    def initialize():
        X = np.zeros((image_n, image_size, image_size))
        Y = np.zeros((image_n, 9))
        return X, Y

    X, Y = initialize()

    image = Image(initializer.new_image(image_size, image_size))
    white_image_np = np.ones((image_size, image_size))

    for i in tqdm.tqdm(range(image_n), "Generating %s set" % name):
        square_size = np.random.randint(3, image_size)
        x_coor = np.random.randint(0, image_size - square_size)
        y_coor = np.random.randint(0, image_size - square_size)
        image.perform_action(RECTANGLE, (RED, GREEN, BLUE, ALPHA, scale(x_coor), scale(y_coor), scale(square_size), scale(square_size), ROTATION))
        array = np.sum(image.array, axis=2) / 3
        X[i] = white_image_np - (array / 255.)
        # draw white rectangle to "reset" image
        image.perform_action_without_array_update(RECTANGLE, (1., 1., 1., ALPHA, scale(x_coor), scale(y_coor), scale(square_size), scale(square_size), ROTATION))
        Y[i][0] = RED
        Y[i][1] = GREEN
        Y[i][2] = BLUE
        Y[i][3] = ALPHA
        Y[i][4] = scale(x_coor)
        Y[i][5] = scale(y_coor)
        Y[i][6] = scale(square_size)
        Y[i][7] = scale(square_size)
        Y[i][8] = ROTATION

    path = "./{}_{}.npy"
    np.save(path.format(name, "X"), X)
    np.save(path.format(name, "Y"), Y)


register("square_with_parameters_generator", "", "", "", "", "", "", "",
         [
             (PF_INT, "image", "Image size", 100),
             (PF_INT, "number", "Number of images for the whole dataset", 5000),
             (PF_FLOAT, "test", "Percentage of images used for testing", 0.3)
         ], [], plugin_main)

main()
