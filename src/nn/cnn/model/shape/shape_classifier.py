import sys
import tqdm
import argparse
import os

import tensorflow as tf
import numpy as np

from src.nn.cnn.model.model import Model
from src.nn.cnn.dataset.dataset import MultipartDataset


ARGS = None


class ShapeClassifier(Model):
    def __init__(self, args):
        super(ShapeClassifier, self).__init__(args, args.channels, args.classes)

    def save_test_result_with_parameters(self, score):
        with open('results.txt', mode='a') as f:
            f.write('score = %s, python shape_classifier.py --name %s --epochs %s --classes %s '
                    '--conv1_filters %s --conv2_filters %s --fc1_neurons %s --learning_rate %s '
                    '--dropout %s\n' % (score, self.name, self.epochs, self.outputs,
                                        self.conv1_filters, self.conv2_filters, self.fc1_neurons,
                                        self.learning_rate, self.dropout))


def main(_):
    x = tf.placeholder(tf.float32, [None, ARGS.image_size, ARGS.image_size, ARGS.channels], name="x")
    y = tf.placeholder(tf.int32, [None, ARGS.classes], name="y")
    training = tf.placeholder(tf.bool, name="training")

    model = ShapeClassifier(ARGS)

    y_conv, keep_prob = model.conv_net(x, training)

    with tf.name_scope('loss'):
        cross_entropy = tf.reduce_mean(
            tf.nn.softmax_cross_entropy_with_logits_v2(labels=y, logits=y_conv),
            name="cross_entropy")

    with tf.name_scope('optimizer'):
        optimizer = tf.train.AdamOptimizer(ARGS.learning_rate)

    train_op = optimizer.minimize(cross_entropy)

    with tf.name_scope('prediction'):
        correct_prediction = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32), name="accuracy")

    with tf.Session() as sess:

        global_epoch, saver = model.restore_if_not_new(sess)

        data = MultipartDataset(ARGS.dataset_path, ARGS.batch_size)

        if not ARGS.test:
            best_accuracy = 0
            epochs_not_improving = 0

            for epoch in tqdm.tqdm(range(global_epoch, ARGS.epochs)):

                num_batches = data.train.num_batches if ARGS.batches is None else ARGS.batches
                for step in tqdm.tqdm(range(num_batches)):
                    X, Y = data.train.next_batch()
                    train_op.run(feed_dict={x: X, y: Y, keep_prob: ARGS.dropout, training: True})
                    if step == 0:
                        train_accuracy = accuracy.eval(
                            feed_dict={x: X, y: Y, keep_prob: 1.0, training: True})
                        tqdm.tqdm.write('train accuracy %g' % train_accuracy)

                test_accuracy = evaluate_test_accuracy(accuracy, data, keep_prob, training, x, y)
                tqdm.tqdm.write('test accuracy %g' % test_accuracy)

                if test_accuracy > best_accuracy:
                    current_epoch = epoch + 1
                    model.save(current_epoch, saver, sess)
                    best_accuracy = test_accuracy
                    epochs_not_improving = 0
                else:
                    epochs_not_improving += 1

                if epochs_not_improving >= ARGS.early_stopping_epochs:
                    break

                data.train.restart()

        mean_test_accuracy = evaluate_test_accuracy(accuracy, data, keep_prob, training, x, y)
        model.save_test_result_with_parameters(mean_test_accuracy)


def evaluate_test_accuracy(accuracy, data, keep_prob, training, x, y):
    test_accuracy = np.zeros(data.test.num_batches)
    for i in tqdm.tqdm(range(data.test.num_batches)):
        X, Y = data.test.next_batch()
        prediction = accuracy.eval(feed_dict={x: X, y: Y, keep_prob: 1.0, training: False})
        test_accuracy[i] = prediction
    mean_test_accuracy = np.mean(test_accuracy)
    print("test accuracy = %g" % mean_test_accuracy)
    data.test.restart()
    return mean_test_accuracy


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--model", type=str,
                        help="path to the partially trained model - when missing, the model will "
                             "be trained from scratch")
    parser.add_argument("--name", type=str, default="new_model",
                        help="name of new model - ignored when --model argument provided")
    parser.add_argument("--conv1_filters", default=32, type=int,
                        help="number of filters in first convolutional layer")
    parser.add_argument("--conv2_filters", default=64, type=int,
                        help="number of filters in second convolutional layer")
    parser.add_argument("--conv3_filters", default=128, type=int,
                        help="number of filters in third convolutional layer")
    parser.add_argument("--fc1_neurons", default=512, type=int,
                        help="number of neurons in first fully connected layer")
    parser.add_argument("--learning_rate", type=float, default=0.0001)
    parser.add_argument("--dropout", type=float, default=0.45)
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--image_size", type=int, default=100)
    parser.add_argument("--batches", type=int)
    parser.add_argument("--classes", type=int, default=4)
    parser.add_argument("--batch_norm", action="store_true")
    parser.add_argument("--batch_size", type=int, default=50)
    parser.add_argument("--early_stopping_epochs", type=int, default=10)
    parser.add_argument("--test", action="store_true", help="perform only testing on given model")
    parser.add_argument("dataset_path", type=str)
    parser.add_argument("--threads", type=int, default=0,
                        help="thread pool for tf session - default number of all logical CPU cores")
    parser.add_argument("--channels", type=int, default=3)
    ARGS = parser.parse_args()
    tf.app.run(main=main, argv=sys.argv)
