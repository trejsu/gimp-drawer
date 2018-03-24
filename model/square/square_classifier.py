import sys
import tqdm
import argparse
import os
import json
import math

import tensorflow as tf
import matplotlib.pylab as plt
import numpy as np

from model.square.dataset import DataSet


ARGS = None
FILTER_SIZE = 5
CHANNELS = 1
MODEL_DIR = os.path.expandvars("$GIMP_PROJECT/out/model/square/")


def convolutional_network(image):
    image = tf.reshape(image, [-1, ARGS.size, ARGS.size, 1])
    # First convolutional layer - maps image to ARGS.conv1 feature maps.
    with tf.name_scope('conv1'):
        W_conv1 = weight_variable([FILTER_SIZE, FILTER_SIZE, CHANNELS, ARGS.conv1])
        b_conv1 = bias_variable([ARGS.conv1])
        h_conv1 = tf.nn.relu(conv2d(image, W_conv1) + b_conv1)

    # Pooling layer - downsamples by 2X.
    with tf.name_scope('pool1'):
        h_pool1 = max_pool_2x2(h_conv1)

    # Second convolutional layer - maps ARGS.conv1 feature maps to ARGS.conv2.
    with tf.name_scope('conv2'):
        W_conv2 = weight_variable([FILTER_SIZE, FILTER_SIZE, ARGS.conv1, ARGS.conv2])
        b_conv2 = bias_variable([ARGS.conv2])
        h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)

    # Second pooling layer.
    with tf.name_scope('pool2'):
        h_pool2 = max_pool_2x2(h_conv2)

    # Fully connected layer 1 - after 2 round of downsampling, our ARGS.size x ARGS.size image
    # is down to ARGS.SIZE / 4 x ARGS.SIZE / 4 x ARGS.conv2 feature maps -- maps this to ARGS.fc1 features.
    with tf.name_scope('fc1'):
        image_size = int(math.ceil(ARGS.size / 4.))
        W_fc1 = weight_variable([image_size * image_size * ARGS.conv2, ARGS.fc1])
        b_fc1 = bias_variable([ARGS.fc1])

        h_pool2_flat = tf.reshape(h_pool2, [-1, image_size * image_size * ARGS.conv2])
        h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

    # Dropout - controls the complexity of the model, prevents co-adaptation of features.
    with tf.name_scope('dropout'):
        keep_prob = tf.placeholder(tf.float32, name="keep_prob")
        h_fc1_dropout = tf.nn.dropout(h_fc1, keep_prob)

    # Map the ARGS.fc1 features to ARGS.classes action arguments
    with tf.name_scope('fc2'):
        W_fc2 = weight_variable([ARGS.fc1, ARGS.classes])
        b_fc2 = bias_variable([ARGS.classes])

        y_conv = tf.add(tf.matmul(h_fc1_dropout, W_fc2), b_fc2, name="y_conv")

    return y_conv, keep_prob


def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')


def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')


def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=ARGS.noise)
    return tf.Variable(initial, name="W")


def bias_variable(shape):
    initial = tf.constant(ARGS.init, shape=shape)
    return tf.Variable(initial, name="b")


def get_one_hot(targets, nb_classes):
    return np.eye(nb_classes)[np.array(targets).reshape(-1)]


