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
        self.next_index = 0
        self.batch_n = int(math.ceil(set_n / float(batch_size)))
        self.set_n = set_n
        self.X = None
        self.Y = None
        self.has_next = True
        self.class_n = class_n
        self.batch_size = batch_size

    def next_batch(self):
        not_initialized = self.X is None or self.Y is None
        if not_initialized:
            self.__load()
        end = self.next_index + self.batch_size >= self.set_n
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
        X = self.X[self.next_index:self.next_index + self.batch_size]
        Y = self.Y[self.next_index:self.next_index + self.batch_size]
        self.next_index += self.batch_size
        return X, Y

    def __shuffle(self):
        seed = np.random.randint(0, 1000)

        def shuffle_with_seed(data):
            np.random.seed(seed)
            np.random.shuffle(data)

        shuffle_with_seed(self.X)
        shuffle_with_seed(self.Y)

    def random_x(self, n):
        indexes = np.random.choice(self.set_n, n)
        return self.X[indexes]








