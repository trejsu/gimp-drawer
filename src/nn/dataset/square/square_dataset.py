import os
import math

import numpy as np

from nn.dataset.dataset import Dataset


PATH = os.path.expandvars("$SQUARE_DATASET_PATH")
BATCH_SIZE = 50
TRAIN = 3500
TEST = 1500


class SquareDataset(Dataset):
    def __init__(self, class_n):
        self.train = Set("train", class_n, TRAIN)
        self.test = Set("test", class_n, TEST)


class Set(object):
    def __init__(self, name, class_n, set_n):
        self.name = name
        self.next_index = 0
        self.batch_n = int(math.ceil(set_n / float(BATCH_SIZE)))
        self.set_n = set_n
        self.X = None
        self.Y = None
        self.has_next = True
        self.class_n = class_n

    def next_batch(self):
        not_initialized = self.X is None or self.Y is None
        if not_initialized:
            self.__load()
        end = self.next_index + BATCH_SIZE >= self.set_n
        return self.__next_batch_from_the_end() if end else self.__next_batch()

    def __load(self):
        del self.X, self.Y
        self.X = np.load(PATH + "/%s_X.npy" % self.name, mmap_mode="r")
        self.Y = np.load(PATH + "/%s_Y_%d.npy" % (self.name, self.class_n), mmap_mode="r")
        self.__shuffle()

    def __next_batch_from_the_end(self):
        left = self.set_n - self.next_index
        X = self.X[-left:]
        Y = self.Y[-left:]
        self.has_next = False
        return X, Y

    def __next_batch(self):
        X = self.X[self.next_index:self.next_index + BATCH_SIZE]
        Y = self.Y[self.next_index:self.next_index + BATCH_SIZE]
        self.next_index += BATCH_SIZE
        return X, Y

    def __shuffle(self):
        indexes = np.arange(self.X.shape[0])
        np.random.shuffle(indexes)
        self.X = self.X[indexes]
        self.Y = self.Y[indexes]








