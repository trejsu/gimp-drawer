import os
from tqdm import tqdm
import random


def main():
    epochs = [1]
    conv1_filters = [16, 32, 64, 128, 256, 512]
    conv2_filters = [16, 32, 64, 128, 256, 512]
    fc1_neurons = [16, 32, 64, 128, 256, 512]
    learning_rate = [0.1, 0.01, 0.001, 0.0001, 0.00001]
    dropout = [0.4, 0.45, 0.5]
    sigmoid = [(False, False), (True, False), (False, True)]
    batch_size = [25, 50, 100, 150, 200]

    commands = ['python square_regression.py --dataset diff_parameters --output_dim 9 '
                '--name regression_test --epochs %s --conv1_filters %s --conv2_filters %s '
                '--fc1_neurons %s --learning_rate %s --dropout %s %s %s --batch_size %s'
                % (e, conv1, conv2, fc1, lr, d, '--fc2_sigmoid' if s[0] else '',
                   '--loss_sigmoid' if s[1] else '', bs)
                for e in epochs for conv1 in conv1_filters for conv2 in conv2_filters for fc1 in
                fc1_neurons for lr in learning_rate for d in dropout for s in sigmoid
                for bs in batch_size]

    commands = random.sample(commands, 100)
    for command in tqdm(commands):
        tqdm.write(command)
        # os.system(command)


if __name__ == '__main__':
    main()
