import os
import math

import numpy as np


PATH = os.path.expandvars("$GIMP_PROJECT/diffs/")
# PATH = os.path.expandvars("$GIMP_PROJECT/model/diffs/")
PART_SIZE = 70000
# PART_SIZE = 50
TRAIN = 689368
# TRAIN = 869
TEST = 172577
# TEST = 313
BATCH_SIZE = 200
# BATCH_SIZE = 4


class DataSet(object):
    def __init__(self):
        self.train = Set("train", TRAIN)
        self.test = Set("test", TEST)


class Set(object):
    def __init__(self, name, set_n):
        self.name = name
        self.next_index = 0
        self.part_n = math.ceil(set_n / float(PART_SIZE))
        self.current_part = 1
        self.last_part_size = set_n % PART_SIZE
        self.batch_n = int(math.ceil(set_n / float(BATCH_SIZE)))
        self.set_n = set_n
        self.X = None
        self.Y = None
        self.labels = None
        self.has_next = True
        self.__load_current_part()

    def next_batch(self):
        last_part = self.current_part == self.part_n
        end_of_part = self.next_index + BATCH_SIZE >= PART_SIZE
        end_of_last_part = self.next_index + BATCH_SIZE >= self.last_part_size

        if last_part:
            X, Y, labels = self.__next_batch_from_last_part() if end_of_last_part \
                else self.__next_batch_from_same_part()
        else:
            X, Y, labels = self.__next_batch_from_different_parts() if end_of_part \
                else self.__next_batch_from_same_part()
        return X, Y, labels

    def random(self):
        part = np.random.randint(1, self.last_part_size + 1)
        if part == self.part_n:
            index_upper_bound = self.last_part_size
        else:
            index_upper_bound = PART_SIZE
        index = np.random.randint(0, index_upper_bound)
        X, Y, labels = self.__load_part(part)
        return X[index], Y[index], labels[index]

    def __load_current_part(self):
        del self.X, self.Y, self.labels
        self.X = np.load(PATH + "%s_X_%d.npy" % (self.name, self.current_part), mmap_mode="r")
        self.Y = np.load(PATH + "%s_Y_%d.npy" % (self.name, self.current_part), mmap_mode="r")
        self.labels = np.load(
            PATH + "%s_labels_%d.npy" % (self.name, self.current_part), mmap_mode="r")

    def __load_part(self, part):
        return np.load(PATH + "%s_X_%d.npy" % (self.name, part), mmap_mode="r"), \
               np.load(PATH + "%s_Y_%d.npy" % (self.name, part), mmap_mode="r"), \
               np.load(PATH + "%s_labels_%d.npy" % (self.name, part), mmap_mode="r")

    def __next_batch_from_last_part(self):
        left_in_current_part = (self.last_part_size - self.next_index)
        X = self.X[-left_in_current_part:]
        Y = self.Y[-left_in_current_part:]
        labels = self.labels[-left_in_current_part:]
        self.has_next = False
        return X, Y, labels

    def __next_batch_from_different_parts(self):
        left_in_current_part = (PART_SIZE - self.next_index)
        X = self.X[-left_in_current_part:]
        Y = self.Y[-left_in_current_part:]
        labels = self.labels[-left_in_current_part:]
        self.current_part += 1
        self.__load_current_part()
        self.next_index = 0
        return X, Y, labels

    def __next_batch_from_same_part(self):
        X = self.X[self.next_index:self.next_index + BATCH_SIZE]
        Y = self.Y[self.next_index:self.next_index + BATCH_SIZE]
        labels = self.labels[self.next_index:self.next_index + BATCH_SIZE]
        self.next_index += BATCH_SIZE
        return X, Y, labels







