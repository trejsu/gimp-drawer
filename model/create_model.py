from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import getopt

import tensorflow as tf


def convolutional_network(image):
    # First convolutional layer - maps image to 32 feature maps.
    with tf.name_scope('conv1'):
        W_conv1 = weight_variable([5, 5, 3, 32])
        b_conv1 = bias_variable([32])
        h_conv1 = tf.nn.relu(conv2d(image, W_conv1) + b_conv1)

    # Pooling layer - downsamples by 2X.
    with tf.name_scope('pool1'):
        h_pool1 = max_pool_2x2(h_conv1)

    # Second convolutional layer - maps 32 feature maps to 64.
    with tf.name_scope('conv2'):
        W_conv2 = weight_variable([5, 5, 32, 64])
        b_conv2 = bias_variable([64])
        h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)

    # Second pooling layer.
    with tf.name_scope('pool2'):
        h_pool2 = max_pool_2x2(h_conv2)

    # Fully connected layer 1 - after 2 round of downsampling, our 100x100 image
    # is down to 25x25x64 feature maps -- maps this to 512 features.
    with tf.name_scope('fully_connected1'):
        W_fully_conn1 = weight_variable([25 * 25 * 64, 512])
        b_fully_conn1 = bias_variable([512])

        h_pool2_flat = tf.reshape(h_pool2, [-1, 25 * 25 * 64])
        h_fully_conn1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fully_conn1) + b_fully_conn1)

    # Dropout - controls the complexity of the model, prevents co-adaptation of features.
    with tf.name_scope('dropout'):
        keep_prob = tf.placeholder(tf.float32)
        h_fully_conn1_dropout = tf.nn.dropout(h_fully_conn1, keep_prob)

    # Map the 512 features to 9 action arguments
    with tf.name_scope('fully_connected2'):
        W_fully_conn2 = weight_variable([512, 9])
        b_fully_conn2 = bias_variable([9])

        y_conv = tf.matmul(h_fully_conn1_dropout, W_fully_conn2) + b_fully_conn2

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


def main(argv):
    model_path = get_model_path(argv[1:])

    x = tf.placeholder(tf.float32, [None, 100, 100, 3])
    y_ = tf.placeholder(tf.float32, [None, 9])
    y_conv, keep_prob = convolutional_network(x)

    with tf.Session() as sess:
        saver = tf.train.Saver()
        sess.run(tf.global_variables_initializer())
        model_location = saver.save(sess, model_path, global_step=0)
        print("model saved to location: %s" % model_location)


def get_model_path(argv):
    model_path = "./new_model"
    opts, args = getopt.getopt(argv, "m:")
    for opt, arg in opts:
        if opt == '-m':
            model_path = arg
    return model_path


if __name__ == '__main__':
    tf.app.run(main=main, argv=sys.argv)
