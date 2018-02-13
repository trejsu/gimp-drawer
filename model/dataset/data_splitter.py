#!/usr/bin/python

import glob
import random
import argparse

import numpy as np
import tqdm

from model.dataset.natural_keys import natural_keys


ARGS = None


def main():
    test_images, train_images = split_images()
    create_data(train_images, "train")
    create_data(test_images, "test")


def split_images():
    image_dirs = get_all_file_paths(ARGS.path + "/[0-9]*")
    image_dirs.sort(key=natural_keys)
    train_images_number = int(len(image_dirs) * 0.8)
    train_image_dirs = image_dirs[:train_images_number]
    test_image_dirs = image_dirs[train_images_number:]
    return test_image_dirs, train_image_dirs


def get_all_file_paths(path): return glob.glob(path)


def create_data(image_dirs, set_name):
    data = correlate_x_y_and_labels(image_dirs)
    random.shuffle(data)
    data_left = len(data)
    index = -1
    data_left -= ARGS.limit
    current_part_size = ARGS.limit if data_left >= 0 else (ARGS.limit + data_left)
    current_part_number = 1
    X, Y, labels = initialize(current_part_size)
    for d in tqdm.tqdm(data, "Creating {} data set".format(set_name)):
        index += 1
        if index == current_part_size:
            save_set(X, Y, labels, set_name, current_part_number)
            index = 0
            data_left -= ARGS.limit
            current_part_size = ARGS.limit if data_left >= 0 else (ARGS.limit + data_left)
            current_part_number += 1
            del X, Y, labels
            X, Y, labels = initialize(current_part_size)

        x = np.load(d[0])
        X[index] = x
        y = np.load(d[1])
        Y[index] = y
        labels[index] = d[2]

    save_set(X, Y, labels, set_name, current_part_number)


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


def initialize(size):
    X = np.empty((size, 100, 100, 3))
    Y = np.empty((size, 9))
    labels = np.empty((size, 2), np.int)
    return X, Y, labels


def save_set(X, Y, labels, set_name, part):
    np.save("{}/{}_{}_{}.npy".format(ARGS.path, set_name, "X", part), X)
    np.save("{}/{}_{}_{}.npy".format(ARGS.path, set_name, "Y", part), Y)
    np.save("{}/{}_{}_{}.npy".format(ARGS.path, set_name, "labels", part), labels)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-p", "--path", type=str, help="path to the directory with diffs")
    parser.add_argument("-l", "--limit", type=int, default=70000,
                        help="number of actions for one numpy file of data set")
    ARGS = parser.parse_args()
    main()
