import tqdm

import numpy as np

from gimpfu import *

from src.gimp import initializer
from src.gimp.image import Image

RECTANGLE = 1


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

    for i in tqdm.tqdm(range(image_n), "Generating %s set" % name):
        r, g, b, a, x, y, w, h, rotation = rand()
        image.perform_action(RECTANGLE, (r, g, b, a, x, y, w, h, rotation))
        array = image.array
        X[i] = white_image_np - (array / 255.)
        Y[i] = [r, g, b, a, x, y, w, h, rotation]
        image.clear()

    path = "./{}_{}.npy"
    np.save(path.format(name, "X"), X)
    np.save(path.format(name, "Y"), Y)


register("random_square_with_parameters_generator", "", "", "", "", "", "", "",
         [
             (PF_INT, "image", "Image size", 100),
             (PF_INT, "number", "Number of images for the whole dataset", 5000),
             (PF_FLOAT, "test", "Percentage of images used for testing", 0.3)
         ], [], plugin_main)

main()
