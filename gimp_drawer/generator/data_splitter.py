#!/usr/bin/python

import getopt
import sys
import glob
import random
import tqdm

import numpy as np
from scipy import sum

from gimp_drawer.generator.natural_keys import natural_keys


def create_data(image_dirs, set_name, path):
    data = correlate_x_y_and_labels(image_dirs)
    random.shuffle(data)

    X, Y, labels = initialize(len(data))

    # todo: X, Y, labels should be appended to file
    index = 0
    for d in tqdm.tqdm(data, "Creating {} data set".format(set_name)):
        x = np.load(d[0])
        X[index] = x
        y = np.load(d[1])
        Y[index] = y
        labels[index] = d[2]
        index += 1

    save_set(X, Y, labels, path, set_name)


def initialize(size):
    X = np.empty((size, 100, 100, 3))
    Y = np.empty((size, 9))
    labels = np.empty((size, 2), np.int)
    return X, Y, labels


def save_set(X, Y, labels, path, set_name):
    def save(to_save, name): np.save("{}/{}_{}.npy".format(path, set_name, name), to_save)
    save(X, "X")
    save(Y, "Y")
    save(labels, "labels")


def correlate_x_y_and_labels(image_dirs):
    data = []
    for image in image_dirs:
        X = get_all_file_paths(image + "/X_*.npy")
        Y = get_all_file_paths(image + "/Y_*.npy")
        X.sort(key=natural_keys)
        Y.sort(key=natural_keys)
        image_name = image.split("/")[-1]
        for x, y in zip(X, Y):
            action_number = x.split("/")[-1].split("_")[-1].split(".")[0]
            data.append((x, y, (image_name, action_number)))
    return data


def validate(X, Y, labels, path, set_name):
    size = X.shape[0]
    sample_indexes = random.sample(range(0, size - 1), 100)
    for index in tqdm.tqdm(sample_indexes, "Validating {} data set".format(set_name)):
        label = labels[index]
        x_from_X = X[index]
        image_name = label[0]
        action_number = label[1]
        x_from_file = np.load(path + "/{}/X_{}.npy".format(image_name, action_number))
        assert sum(x_from_X - x_from_file) == 0
        y_from_Y = Y[index]
        y_from_file = np.load(path + "/{}/Y_{}.npy".format(image_name, action_number))
        assert sum(y_from_Y - y_from_file) == 0


def validate_data(path):
    def load(name): return np.load(path + name, mmap_mode="r")

    test_X = load("/test_X.npy")
    train_X = load("/train_X.npy")
    test_Y = load("/test_Y.npy")
    train_Y = load("/train_Y.npy")
    test_labels = load("/test_labels.npy")
    train_labels = load("/train_labels.npy")

    validate(train_X, train_Y, train_labels, path, "train")
    validate(test_X, test_Y, test_labels, path, "test")


def main(argv):
    path, limit = read_args(argv)
    test_image_dirs, train_image_dirs = split_images(path, limit)
    create_data(train_image_dirs, "train", path)
    create_data(test_image_dirs, "test", path)
    validate_data(path)


def split_images(path, limit):
    image_dirs = get_all_file_paths(path + "/[0-9]*")
    image_dirs = limit_images(image_dirs, limit)
    image_dirs.sort(key=natural_keys)
    train_images_number = int(len(image_dirs) * 0.8)
    train_image_dirs = image_dirs[:train_images_number]
    test_image_dirs = image_dirs[train_images_number:]
    return test_image_dirs, train_image_dirs


def limit_images(image_dirs, limit):
    if limit is not None:
        random.shuffle(image_dirs)
        image_dirs = image_dirs[:limit]
    return image_dirs


def get_all_file_paths(path): return glob.glob(path)


def read_args(argv):
    path = None
    limit = None
    opts, args = getopt.getopt(argv, "p:l:")

    for opt, arg in opts:
        if opt == '-p':
            path = arg
        if opt == '-l':
            limit = int(arg)

    return path, limit


if __name__ == '__main__':
    main(sys.argv[1:])
