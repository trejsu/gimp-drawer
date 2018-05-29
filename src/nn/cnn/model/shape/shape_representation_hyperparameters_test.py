import os
from tqdm import tqdm
import numpy as np
import argparse
import random


ARGS = None


def main():
    epochs = 1
    sigmoid_choices = [(False, False), (True, False), (False, True)]

    commands = []

    for _ in range(ARGS.n):
        conv1_filters = np.random.randint(23, 266)
        conv2_filters = np.random.randint(36, 480)
        fc1_neurons = np.random.randint(49, 510)
        r = random.uniform(-4, -1)
        learning_rate = 10 ** r
        dropout = random.uniform(0.4, 0.49)
        sigmoid = random.choice(sigmoid_choices)
        batch_size = np.random.randint(29, 180)
        commands.append('python square_regression.py --dataset diff_random_parameters '
                        '--output_dim 9 --name regression_test --epochs {} --conv1_filters {} '
                        '--conv2_filters {} --fc1_neurons {} --learning_rate {} --dropout {} {} {} '
                        '--batch_size {}'.format(epochs, conv1_filters, conv2_filters, fc1_neurons,
                                                 learning_rate, dropout, '--fc2_sigmoid' if sigmoid[0] else '',
                                                 '--loss_sigmoid' if sigmoid[1] else '', batch_size))

    for command in tqdm(commands):
        tqdm.write(command)
        # os.system(command)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--n", type=int, default=100, help="Number of samples")
    ARGS = parser.parse_args()
    main()