def main(_):
    x = tf.placeholder(tf.float32, [None, ARGS.size, ARGS.size], name="x")
    y = tf.placeholder(tf.float32, [None, ARGS.classes], name="y")
    y_conv, keep_prob = convolutional_network(x)

    with tf.name_scope('loss'):
        cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y, logits=y_conv), name="cross_entropy")

    with tf.name_scope('optimizer'):
        train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)

    with tf.name_scope('prediction'):
        correct_prediction = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32), name="accuracy")

    with tf.Session() as sess:

        saver = tf.train.Saver()
        sess.run(tf.global_variables_initializer())
        global_epoch = 0 if ARGS.model is None else int(ARGS.model.split('-')[-1])
        if global_epoch != 0:
            saver.restore(sess, ARGS.model)

        data = DataSet(ARGS.classes)

        loss = []
        for epoch in tqdm.tqdm(range(global_epoch, ARGS.epoch)):

            num_batches = data.train.batch_n if ARGS.batch is None else ARGS.batch
            for step in tqdm.tqdm(range(num_batches)):
                X, Y = data.train.next_batch()
                Y = get_one_hot(Y, ARGS.classes)
                train_step.run(feed_dict={x: X, y: Y, keep_prob: ARGS.dropout})
                cross_entropy_loss = cross_entropy.eval(feed_dict={x: X, y: Y, keep_prob: 1.0})
                loss.append(cross_entropy_loss)
                if step == 0:
                    tqdm.tqdm.write('train accuracy %g' % cross_entropy_loss)

            save_model(epoch + 1, saver, sess)
            save_learning_curve(loss)

        mean_test_accuracy = np.zeros(data.test.batch_n)
        for i in tqdm.tqdm(range(data.test.batch_n)):
            X, Y = data.test.next_batch()
            Y = get_one_hot(Y, ARGS.classes)
            test_accuracy = accuracy.eval(feed_dict={x: X, y: Y, keep_prob: 1.0})
            mean_test_accuracy[i] = test_accuracy
            tqdm.tqdm.write('test accuracy %g' % test_accuracy)
        print("average test accuracy = %g" % np.mean(mean_test_accuracy))


def save_learning_curve(loss):
    plt.plot(loss)
    plt.xlabel("step")
    plt.ylabel("loss")
    model_name = ARGS.name if ARGS.model is None else str(os.path.basename(ARGS.model))
    plt.title("%s %d epoch" % (model_name, ARGS.epoch))
    plt.savefig("%s%s_%d_epoch.png" % (MODEL_DIR, model_name, ARGS.epoch))


def save_model(step, saver, sess):
    model_name = ARGS.name if ARGS.model is None else str(os.path.basename(ARGS.model))
    path = "%s%s" % (MODEL_DIR, model_name.split('-')[0])
    saver.save(sess, path, global_step=step)
    config = {"noise": ARGS.noise, "init": ARGS.init, "conv1": ARGS.conv1, "conv2": ARGS.conv2,
              "fc1": ARGS.fc1, "rate": ARGS.rate, "dropout": ARGS.dropout}
    with open("%s_config.json" % path, 'w+') as outfile:
        json.dump(config, outfile)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-m", "--model", type=str,
                        help="path to the partially trained model - when missing, the model will "
                             "be trained from scratch")
    parser.add_argument("--name", type=str, default="new_model",
                        help="name of new model - ignored when --model argument provided")
    parser.add_argument("--noise", type=float, default=0.1, help="weight variable stddev noise")
    parser.add_argument("-i", "---init", default=0.1, type=float,
                        help="bias variable initial value")
    parser.add_argument("--conv1", default=32, type=int,
                        help="number of filters in first convolutional layer")
    parser.add_argument("--conv2", default=64, type=int,
                        help="number of filters in second convolutional layer")
    parser.add_argument("-f", "--fc1", default=512, type=int,
                        help="number of neurons in first fully connected layer")
    parser.add_argument("-r", "--rate", type=float, default=0.0001, help="learning rate")
    parser.add_argument("-d", "--dropout", type=float, default=0.5, help="dropout")
    parser.add_argument("-e", "--epoch", type=int, default=100, help="epoch number")
    parser.add_argument("-s", "--size", type=int, default=100, help="image size")
    parser.add_argument("-b", "--batch", type=int, help="number of batches to train in each epoch. whole training set if missing")
    parser.add_argument("--classes", type=int, help="number of classes (image parts)")
    ARGS = parser.parse_args()
    tf.app.run(main=main, argv=sys.argv)
