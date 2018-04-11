import os
import math
import json

import numpy as np

from nn.dataset.dataset import Dataset


PATH = os.path.expandvars("$GIMP_PROJECT/dataset/")


class ImageDataset(Dataset):
    def __init__(self):
        with open(PATH + "config.json") as json_file:
            config = json.load(json_file)
        self.train = Set("train", config["train"], config["partSize"], config["batchSize"])
        self.test = Set("test", config["test"], config["partSize"], config["batchSize"])


class Set(object):
    def __init__(self, name, set_n, part_size, batch_size):
        self.name = name
        self.next_batch_index = 0
        self.part_n = int(math.ceil(set_n / float(part_size)))
        self.current_part = 1
        self.last_part_size = set_n % part_size
        self.batch_n = int(math.ceil(set_n / float(batch_size)))
        self.set_n = set_n
        self.X = None
        self.Y = None
        self.labels = None
        self.has_next = True
        self.batch_size = batch_size
        self.part_size = part_size
        self.indexes = np.array(range(self.batch_n))

    def next_batch(self):
        not_initialized = self.X is None or self.Y is None or self.labels is None
        if not_initialized:
            self.__load_current_part()

        last_part = self.current_part == self.part_n
        end_of_part = self.next_batch_index == (self.part_size - 1)
        end_of_last_part = self.next_batch_index == (self.last_part_size - 1)

        if last_part:
            X, Y, labels = self.__next_batch_from_the_end_of_the_last_part() if end_of_last_part \
                else self.__next_batch()
        else:
            X, Y, labels = self.__next_batch_from_the_end() if end_of_part \
                else self.__next_batch()
        return X, Y, labels

    def random(self):
        index, part = self.__get_random_part_and_index()
        X, Y, labels = self.__load_part(part)
        return X[index], Y[index], labels[index]

    def random_label(self):
        index, part = self.__get_random_part_and_index()
        labels = np.load(PATH + "%s_labels_%d.npy" % (self.name, part), mmap_mode="r")
        return labels[index]

    def __get_random_part_and_index(self):
        part = np.random.randint(1, self.part_n + 1)
        if part == self.part_n:
            index_upper_bound = self.last_part_size
        else:
            index_upper_bound = self.part_size
        index = np.random.randint(0, index_upper_bound)
        return index, part

    def __load_current_part(self):
        del self.X, self.Y, self.labels
        self.X = np.load(PATH + "%s_X_%d.npy" % (self.name, self.current_part), mmap_mode="r")
        self.Y = np.load(PATH + "%s_Y_%d.npy" % (self.name, self.current_part), mmap_mode="r")
        self.labels = np.load(
            PATH + "%s_labels_%d.npy" % (self.name, self.current_part), mmap_mode="r")
        self.__shuffle()

    def __load_part(self, part):
        return np.load(PATH + "%s_X_%d.npy" % (self.name, part), mmap_mode="r"), \
               np.load(PATH + "%s_Y_%d.npy" % (self.name, part), mmap_mode="r"), \
               np.load(PATH + "%s_labels_%d.npy" % (self.name, part), mmap_mode="r")

    def __next_batch_from_the_end_of_the_last_part(self):
        left_in_current_part = self.last_part_size % self.batch_size
        X = self.X[-left_in_current_part:]
        Y = self.Y[-left_in_current_part:]
        labels = self.labels[-left_in_current_part:]
        self.has_next = False
        return X, Y, labels

    def __next_batch_from_the_end(self):
        left_in_current_part = self.part_size % self.batch_size
        X = self.X[-left_in_current_part:]
        Y = self.Y[-left_in_current_part:]
        labels = self.labels[-left_in_current_part:]
        self.current_part += 1
        self.__load_current_part()
        self.next_batch_index = 0
        return X, Y, labels

    def __next_batch(self):
        batch_start = self.indexes[self.next_batch_index] * self.batch_size
        X = self.X[batch_start:batch_start + self.batch_size]
        Y = self.Y[batch_start:batch_start + self.batch_size]
        labels = self.labels[batch_start:batch_start + self.batch_size]
        self.next_batch_index += 1
        return X, Y, labels

    def __shuffle(self):
        np.random.shuffle(self.indexes)










