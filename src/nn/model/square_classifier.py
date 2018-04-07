import sys
import tqdm
import argparse
import os
import json
import math

import tensorflow as tf
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from textwrap import wrap

sys.path.insert(0, os.path.realpath('../../'))
from nn.dataset.square.square_dataset import SquareDataset


ARGS = None
FILTER_SIZE = 5
CHANNELS = 1
MODEL_DIR = os.path.expandvars("$SQUARE_MODEL_PATH")
EPSILON = 1e-3

CONFIG = None


def conv_net(image, training):
    image = tf.reshape(image, [-1, ARGS.image_size, ARGS.image_size, 1])

    with tf.name_scope('conv1'):
        W_conv1 = weight_variable([FILTER_SIZE, FILTER_SIZE, CHANNELS, ARGS.conv1_filters])
        b_conv1 = bias_variable([ARGS.conv1_filters])
        conv1 = conv2d(image, W_conv1) + b_conv1
        if ARGS.batch_norm:
            conv1 = tf.layers.batch_normalization(conv1, center=True, scale=True, training=training)
        h_conv1 = tf.nn.relu(conv1)

    with tf.name_scope('pool1'):
        h_pool1 = max_pool_2x2(h_conv1)

    with tf.name_scope('conv2'):
        W_conv2 = weight_variable([FILTER_SIZE, FILTER_SIZE, ARGS.conv1_filters, ARGS.conv2_filters])
        b_conv2 = bias_variable([ARGS.conv2_filters])
        conv2 = conv2d(h_pool1, W_conv2) + b_conv2
        if ARGS.batch_norm:
            conv2 = tf.layers.batch_normalization(conv2, center=True, scale=True, training=training)
        h_conv2 = tf.nn.relu(conv2)

    with tf.name_scope('pool2'):
        h_pool2 = max_pool_2x2(h_conv2)

    with tf.name_scope('fc1'):
        image_size = int(math.ceil(ARGS.image_size / 4.))
        W_fc1 = weight_variable([image_size * image_size * ARGS.conv2_filters, ARGS.fc1_neurons])
        b_fc1 = bias_variable([ARGS.fc1_neurons])

        h_pool2_flat = tf.reshape(h_pool2, [-1, image_size * image_size * ARGS.conv2_filters])
        fc1 = tf.matmul(h_pool2_flat, W_fc1) + b_fc1
        if ARGS.batch_norm:
            fc1 = tf.layers.batch_normalization(fc1, center=True, scale=True, training=training)
        h_fc1 = tf.nn.relu(fc1)

    with tf.name_scope('dropout'):
        keep_prob = tf.placeholder(tf.float32, name="keep_prob")
        h_fc1_dropout = tf.nn.dropout(h_fc1, keep_prob)

    with tf.name_scope('fc2'):
        W_fc2 = weight_variable([ARGS.fc1_neurons, ARGS.classes])
        b_fc2 = bias_variable([ARGS.classes])

        y_conv = tf.add(tf.matmul(h_fc1_dropout, W_fc2), b_fc2, name="y_conv")

    return y_conv, keep_prob


def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')


def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')


def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=ARGS.weight_noise)
    return tf.Variable(initial, name="W")


def bias_variable(shape):
    initial = tf.constant(ARGS.bias_init, shape=shape)
    return tf.Variable(initial, name="b")


def get_one_hot(targets, nb_classes):
    return np.eye(nb_classes)[np.array(targets).reshape(-1)]


