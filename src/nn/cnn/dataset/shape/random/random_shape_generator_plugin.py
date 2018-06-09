from gimpfu import *
import numpy as np
import tqdm

from src.gimp.image import Image
import src.gimp.initializer as initializer


def plugin_main(image_size, num_images, max_examples_per_part, test_part, without_rotation):
    generate_set(int(num_images * (1 - test_part)), image_size, "train", max_examples_per_part, without_rotation)
    generate_set(int(num_images * test_part), image_size, "test", max_examples_per_part, without_rotation)


def generate_set(num_images, image_size, name, max_examples_per_part, without_rotation):
    def initialize(num_examples):
        X = np.zeros((num_examples, image_size, image_size, 3))
        Y = np.zeros((num_examples, 4))
        return X, Y

    def save(X, Y, p):
        path = "./{}_{}_{}.npy"
        np.save(path.format(name, "X", p), X)
        np.save(path.format(name, "Y", p), Y)

    def generate_args(a):
        if a == 0 or a == 1:
            return generate_args_for_selection_shape()
        elif a == 2:
            return generate_args_for_line()
        else:
            return generate_args_for_triangle()

    def generate_args_for_selection_shape():
        def rand():
            return np.random.uniform(0., 1.), np.random.uniform(0., 1.), np.random.uniform(0., 1.), \
                   np.random.uniform(0., 1.), np.random.uniform(0., 1.), np.random.uniform(0., 1.), \
                   np.random.uniform(0. + (1. / image_size), 1.), \
                   np.random.uniform(0. + (1. / image_size), 1.), np.random.uniform(0., 1.)

        r, g, b, a, x, y, w, h, rotation = rand()
        w = min(w, 1 - x)
        h = min(h, 1 - y)
        rotation = 0.5 if without_rotation else rotation
        return r, g, b, a, x, y, w, h, rotation

    def generate_args_for_line():
        def rand():
            return np.random.uniform(0., 1.), np.random.uniform(0., 1.), np.random.uniform(0., 1.), \
                   np.random.uniform(0., 1.), np.random.uniform(0., 1.), np.random.uniform(0., 1.), \
                   np.random.uniform(0., 1.), np.random.uniform(0., 1.), np.random.uniform(0., 1.)

        return rand()

    def generate_args_for_triangle():
        def rand():
            return np.random.uniform(0., 1.), np.random.uniform(0., 1.), np.random.uniform(0., 1.), \
                   np.random.uniform(0., 1.), np.random.uniform(0., 1.), np.random.uniform(0., 1.), \
                   np.random.uniform(0., 1.), np.random.uniform(0., 1.), np.random.uniform(0., 1.), \
                   np.random.uniform(0., 1.)

        return rand()

    remaining_examples = num_images
    part = 1

    image = Image(initializer.new_image(image_size, image_size))
    white_image_np = np.ones((image_size, image_size, 3))

    while remaining_examples > 0:
        examples_in_current_part = min(remaining_examples, max_examples_per_part)
        X, Y = initialize(examples_in_current_part)
        for i in tqdm.tqdm(range(examples_in_current_part), "Generating {} set, part {}".format(name, part)):
            action = np.random.randint(0, 4)
            args = generate_args(action)
            image.perform_action(action, args)
            array = image.array
            X[i] = (array / 255.) - white_image_np
            Y[i][action] = 1
            image.clear()

        save(X, Y, part)
        remaining_examples -= examples_in_current_part
        part += 1





