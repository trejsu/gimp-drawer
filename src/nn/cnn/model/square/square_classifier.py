import sys
import tqdm
import argparse
import os

import tensorflow as tf
import numpy as np

sys.path.insert(0, os.path.realpath('../../'))
from nn.dataset.square.square_dataset import SquareCenterDataset
from nn.model.model import Model


ARGS = None


class SquareClassifier(Model):

    CHANNELS = 1

    def __init__(self, args):
        super(SquareClassifier, self).__init__(args, SquareClassifier.CHANNELS, args.classes)

    def save_test_result_with_parameters(self, score):
        with open('results.txt', mode='a') as f:
            f.write('score = %s, python square_classifier.py --name %s --epochs %s --classes %s '
                    '--conv1_filters %s --conv2_filters %s --fc1_neurons %s --learning_rate %s '
                    '--dropout %s\n' % (score, self.name, self.epochs, self.outputs,
                                        self.conv1_filters, self.conv2_filters, self.fc1_neurons,
                                        self.learning_rate, self.dropout))


def main(_):
    x = tf.placeholder(tf.float32, [None, ARGS.image_size, ARGS.image_size], name="x")
    y = tf.placeholder(tf.int32, [None], name="y")
    y_one_hot = tf.one_hot(y, ARGS.classes)
    training = tf.placeholder(tf.bool, name="training")

    model = SquareClassifier(ARGS)

    y_conv, keep_prob = model.conv_net(x, training)

    with tf.name_scope('loss'):
        cross_entropy = tf.reduce_mean(
            tf.nn.softmax_cross_entropy_with_logits(labels=y_one_hot, logits=y_conv),
            name="cross_entropy")

    with tf.name_scope('optimizer'):
        optimizer = tf.train.AdamOptimizer(ARGS.learning_rate)

    update_ops = tf.get_collection(tf.GraphKeys.UPDATE_OPS)
    with tf.control_dependencies(update_ops):
        train_op = optimizer.minimize(cross_entropy)

    with tf.name_scope('prediction'):
        correct_prediction = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y_one_hot, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32), name="accuracy")

    with tf.Session() as sess:

        global_epoch, saver = model.restore_if_not_new(sess)

        data = SquareCenterDataset(ARGS.classes, ARGS.batch_size)

        if not ARGS.test:

            loss = []
            best_accuracy = 0
            epochs_not_improving = 0
            best_model_epoch = 0

            for epoch in tqdm.tqdm(range(global_epoch, ARGS.epochs)):

                num_batches = data.train.batch_n if ARGS.batches is None else ARGS.batches
                for step in tqdm.tqdm(range(num_batches)):
                    X, Y = data.train.next_batch()
                    _, cross_entropy_loss = sess.run([train_op, cross_entropy],
                                                     feed_dict={x: X, y: Y.reshape([-1]),
                                                                keep_prob: ARGS.dropout,
                                                                training: True})
                    loss.append(cross_entropy_loss)
                    if step == 0:
                        train_accuracy = accuracy.eval(
                            feed_dict={x: X, y: Y.reshape([-1]), keep_prob: 1.0, training: True})
                        tqdm.tqdm.write('train accuracy %g' % train_accuracy)

                test_accuracy = evaluate_test_accuracy(accuracy, data, keep_prob, training, x, y)
                tqdm.tqdm.write('test accuracy %g' % test_accuracy)

                if test_accuracy > best_accuracy:
                    current_epoch = epoch + 1
                    model.save(current_epoch, saver, sess)
                    best_accuracy = test_accuracy
                    epochs_not_improving = 0
                    best_model_epoch = current_epoch
                else:
                    epochs_not_improving += 1

                if epochs_not_improving >= ARGS.early_stopping_epochs:
                    break

                data.train.restart()

            model.save_learning_curve(loss, best_model_epoch)

        mean_test_accuracy = evaluate_test_accuracy(accuracy, data, keep_prob, training, x, y)
        model.save_test_result_with_parameters(mean_test_accuracy)


def evaluate_test_accuracy(accuracy, data, keep_prob, training, x, y):
    test_accuracy = np.zeros(100)
    data.test.next_batch()
    X, Y = data.test.X, data.test.Y
    for i in tqdm.tqdm(range(100)):
        prediction = accuracy.eval(
            feed_dict={x: np.expand_dims(X[i], 0), y: Y[i], keep_prob: 1.0, training: False})
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
    parser.add_argument("--conv2_filters", default=16, type=int,
                        help="number of filters in second convolutional layer")
    parser.add_argument("--fc1_neurons", default=256, type=int,
                        help="number of neurons in first fully connected layer")
    parser.add_argument("--learning_rate", type=float, default=0.01)
    parser.add_argument("--dropout", type=float, default=0.45)
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--image_size", type=int, default=100)
    parser.add_argument("--batches", type=int)
    parser.add_argument("--classes", type=int)
    parser.add_argument("--batch_norm", action="store_true")
    parser.add_argument("--batch_size", type=int, default=50)
    parser.add_argument("--early_stopping_epochs", type=int, default=10)
    parser.add_argument("--test", action="store_true", help="perform only testing on given model")
    ARGS = parser.parse_args()
    tf.app.run(main=main, argv=sys.argv)
