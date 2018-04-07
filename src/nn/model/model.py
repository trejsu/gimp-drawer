import os
import json
import math
from textwrap import wrap

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import tensorflow as tf


MODEL_DIR = os.path.expandvars("$SQUARE_MODEL_PATH")
FILTER_SIZE = 5


class Model(object):
    def __init__(self, args, channels, outputs):
        self.model = args.model
        self.name = args.name
        self.epochs = args.epochs
        self.conv1_filters = args.conv1_filters
        self.conv2_filters = args.conv2_filters
        self.fc1_neurons = args.fc1_neurons
        self.learning_rate = args.learning_rate
        self.dropout = args.dropout
        self.batch_norm = args.batch_norm
        self.image_size = args.image_size
        self.channels = channels
        self.outputs = outputs

    def save_learning_curve(self, loss):
        plt.plot(loss)
        plt.xlabel('step')
        plt.ylabel('loss')
        model_name = self.name if self.model is None else str(os.path.basename(self.model))
        config = ', '.join(['%s: %s' % (key, value) for key, value in self._get_config().items()])
        title = '%s %d epoch. %s' % (model_name, self.epochs, config)
        plt.suptitle("\n".join(wrap(title, 60)))
        plt.savefig('%s/learning_curve/%s_%d_epoch.png' % (MODEL_DIR, model_name, self.epochs))

    def save(self, step, saver, sess):
        model_name = self.name if self.model is None else str(os.path.basename(self.model))
        model_name = model_name.split('-')[0]
        model_dir = "%s/%s" % (MODEL_DIR, model_name)
        if not os.path.exists(model_dir):
            os.mkdir(model_dir)
        model_path = "%s/%s" % (model_dir, model_name)
        with open("%s_config.json" % model_path, 'w+') as outfile:
            json.dump(self._get_config(), outfile)
        return saver.save(sess, model_path, global_step=step)

    def save_test_result_with_parameters(self, score):
        raise NotImplementedError

    def _get_config(self):
        return {"conv1_filters": self.conv1_filters, "conv2_filters": self.conv2_filters,
                "fc1": self.fc1_neurons, "learning_rate": self.learning_rate,
                "dropout": self.dropout, "batch_norm": self.batch_norm}

    def conv_net(self, image, training):
        image = tf.reshape(image, [-1, self.image_size, self.image_size, self.channels])

        with tf.name_scope('conv1'):
            W_conv1 = weight_variable([FILTER_SIZE, FILTER_SIZE, self.channels, self.conv1_filters])
            b_conv1 = bias_variable([self.conv1_filters])
            conv1 = conv2d(image, W_conv1) + b_conv1
            if self.batch_norm:
                conv1 = tf.layers.batch_normalization(conv1, center=True, scale=True,
                                                      training=training)
            h_conv1 = tf.nn.relu(conv1)

        with tf.name_scope('pool1'):
            h_pool1 = max_pool_2x2(h_conv1)

        with tf.name_scope('conv2'):
            W_conv2 = weight_variable(
                [FILTER_SIZE, FILTER_SIZE, self.conv1_filters, self.conv2_filters])
            b_conv2 = bias_variable([self.conv2_filters])
            conv2 = conv2d(h_pool1, W_conv2) + b_conv2
            if self.batch_norm:
                conv2 = tf.layers.batch_normalization(conv2, center=True, scale=True,
                                                      training=training)
            h_conv2 = tf.nn.relu(conv2)

        with tf.name_scope('pool2'):
            h_pool2 = max_pool_2x2(h_conv2)

        with tf.name_scope('fc1'):
            image_size = int(math.ceil(self.image_size / 4.))
            W_fc1 = weight_variable(
                [image_size * image_size * self.conv2_filters, self.fc1_neurons])
            b_fc1 = bias_variable([self.fc1_neurons])

            h_pool2_flat = tf.reshape(h_pool2, [-1, image_size * image_size * self.conv2_filters])
            fc1 = tf.matmul(h_pool2_flat, W_fc1) + b_fc1
            if self.batch_norm:
                fc1 = tf.layers.batch_normalization(fc1, center=True, scale=True, training=training)
            h_fc1 = tf.nn.relu(fc1)

        with tf.name_scope('dropout'):
            keep_prob = tf.placeholder(tf.float32, name="keep_prob")
            h_fc1_dropout = tf.nn.dropout(h_fc1, keep_prob)

        with tf.name_scope('fc2'):
            y_conv = self.fc2_layer(h_fc1_dropout)

        return y_conv, keep_prob

    def fc2_layer(self, h_fc1_dropout):
        W_fc2 = weight_variable([self.fc1_neurons, self.outputs])
        b_fc2 = bias_variable([self.outputs])
        y_conv = tf.add(tf.matmul(h_fc1_dropout, W_fc2), b_fc2, name="y_conv")
        return y_conv

    def restore_if_not_new(self, sess):
        saver = tf.train.Saver()
        sess.run(tf.global_variables_initializer())
        global_epoch = 0 if self.model is None else int(self.model.split('-')[-1])
        if global_epoch != 0:
            saver.restore(sess, self.model)
        return global_epoch, saver


def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')


def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')


def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial, name="W")


def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial, name="b")




