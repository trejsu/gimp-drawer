from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import tempfile
import tqdm

import numpy as np
import tensorflow as tf


def convolutional_network(image):
    # First convolutional layer - maps one grayscale image to 32 feature maps.
    with tf.name_scope('conv1'):
        W_conv1 = weight_variable([5, 5, 3, 32])
        b_conv1 = bias_variable([32])
        h_conv1 = tf.nn.relu(conv2d(image, W_conv1) + b_conv1)

    # Pooling layer - downsamples by 2X.
    with tf.name_scope('pool1'):
        h_pool1 = max_pool_2x2(h_conv1)

    # Second convolutional layer -- maps 32 feature maps to 64.
    with tf.name_scope('conv2'):
        W_conv2 = weight_variable([5, 5, 32, 64])
        b_conv2 = bias_variable([64])
        h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)

    # Second pooling layer.
    with tf.name_scope('pool2'):
        h_pool2 = max_pool_2x2(h_conv2)

    # Fully connected layer 1 -- after 2 round of downsampling, our 100x100 image
    # is down to 25x25x64 feature maps -- maps this to 512 features.
    with tf.name_scope('fc1'):
        W_fc1 = weight_variable([25 * 25 * 64, 512])
        b_fc1 = bias_variable([512])

        h_pool2_flat = tf.reshape(h_pool2, [-1, 25 * 25 * 64])
        h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

    # Dropout - controls the complexity of the model, prevents co-adaptation of
    # features.
    with tf.name_scope('dropout'):
        keep_prob = tf.placeholder(tf.float32)
        h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

    # Map the 512 features to 9 action arguments
    with tf.name_scope('fc2'):
        W_fc2 = weight_variable([512, 9])
        b_fc2 = bias_variable([9])

        y_conv = tf.matmul(h_fc1_drop, W_fc2) + b_fc2
    return y_conv, keep_prob


def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')


def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')


def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)


def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)


def read_data_sets(data_dir):
    def load(name): return np.load(data_dir + name, mmap_mode="r")

    test_X = load("/test_X.npy")
    train_X = load("/train_X.npy")
    test_Y = load("/test_Y.npy")
    train_Y = load("/train_Y.npy")
    test_labels = load("/test_labels.npy")
    train_labels = load("/train_labels.npy")
    return {
        "train": {
            "X": train_X,
            "Y": train_Y,
            "labels": train_labels
        },
        "test": {
            "X": test_X,
            "Y": test_Y,
            "labels": test_labels
        }
    }


def main(_):
    data_dir = "data/1125"
    data = read_data_sets(data_dir)

    x = tf.placeholder(tf.float32, [None, 100, 100, 3])
    y_ = tf.placeholder(tf.float32, [None, 9])
    y_conv, keep_prob = convolutional_network(x)

    with tf.name_scope('loss'):
        mean_squared_error = tf.losses.mean_squared_error(labels=y_, predictions=y_conv)
    mean_squared_error = tf.reduce_mean(mean_squared_error)

    with tf.name_scope('adam_optimizer'):
        train_step = tf.train.AdamOptimizer(1e-4).minimize(mean_squared_error)

    with tf.name_scope('accuracy'):
        correct_prediction = mean_squared_error
    accuracy = tf.reduce_mean(correct_prediction)

    graph_location = tempfile.mkdtemp()
    print('Saving graph to: %s' % graph_location)
    train_writer = tf.summary.FileWriter(graph_location)
    train_writer.add_graph(tf.get_default_graph())

    with tf.Session() as sess:

        saver = tf.train.Saver()
        sess.run(tf.global_variables_initializer())
        # step = 1700
        # saver.restore(sess, "./my-model-%d" % step)

        for i in tqdm.tqdm(range(1759)):

            batch_start = i * 50
            train_X = data["train"]["X"][batch_start:batch_start + 50]
            train_Y = data["train"]["Y"][batch_start:batch_start + 50]

            if i % 100 == 0:
                train_accuracy = accuracy.eval(
                    feed_dict={x: train_X, y_: train_Y, keep_prob: 1.0})
                print('step %d, mean squared error %g' % (i, train_accuracy))
                if i != 0:
                    saver.save(sess, './hopefully-improved-model', global_step=i)

            train_step.run(feed_dict={x: train_X, y_: train_Y, keep_prob: 0.5})

        for i in tqdm.tqdm(range(440)):
            batch_start = i * 50
            test_X = data["test"]["X"][batch_start:batch_start + 50]
            test_Y = data["test"]["Y"][batch_start:batch_start + 50]
            print('mse = %g' % accuracy.eval(
                feed_dict={x: test_X, y_: test_Y, keep_prob: 1.0}))


if __name__ == '__main__':
    tf.app.run(main=main, argv=[sys.argv[0]])
