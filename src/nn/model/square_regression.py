import sys
import tqdm
import argparse
import os
import random

import numpy as np

sys.path.insert(0, os.path.realpath('../../'))
from nn.dataset.square.square_dataset import SquareDataset
from nn.model.model import *


ARGS = None
MODEL_DIR = os.path.expandvars("$GIMP_PROJECT/out/model/square/")


class SquareRegression(Model):

    CHANNELS = 1
    OUTPUTS = 2

    def __init__(self, args):
        super().__init__(args, SquareRegression.CHANNELS, SquareRegression.OUTPUTS)
        self.fc2_sigmoid = args.fc2_sigmoid

    def save_test_result_with_parameters(self, score):
        with open('results.txt', mode='a') as f:
            f.write('score = %s, python square_regression.py --name %s --epochs %s '
                    '--conv1_filters %s --conv2_filters %s --fc1_neurons %s --learning_rate %s '
                    '--dropout %s\n' % (score, self.name, self.epochs, self.conv1_filters,
                                        self.conv2_filters, self.fc1_neurons, self.learning_rate,
                                        self.dropout))

    def fc2_layer(self, h_fc1_dropout):
        W_fc2 = weight_variable([self.fc1_neurons, self.outputs])
        b_fc2 = bias_variable([self.outputs])
        y_conv = tf.add(tf.matmul(h_fc1_dropout, W_fc2), b_fc2, name="y_conv")
        if self.fc2_sigmoid:
            y_conv = tf.nn.sigmoid(y_conv)
        return y_conv


def main(_):
    x = tf.placeholder(tf.float32, [None, ARGS.image_size, ARGS.image_size], name="x")
    y = tf.placeholder(tf.float32, [None, 2], name="y")
    training = tf.placeholder(tf.bool, name="training")

    model = SquareRegression(ARGS)
    y_conv, keep_prob = model.conv_net(x, training)

    with tf.name_scope('loss'):
        if ARGS.loss_sigmoid:
            loss = tf.reduce_mean(tf.square(tf.nn.sigmoid(y_conv) - y), name="loss")
        else:
            loss = tf.reduce_mean(tf.losses.mean_squared_error(labels=y, predictions=y_conv),
                                  name="loss")

    with tf.name_scope('optimizer'):
        train_step = tf.train.AdamOptimizer(ARGS.learning_rate).minimize(loss)

    with tf.Session() as sess:

        global_epoch, saver = model.restore_if_not_new(sess)
        data = SquareDataset(1)
        train_mse = []

        for epoch in tqdm.tqdm(range(global_epoch, ARGS.epochs)):

            num_batches = data.train.batch_n if ARGS.batches is None else ARGS.batches

            for step in tqdm.tqdm(range(num_batches)):
                X, Y = data.train.next_batch()
                train_step.run(feed_dict={x: X, y: Y, keep_prob: ARGS.dropout, training: True})
                loss_eval = loss.eval(feed_dict={x: X, y: Y, keep_prob: 1.0, training: True})
                train_mse.append(loss_eval)
                if step == 0:
                    tqdm.tqdm.write('train mse %g' % loss_eval)

            model.save(epoch + 1, saver, sess)
            model.save_learning_curve(train_mse)

        test_mse = np.zeros(data.test.batch_n)
        for i in tqdm.tqdm(range(data.test.batch_n)):
            X, Y = data.test.next_batch()
            mse = loss.eval(feed_dict={x: X, y: Y, keep_prob: 1.0, training: False})
            test_mse[i] = mse
        mean_test_mse = np.mean(test_mse)
        print("average test mse = %g" % mean_test_mse)

        model.save_test_result_with_parameters(mean_test_mse)

        examples = data.test.random_X(ARGS.visual_test_examples)
        predictions = y_conv.eval(feed_dict={x: examples, keep_prob: 1.0, training: False})
        visualize_predictions(examples, predictions, model)


def visualize_predictions(examples, predictions, model):
    size = ARGS.image_size

    for index, (example, prediction) in enumerate(zip(examples, predictions)):
        rgb_example = gray_to_rgb(example, size)
        x_prediction = int(prediction[0] * size)
        y_prediction = int(prediction[1] * size)
        if 0 <= x_prediction <= size and 0 <= y_prediction <= size:
            rgb_example[x_prediction][y_prediction][0] = 1
            rgb_example[x_prediction][y_prediction][1] = 0
            rgb_example[x_prediction][y_prediction][2] = 0
        plt.imshow(rgb_example)
        plt.suptitle('prediction = (%d, %d)' % (x_prediction, y_prediction))
        plt.savefig('%s/%s/visualized_prediction_%d.png' % (Model.MODEL_DIR, model.get_model_name(),
                                                            index))


def gray_to_rgb(example, size):
    rgb_example = np.zeros([size, size, 3])
    rgb_example[:, :, 0] = example
    rgb_example[:, :, 1] = example
    rgb_example[:, :, 2] = example
    return rgb_example


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
    parser.add_argument("--fc1_neurons", default=512, type=int,
                        help="number of neurons in first fully connected layer")
    parser.add_argument("--learning_rate", type=float, default=0.0001)
    parser.add_argument("--dropout", type=float, default=0.5)
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--image_size", type=int, default=100)
    parser.add_argument("--batches", type=int)
    parser.add_argument("--batch_norm", action="store_true")
    parser.add_argument("--fc2_sigmoid", action="store_true")
    parser.add_argument("--loss_sigmoid", action="store_true")
    parser.add_argument("--visual_test_examples", type=int, default=3)
    ARGS = parser.parse_args()
    tf.app.run(main=main, argv=sys.argv)
