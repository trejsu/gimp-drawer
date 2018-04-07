import os
from tqdm import tqdm
import random


def main():
    name_classes = [('2_parts', 2), ('4_parts', 4), ('9_parts', 9), ('25_parts', 25)]
    epochs = [1]
    conv1_filters = [32, 64, 128, 256, 512]
    conv2_filters = [16, 32, 64, 128, 256]
    fc1_neurons = [256, 512, 1024]
    learning_rate = [1.0, 0.1, 0.01, 0.001, 0.0001, 0.00001]
    dropout = [0.4, 0.45, 0.5]

    commands = ['python square_classifier.py --name %s --epochs %s --classes %s '
                '--conv1_filters %s --conv2_filters %s --fc1_neurons %s --learning_rate %s '
                '--dropout %s' % (name, e, classes, conv1, conv2, fc1, lr, d)
                for (name, classes) in name_classes for e in epochs for conv1 in conv1_filters
                for conv2 in conv2_filters for fc1 in fc1_neurons for lr in learning_rate
                for d in dropout]

    # commands = random.sample(commands, 100)
    for command in tqdm(commands):
        tqdm.write(command)
        os.system(command)


if __name__ == '__main__':
    main()
