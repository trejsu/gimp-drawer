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
        conv1_filters = np.random.randint(23, 200)
        conv2_filters = np.random.randint(36, 200)
        conv3_filters = np.random.randint(36, 200)
        fc1_neurons = np.random.randint(49, 510)
        r = random.uniform(-4, -1)
        learning_rate = 10 ** r
        dropout = random.uniform(0.4, 0.49)
        sigmoid = random.choice(sigmoid_choices)
        batch_size = np.random.randint(29, 100)
        commands.append('python shape_representation.py --dataset random_rectangle '
                        '--output_dim 9 --name test --epochs {} --conv1_filters {} '
                        '--conv2_filters {} --conv3_filters {} --fc1_neurons {} --learning_rate {} '
                        '--dropout {} {} {} --batch_size {} --threads {}'
                        .format(epochs, conv1_filters, conv2_filters, conv3_filters, fc1_neurons,
                                learning_rate, dropout, '--fc2_sigmoid' if sigmoid[0] else '',
                                '--loss_sigmoid' if sigmoid[1] else '', batch_size, ARGS.threads))

    for command in tqdm(commands):
        # tqdm.write(command)
        os.system(command)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--n", type=int, default=100, help="Number of samples")
    parser.add_argument("--threads", type=int, default=15)
    ARGS = parser.parse_args()
    main()