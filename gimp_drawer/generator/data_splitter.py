#!/usr/bin/python

import getopt
import sys
import glob
import random
import tqdm

import numpy as np

from gimp_drawer.generator.natural_keys import natural_keys


def create_data(image_dirs, set_name, path):
    def save(to_save, name): np.save("{}/{}_{}.npy".format(path, set_name, name), to_save)

    data = correlate_x_y_and_labels(image_dirs)
    random.shuffle(data)

    X = []
    Y = []
    labels = []

    for d in tqdm.tqdm(data, "Creating {} data set".format(set_name)):
        x = np.load(d[0])
        X.append(x.tolist())
        y = np.load(d[1])
        Y.append(y.tolist())
        labels.append(d[2])

    X = np.array(X)
    Y = np.array(Y)

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
            data.append((x, y, image_name))
    return data


def main(argv):
    path, limit = read_args(argv)
    test_image_dirs, train_image_dirs = split_images(path, limit)
    create_data(train_image_dirs, "train", path)
    create_data(test_image_dirs, "test", path)


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
