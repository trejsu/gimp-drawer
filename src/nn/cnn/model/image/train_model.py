import sys
import tqdm
import argparse
import os
import json
import math

import tensorflow as tf
import matplotlib.pylab as plt

from src.nn.dataset.image.image_dataset import ImageDataset


ARGS = None
FILTER_SIZE = 5
CHANNELS = 3
MODEL_DIR = os.path.expandvars("$GIMP_PROJECT/out/model/")


def convolutional_network(image):
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

    # Map the ARGS.fc1 features to 9 action arguments
    with tf.name_scope('fc2'):
        W_fc2 = weight_variable([ARGS.fc1, 9])
        b_fc2 = bias_variable([9])

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


def main(_):
    x = tf.placeholder(tf.float32, [None, ARGS.size, ARGS.size, 3], name="x")
    y = tf.placeholder(tf.float32, [None, 9], name="y")
    y_conv, keep_prob = convolutional_network(x)

    with tf.name_scope('loss'):
        loss = tf.reduce_mean(tf.losses.mean_squared_error(labels=y, predictions=y_conv), name="loss")
        # loss = tf.reduce_mean(tf.square(tf.nn.sigmoid(y_conv) - y_))

    with tf.name_scope('optimizer'):
        train_step = tf.train.AdamOptimizer(ARGS.rate).minimize(loss)

    with tf.Session() as sess:

        saver = tf.train.Saver()
        sess.run(tf.global_variables_initializer())
        global_epoch = 0 if ARGS.model is None else int(ARGS.model.split('-')[-1])
        if global_epoch != 0:
            print("RESTORING")
            saver.restore(sess, ARGS.model)

        data = ImageDataset()

        mse_loss = []
        for epoch in tqdm.tqdm(range(global_epoch, ARGS.epoch)):

            num_batches = data.train.batch_n if ARGS.batch is None else ARGS.batch
            for step in tqdm.tqdm(range(num_batches)):
                X, Y, _ = data.train.next_batch()
                train_step.run(feed_dict={x: X, y: Y, keep_prob: ARGS.dropout})
                if step % 100 == 0:
                    train_error = loss.eval(feed_dict={x: X, y: Y, keep_prob: 1.0})
                    tqdm.tqdm.write('epoch %d, step %d, mean squared error %g' % (epoch + 1, step, train_error))
                    mse_loss.append(train_error)

            save_model(epoch + 1, saver, sess)
            save_learning_curve(mse_loss)


def save_learning_curve(mse_loss):
    plt.plot(mse_loss)
    plt.xlabel("step * 100")
    plt.ylabel("MSE")
    model_name = ARGS.name if ARGS.model is None else str(os.path.basename(ARGS.model))
    plt.savefig(MODEL_DIR + model_name + "_learning_curve.png")


def save_model(step, saver, sess):
    model_name = ARGS.name if ARGS.model is None else str(os.path.basename(ARGS.model))
    path = MODEL_DIR + model_name.split('-')[0]
    saver.save(sess, path, global_step=step)
    config = {"noise": ARGS.noise, "init": ARGS.init, "conv1": ARGS.conv1, "conv2": ARGS.conv2,
              "fc1": ARGS.fc1, "rate": ARGS.rate, "dropout": ARGS.dropout}
    with open(path + "_config.json", 'w+') as outfile:
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
    ARGS = parser.parse_args()
    tf.app.run(main=main, argv=sys.argv)