def main(_):
    x = tf.placeholder(tf.float32, [None, ARGS.image_size, ARGS.image_size], name="x")
    y = tf.placeholder(tf.float32, [None, ARGS.classes], name="y")
    training = tf.placeholder(tf.bool, name="training")
    y_conv, keep_prob = conv_net(x, training)

    with tf.name_scope('loss'):
        cross_entropy = tf.reduce_mean(
            tf.nn.softmax_cross_entropy_with_logits(labels=y, logits=y_conv), name="cross_entropy")

    with tf.name_scope('optimizer'):
        optimizer = tf.train.AdamOptimizer(ARGS.learning_rate)

    update_ops = tf.get_collection(tf.GraphKeys.UPDATE_OPS)
    with tf.control_dependencies(update_ops):
        train_op = optimizer.minimize(cross_entropy)

    with tf.name_scope('prediction'):
        correct_prediction = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32), name="accuracy")

    with tf.Session() as sess:

        saver = tf.train.Saver()
        sess.run(tf.global_variables_initializer())
        global_epoch = 0 if ARGS.model is None else int(ARGS.model.split('-')[-1])
        if global_epoch != 0:
            saver.restore(sess, ARGS.model)

        data = SquareDataset(ARGS.classes)

        loss = []
        for epoch in tqdm.tqdm(range(global_epoch, ARGS.epochs)):

            num_batches = data.train.batch_n if ARGS.batches is None else ARGS.batches
            for step in tqdm.tqdm(range(num_batches)):
                X, Y = data.train.next_batch()
                Y = get_one_hot(Y, ARGS.classes)
                _, cross_entropy_loss = sess.run([train_op, cross_entropy],
                                                 feed_dict={x: X, y: Y, keep_prob: ARGS.dropout,
                                                            training: True})
                loss.append(cross_entropy_loss)
                if step % 5 == 0:
                    train_accuracy = accuracy.eval(
                        feed_dict={x: X, y: Y, keep_prob: 1.0, training: True})
                    tqdm.tqdm.write('train accuracy %g' % train_accuracy)

            save_model(epoch + 1, saver, sess)
            save_learning_curve(loss)

        test_accuracy = np.zeros(100)
        data.test.next_batch()
        X, Y = data.test.X, data.test.Y
        for i in tqdm.tqdm(range(100)):
            prediction = accuracy.eval(feed_dict={x: np.expand_dims(X[i], 0),
                                                  y: get_one_hot(Y[i], ARGS.classes),
                                                  keep_prob: 1.0, training: False})
            test_accuracy[i] = prediction
        print("test accuracy = %g" % np.mean(test_accuracy))


def save_learning_curve(loss):
    plt.plot(loss)
    plt.xlabel('step')
    plt.ylabel('loss')
    model_name = ARGS.name if ARGS.model is None else str(os.path.basename(ARGS.model))
    config = ', '.join(['%s: %s' % (key, value) for key, value in CONFIG.items()])
    title = '%s %d epoch. %s' % (model_name, ARGS.epochs, config)
    plt.suptitle("\n".join(wrap(title, 60)))
    plt.savefig('%s/learning_curve/%s_%d_epoch.png' % (MODEL_DIR, model_name, ARGS.epochs))


def save_model(step, saver, sess):
    model_name = ARGS.name if ARGS.model is None else str(os.path.basename(ARGS.model))
    model_name = model_name.split('-')[0]
    model_dir = "%s/%s" % (MODEL_DIR, model_name)
    if not os.path.exists(model_dir):
        os.mkdir(model_dir)
    model_path = "%s/%s" % (model_dir, model_name)
    with open("%s_config.json" % model_path, 'w+') as outfile:
        json.dump(CONFIG, outfile)
    return saver.save(sess, model_path, global_step=step)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--model", type=str,
                        help="path to the partially trained model - when missing, the model will "
                             "be trained from scratch")
    parser.add_argument("--name", type=str, default="new_model",
                        help="name of new model - ignored when --model argument provided")
    parser.add_argument("--weight_noise", type=float, default=0.1,
                        help="weight variable stddev noise")
    parser.add_argument("---bias_init", default=0.1, type=float,
                        help="bias variable initial value")
    parser.add_argument("--conv1_filters", default=32, type=int,
                        help="number of filters in first convolutional layer")
    parser.add_argument("--conv2_filters", default=64, type=int,
                        help="number of filters in second convolutional layer")
    parser.add_argument("--fc1_neurons", default=512, type=int,
                        help="number of neurons in first fully connected layer")
    parser.add_argument("--learning_rate", type=float, default=0.0001, help="learning rate")
    parser.add_argument("--dropout", type=float, default=0.5, help="dropout")
    parser.add_argument("--epochs", type=int, default=100, help="epoch number")
    parser.add_argument("--image_size", type=int, default=100, help="image size")
    parser.add_argument("--batches", type=int,
                        help="number of batches to train in each epoch. whole training set if missing")
    parser.add_argument("--classes", type=int, help="number of classes (image parts)")
    parser.add_argument("--batch_norm", help="use batch normalization", action="store_true")
    ARGS = parser.parse_args()
    CONFIG = {"weight_noise": ARGS.weight_noise, "bias_init": ARGS.bias_init,
              "conv1_filters": ARGS.conv1_filters, "conv2_filters": ARGS.conv2_filters,
              "fc1": ARGS.fc1_neurons, "learning_rate": ARGS.learning_rate, "dropout": ARGS.dropout,
              "batch_norm": ARGS.batch_norm}
    tf.app.run(main=main, argv=sys.argv)
