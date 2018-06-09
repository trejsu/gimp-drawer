import os.path as path
import json
import math
import numpy as np


class Dataset(object):
    def next_batch(self):
        raise NotImplementedError

    def random(self):
        raise NotImplementedError

    def random_x(self):
        raise NotImplementedError

    def random_y(self):
        raise NotImplementedError

    def restart(self):
        raise NotImplementedError


class MultipartDataset(object):
    def __init__(self, dataset_path, batch_size):
        with open(path.join(dataset_path, 'config.json')) as config_file:
            config = json.load(config_file)
        self.train = MultipartSet('train', config['train'], config['partSize'], batch_size,
                                  dataset_path)
        self.test = MultipartSet('test', config['test'], config['partSize'], batch_size,
                                 dataset_path)


class MultipartSet(Dataset):
    def __init__(self, name, set_size, part_size, batch_size, dataset_path):
        super(MultipartSet, self).__init__()
        self.name = name
        self.set_size = set_size
        self.part_size = part_size
        self.batch_size = batch_size
        self.X = None
        self.Y = None
        self.next_batch_index = 0
        self.num_parts = int(math.ceil(set_size / float(part_size)))
        self.current_part = 1
        self.last_part_size = set_size % part_size
        self.num_batches = int(math.ceil(set_size / float(batch_size)))
        self.has_next = True
        self.indexes = np.array(range(self.num_batches))
        self.dataset_path = dataset_path

    def next_batch(self):
        not_initialized = self.X is None or self.Y is None
        if not_initialized:
            self._load_current_part()

        last_part = self.current_part == self.num_parts
        end_of_part = self.next_batch_index == (self.part_size - 1)
        end_of_last_part = self.next_batch_index == (self.last_part_size - 1)

        if last_part:
            X, Y = self._next_batch_from_the_end_of_the_last_part() if end_of_last_part \
                else self._next_batch()
        else:
            X, Y = self._next_batch_from_the_end() if end_of_part else self._next_batch()
        return X, Y

    def random(self):
        index, part = self._get_random_part_and_index()
        X, Y = self._load_part(part)
        return X[index], Y[index]

    def random_x(self):
        return self._random_part('X')

    def random_y(self):
        return self._random_part('Y')

    def restart(self):
        self.next_batch_index = 0
        self._shuffle()
        self.has_next = True

    def _random_part(self, name):
        index, part = self._get_random_part_and_index()
        x = np.load(path.join(self.dataset_path, "{}_{}_{}.npy".format(self.name, name, part)),
                    mmap_mode="r")
        return x[index]

    def _get_random_part_and_index(self):
        part = np.random.randint(1, self.num_parts + 1)
        if part == self.num_parts:
            index_upper_bound = self.last_part_size
        else:
            index_upper_bound = self.part_size
        index = np.random.randint(0, index_upper_bound)
        return index, part

    def _load_current_part(self):
        del self.X, self.Y
        self.X = np.load(path.join(self.dataset_path, "{}_X_{}.npy".format(self.name,
                                                                           self.current_part)),
                         mmap_mode="r")
        self.Y = np.load(path.join(self.dataset_path, "{}_Y_{}.npy".format(self.name,
                                                                           self.current_part)),
                         mmap_mode="r")
        self._shuffle()

    def _load_part(self, part):
        return np.load(path.join(self.dataset_path, "{}_X_{}.npy".format(self.name, part)),
                       mmap_mode="r"), \
               np.load(path.join(self.dataset_path, "{}_Y_{}.npy".format(self.name, part)),
                       mmap_mode="r")

    def _next_batch_from_the_end_of_the_last_part(self):
        left_in_current_part = self.last_part_size % self.batch_size
        X = self.X[-left_in_current_part:]
        Y = self.Y[-left_in_current_part:]
        self.has_next = False
        return X, Y

    def _next_batch_from_the_end(self):
        left_in_current_part = self.part_size % self.batch_size
        X = self.X[-left_in_current_part:]
        Y = self.Y[-left_in_current_part:]
        self.current_part += 1
        self._load_current_part()
        self.next_batch_index = 0
        return X, Y

    def _next_batch(self):
        batch_start = self.indexes[self.next_batch_index] * self.batch_size
        X = self.X[batch_start:batch_start + self.batch_size]
        Y = self.Y[batch_start:batch_start + self.batch_size]
        self.next_batch_index += 1
        return X, Y

    def _shuffle(self):
        np.random.shuffle(self.indexes)


class OnePartDataset(object):
    def __init__(self, dataset_path, batch_size):
        with open(path.join(dataset_path, 'config.json')) as config_file:
            config = json.load(config_file)
        self.train = OnePartSet('train', config['train'], batch_size, dataset_path)
        self.test = OnePartSet('test', config['test'], batch_size, dataset_path)


class OnePartSet(Dataset):
    def __init__(self, name, set_size, batch_size, dataset_path):
        self.name = name
        self.set_size = set_size
        self.batch_size = batch_size
        self.dataset_path = dataset_path
        self.X = None
        self.Y = None
        self.num_batches = int(math.ceil(set_size / float(batch_size)))
        self.indexes = np.array(range(self.num_batches))
        self.next_batch_index = 0
        self.has_next = True

    def next_batch(self):
        not_initialized = self.X is None or self.Y is None
        if not_initialized:
            self._load()
        end = self.next_batch_index == (self.set_size - 1)
        return self._next_batch_from_the_end() if end else self._default_next_batch()

    def random(self):
        indexes = np.random.choice(self.set_size, 1)
        return self.X[indexes], self.Y[indexes]

    def random_x(self):
        indexes = np.random.choice(self.set_size, 1)
        return self.X[indexes]

    def random_y(self):
        indexes = np.random.choice(self.set_size, 1)
        return self.Y[indexes]

    def restart(self):
        self.next_batch_index = 0
        self._shuffle()
        self.has_next = True

    def _load(self):
        del self.X, self.Y
        self.X = np.load(path.join(self.dataset_path, "{}_X.npy".format(self.name)), mmap_mode="r")
        self.Y = np.load(path.join(self.dataset_path, "{}_Y.npy".format(self.name)), mmap_mode="r")
        self._shuffle()

    def _shuffle(self):
        np.random.shuffle(self.indexes)

    def _next_batch_from_the_end(self):
        elements_left = self.set_size % self.batch_size
        X = self.X[-elements_left:]
        Y = self.Y[-elements_left:]
        self.has_next = False
        return X, Y

    def _default_next_batch(self):
        batch_start = self.indexes[self.next_batch_index] * self.batch_size
        X = self.X[batch_start:batch_start + self.batch_size]
        Y = self.Y[batch_start:batch_start + self.batch_size]
        self.next_batch_index += 1
        return X, Y
