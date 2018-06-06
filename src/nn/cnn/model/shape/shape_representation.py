import sys
import tqdm
import argparse

import numpy as np

from src.nn.cnn.dataset.dataset import OnePartDataset
from src.nn.cnn.model.model import *


ARGS = None


class ShapeRepresentation(Model):

    def __init__(self, args):
        super(ShapeRepresentation, self).__init__(args, ARGS.channels, ARGS.output_dim)
        self.fc2_sigmoid = args.fc2_sigmoid
        self.loss_sigmoid = args.loss_sigmoid

    def save_test_result_with_parameters(self, score):
        with open('shape_representation_results.txt', mode='a') as f:
            f.write('score = %s, python square_regression.py --name %s --epochs %s '
                    '--conv1_filters %s --conv2_filters %s --conv3_filters %s --fc1_neurons %s '
                    '--learning_rate %s --dropout %s --batch_size %s %s %s\n'
                    % (score, self.name, self.epochs, self.conv1_filters, self.conv2_filters,
                       self.conv3_filters, self.fc1_neurons, self.learning_rate, self.dropout,
                       ARGS.batch_size, '--fc2_sigmoid' if self.fc2_sigmoid else '',
                       '--loss_sigmoid' if self.loss_sigmoid else ''))

    def fc2_layer(self, h_fc1_dropout):
        W_fc2 = weight_variable([self.fc1_neurons, self.outputs])
        b_fc2 = bias_variable([self.outputs])
        if self.fc2_sigmoid:
            y_conv = tf.nn.sigmoid(tf.add(tf.matmul(h_fc1_dropout, W_fc2), b_fc2), name="y_conv")
        else:
            y_conv = tf.add(tf.matmul(h_fc1_dropout, W_fc2), b_fc2, name="y_conv")
        return y_conv


def main(_):
    x = tf.placeholder(tf.float32, [None, ARGS.image_size, ARGS.image_size, ARGS.channels], name="x")
    y = tf.placeholder(tf.float32, [None, ARGS.output_dim], name="y")
    training = tf.placeholder(tf.bool, name="training")

    model = ShapeRepresentation(ARGS)
    y_conv, keep_prob = model.conv_net(x, training)

    with tf.name_scope('loss'):
        if ARGS.loss_sigmoid:
            loss = tf.reduce_mean(tf.square(tf.nn.sigmoid(y_conv) - y), name="loss")
        else:
            loss = tf.reduce_mean(tf.losses.mean_squared_error(labels=y, predictions=y_conv),
                                  name="loss")

    with tf.name_scope('optimizer'):
        train_step = tf.train.AdamOptimizer(learning_rate=ARGS.learning_rate).minimize(loss)

    with tf.Session(config=tf.ConfigProto(inter_op_parallelism_threads=ARGS.threads,
                                          intra_op_parallelism_threads=ARGS.threads)) as sess:

        global_epoch, saver = model.restore_if_not_new(sess)
        data = OnePartDataset(ARGS.dataset_path, ARGS.batch_size)

        if not ARGS.test:

            train_mse = []
            lowest_mse = 100
            epochs_not_improving = 0
            best_model_epoch = 0

            for epoch in tqdm.tqdm(range(global_epoch, ARGS.epochs)):

                num_batches = data.train.num_batches if ARGS.batches is None else ARGS.batches

                for step in tqdm.tqdm(range(num_batches)):
                    X, Y = data.train.next_batch()
                    train_step.run(feed_dict={x: X, y: Y, keep_prob: ARGS.dropout, training: True})
                    train_loss = loss.eval(feed_dict={x: X, y: Y, keep_prob: 1.0, training: True})
                    train_mse.append(train_loss)
                    if step == 0:
                        tqdm.tqdm.write('train mse %g' % train_loss)

                test_loss = evaluate_test_mse(data, keep_prob, loss, training, x, y)
                tqdm.tqdm.write('test mse %g' % test_loss)
                if test_loss < lowest_mse:
                    current_epoch = epoch + 1
                    model.save(current_epoch, saver, sess)
                    best_model_epoch = current_epoch
                    lowest_mse = test_loss
                    epochs_not_improving = 0
                else:
                    epochs_not_improving += 1

                if epochs_not_improving >= ARGS.early_stopping_epochs:
                    break

                data.train.restart()

            model.save_learning_curve(train_mse, best_model_epoch)

        mean_test_mse = evaluate_test_mse(data, keep_prob, loss, training, x, y)
        model.save_test_result_with_parameters(mean_test_mse)


def evaluate_test_mse(data, keep_prob, loss, training, x, y):
    test_mse = np.zeros(data.test.batch_n)
    for i in tqdm.tqdm(range(data.test.batch_n)):
        X, Y = data.test.next_batch()
        mse = loss.eval(feed_dict={x: X, y: Y, keep_prob: 1.0, training: False})
        test_mse[i] = mse
    mean_test_mse = np.mean(test_mse)
    print("average test mse = %g" % mean_test_mse)
    data.test.restart()
    return mean_test_mse


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
    parser.add_argument("--learning_rate", type=float, default=0.01)
    parser.add_argument("--dropout", type=float, default=0.5)
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--image_size", type=int, default=100)
    parser.add_argument("--batches", type=int)
    parser.add_argument("--batch_norm", action="store_true")
    parser.add_argument("--fc2_sigmoid", action="store_true")
    parser.add_argument("--loss_sigmoid", action="store_true")
    parser.add_argument("--batch_size", type=int, default=25)
    parser.add_argument("--early_stopping_epochs", type=int, default=10)
    parser.add_argument("--test", action="store_true", help="perform only testing on given model")
    parser.add_argument("--output_dim", type=int, help="number of output values")
    parser.add_argument("dataset_path", type=str)
    parser.add_argument("--channels", type=int, default=3)
    parser.add_argument("--threads", type=int, default=0,
                        help="thread pool for tf session - default number of all logical CPU cores")
    ARGS = parser.parse_args()
    tf.app.run(main=main, argv=sys.argv)

