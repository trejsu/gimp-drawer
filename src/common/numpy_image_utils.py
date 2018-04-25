import numpy as np


def flatten_channels(image):
    return np.sum(image, axis=2) / 3
