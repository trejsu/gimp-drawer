from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import tqdm
import getopt

import numpy as np
import tensorflow as tf


def read_test_set(data_dir):
    X = np.load(data_dir + "/test_X.npy", mmap_mode="r")
    Y = np.load(data_dir + "/test_Y.npy", mmap_mode="r")
    return {
        "X": X,
        "Y": Y,
    }


def main(argv):
    data_dir = "data/1125"
    data = read_test_set(data_dir)
    model_path = get_model_path(argv[1:])

    graph = tf.Graph()
    with graph.as_default():
        sess = tf.Session(graph=graph)
        saver = tf.train.import_meta_graph(model_path + ".meta")
        saver.restore(sess, model_path)

    y_ = graph.get_tensor_by_name("Placeholder_1:0")
    x = graph.get_tensor_by_name("Placeholder:0")
    keep_prob = graph.get_tensor_by_name("dropout/Placeholder:0")
    error = graph.get_tensor_by_name("Mean_1:0")

    with sess:
        for i in tqdm.tqdm(range(440)):
            batch_start = i * 50
            X = data["X"][batch_start:batch_start + 50]
            Y = data["Y"][batch_start:batch_start + 50]
            print('mse = %g' % error.eval(feed_dict={x: X, y_: Y, keep_prob: 1.0}))


def get_model_path(argv):
    model_path = None
    opts, args = getopt.getopt(argv, "m:")
    for opt, arg in opts:
        if opt == '-m':
            model_path = arg
    return model_path


if __name__ == '__main__':
    tf.app.run(main=main, argv=sys.argv)
