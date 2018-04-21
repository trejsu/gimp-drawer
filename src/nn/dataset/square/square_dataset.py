import os
import math

import numpy as np

from src.nn.dataset.dataset import Dataset


SQUARE_CENTER_DATASET_PATH = os.path.expandvars("$SQUARE_CENTER_DATASET_PATH")
SQUARE_WITH_PARAMETERS_DATASET_PATH = os.path.expandvars("$SQUARE_WITH_PARAMETERS_DATASET_PATH")
DIFF_SQUARE_WITH_PARAMETERS_DATASET_PATH = os.path.expandvars("$DIFF_SQUARE_WITH_PARAMETERS_DATASET_PATH")
TRAIN = 3500
TEST = 1500


class SquareCenterDataset(Dataset):
    def __init__(self, class_n, batch_size):
        self.train = SquareCenterSet("train", class_n, TRAIN, batch_size)
        self.test = SquareCenterSet("test", class_n, TEST, batch_size)


class SquareWithParametersDataset(Dataset):
    def __init__(self, batch_size):
        self.train = SquareWithParametersSet("train", TRAIN, batch_size)
        self.test = SquareWithParametersSet("test", TEST, batch_size)


class DiffSquareWithParametersDataset(Dataset):
    def __init__(self, batch_size):
        self.train = DiffSquareWithParametersSet("train", TRAIN, batch_size)
        self.test = DiffSquareWithParametersSet("test", TEST, batch_size)


class SquareCenterRegressionDataset(SquareCenterDataset):
    def __init__(self, batch_size):
        super(SquareCenterRegressionDataset, self).__init__(1, batch_size)


class Set(object):
    def __init__(self, name, set_n, batch_size):
        self.name = name
        self.next_batch_index = 0
        self.batch_n = int(math.ceil(set_n / float(batch_size)))
        self.set_n = set_n
        self.X = None
        self.Y = None
        self.has_next = True
        self.batch_size = batch_size
        self.indexes = np.array(range(self.batch_n))

    def restart(self):
        self.next_batch_index = 0
        self.shuffle()
        self.has_next = True

    def next_batch(self):
        not_initialized = self.X is None or self.Y is None
        if not_initialized:
            self.load()
        end = self.next_batch_index == (self.set_n - 1)
        return self.next_batch_from_the_end() if end else self.default_next_batch()

    def load(self):
        raise NotImplementedError

    def next_batch_from_the_end(self):
        elements_left = self.set_n % self.batch_size
        X = self.X[-elements_left:]
        Y = self.Y[-elements_left:]
        self.has_next = False
        return X, Y

    def default_next_batch(self):
        batch_start = self.indexes[self.next_batch_index] * self.batch_size
        X = self.X[batch_start:batch_start + self.batch_size]
        Y = self.Y[batch_start:batch_start + self.batch_size]
        self.next_batch_index += 1
        return X, Y

    def shuffle(self):
        np.random.shuffle(self.indexes)

    def random_x(self, n):
        indexes = np.random.choice(self.set_n, n)
        return self.X[indexes]


class SquareCenterSet(Set):
    def __init__(self, name, class_n, set_n, batch_size):
        super(SquareCenterSet, self).__init__(name, set_n, batch_size)
        self.class_n = class_n

    def load(self):
        del self.X, self.Y
        self.X = np.load(SQUARE_CENTER_DATASET_PATH + "/%s_X.npy" % self.name, mmap_mode="r")
        self.Y = np.load(SQUARE_CENTER_DATASET_PATH + "/%s_Y_%d.npy" % (self.name, self.class_n), mmap_mode="r")
        self.shuffle()


class SquareWithParametersSet(Set):
    def __init__(self, name, set_n, batch_size):
        super(SquareWithParametersSet, self).__init__(name, set_n, batch_size)

    def load(self):
        del self.X, self.Y
        self.X = np.load(SQUARE_WITH_PARAMETERS_DATASET_PATH + "/%s_X.npy" % self.name, mmap_mode="r")
        self.Y = np.load(SQUARE_WITH_PARAMETERS_DATASET_PATH + "/%s_Y.npy" % self.name, mmap_mode="r")
        self.shuffle()


class DiffSquareWithParametersSet(Set):
    def __init__(self, name, set_n, batch_size):
        super(DiffSquareWithParametersSet, self).__init__(name, set_n, batch_size)

    def load(self):
        del self.X, self.Y
        self.X = np.load(DIFF_SQUARE_WITH_PARAMETERS_DATASET_PATH + "/%s_X.npy" % self.name, mmap_mode="r")
        self.Y = np.load(DIFF_SQUARE_WITH_PARAMETERS_DATASET_PATH + "/%s_Y.npy" % self.name, mmap_mode="r")
        self.shuffle()


def get_dataset(name):
    return {
        'center': SquareCenterRegressionDataset,
        'parameters': SquareWithParametersDataset,
        'diff_parameters': DiffSquareWithParametersDataset
    }[name]

