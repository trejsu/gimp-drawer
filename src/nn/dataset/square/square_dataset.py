import os
import math

import numpy as np

from nn.dataset.dataset import Dataset


PATH = os.path.expandvars("$SQUARE_DATASET_PATH")
TRAIN = 3500
TEST = 1500


class SquareDataset(Dataset):
    def __init__(self, class_n, batch_size):
        self.train = Set("train", class_n, TRAIN, batch_size)
        self.test = Set("test", class_n, TEST, batch_size)


class Set(object):
    def __init__(self, name, class_n, set_n, batch_size):
        self.name = name
        self.next_batch_index = 0
        self.batch_n = int(math.ceil(set_n / float(batch_size)))
        self.set_n = set_n
        self.X = None
        self.Y = None
        self.has_next = True
        self.class_n = class_n
        self.batch_size = batch_size
        self.indexes = np.array(range(self.batch_n))

    def restart(self):
        self.next_batch_index = 0
        self.__shuffle()
        self.has_next = True

    def next_batch(self):
        not_initialized = self.X is None or self.Y is None
        if not_initialized:
            self.__load()
        end = self.next_batch_index == (self.set_n - 1)
        return self.__next_batch_from_the_end() if end else self.__next_batch()

    def __load(self):
        del self.X, self.Y
        self.X = np.load(PATH + "/%s_X.npy" % self.name, mmap_mode="r")
        self.Y = np.load(PATH + "/%s_Y_%d.npy" % (self.name, self.class_n), mmap_mode="r")
        self.__shuffle()

    def __next_batch_from_the_end(self):
        elements_left = self.set_n % self.batch_size
        X = self.X[-elements_left:]
        Y = self.Y[-elements_left:]
        self.has_next = False
        return X, Y

    def __next_batch(self):
        batch_start = self.indexes[self.next_batch_index] * self.batch_size
        X = self.X[batch_start:batch_start + self.batch_size]
        Y = self.Y[batch_start:batch_start + self.batch_size]
        self.next_batch_index += 1
        return X, Y

    def __shuffle(self):
        np.random.shuffle(self.indexes)

    def random_x(self, n):
        indexes = np.random.choice(self.set_n, n)
        return self.X[indexes]








