import sys
import argparse
import os

import numpy as np
import os.path as path
import tensorflow as tf

from keras.models import Sequential
from keras.layers import Conv2D, MaxPool2D, Flatten, Dense, Dropout, BatchNormalization, Activation
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.optimizers import Adam
from keras import backend as K


ARGS = None
SAVE_PATH = path.join(os.path.expandvars("$GIMP_PROJECT"), 'result/model')


def main(_):
    X_train = np.load(path.join(ARGS.dataset_path, "train_X.npy"), mmap_mode="r")
    Y_train = np.load(path.join(ARGS.dataset_path, "train_Y.npy"), mmap_mode="r")
    X_test = np.load(path.join(ARGS.dataset_path, "test_X.npy"), mmap_mode="r")
    Y_test = np.load(path.join(ARGS.dataset_path, "test_Y.npy"), mmap_mode="r")

    model = Sequential()
    model.add(Conv2D(ARGS.conv1_filters, ARGS.conv1_kernel_size, strides=(1, 1),
                     padding='same', activation='relu',
                     input_shape=(ARGS.image_size, ARGS.image_size, ARGS.channels)))
    model.add(MaxPool2D(pool_size=(2, 2), strides=(2, 2), padding='same'))
    model.add(Conv2D(ARGS.conv2_filters, ARGS.conv2_kernel_size, strides=(1, 1),
                     padding='same', activation='relu'))
    model.add(MaxPool2D(pool_size=(2, 2), strides=(2, 2), padding='same'))
    model.add(Flatten())
    model.add(Dense(ARGS.fc1_neurons))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(Dropout(ARGS.dropout))
    model.add(Dense(ARGS.output_dim, activation='sigmoid'))

    callbacks = [EarlyStopping(monitor='val_loss', patience=ARGS.early_stopping_epochs, mode='min'),
                 ModelCheckpoint(get_saving_path(), monitor='val_loss', save_best_only=True,
                                 save_weights_only=False, mode='min', period=1)]

    optimizer = Adam(lr=ARGS.learning_rate)
    model.compile(optimizer=optimizer, loss='mse')

    K.set_session(K.tf.Session(config=tf.ConfigProto(inter_op_parallelism_threads=ARGS.threads,
                                                     intra_op_parallelism_threads=ARGS.threads)))

    model.fit(x=X_train, y=Y_train, batch_size=ARGS.batch_size, epochs=ARGS.epochs,
              callbacks=callbacks, validation_data=(X_test, Y_test), shuffle=True)


def get_saving_path():
    model_name = ARGS.name if ARGS.model is None else str(path.basename(ARGS.model))
    model_name = model_name.split('-')[0]
    model_dir = "%s/%s" % (SAVE_PATH, model_name)
    print(model_dir)
    if not os.path.exists(model_dir):
        os.mkdir(model_dir)
    model_path = "%s/%s" % (model_dir, model_name)
    return model_path


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
    parser.add_argument("--conv1_kernel_size", default=10, type=int,
                        help="size of kernels in first convolutional layer")
    parser.add_argument("--conv2_kernel_size", default=5, type=int,
                        help="size of kernels in second convolutional layer")
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

