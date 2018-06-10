import sys
import argparse
import os

import numpy as np
import os.path as path
import tensorflow as tf

from keras.models import Sequential
from keras.layers import Conv2D, MaxPool2D, Flatten, Dense, BatchNormalization, Activation
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
    model.add(Conv2D(filters=64, kernel_size=(11, 11), padding='same'))
    model.add(BatchNormalization((64, 226, 226)))
    model.add(Activation('relu'))
    model.add(MaxPool2D(poolsize=(3, 3)))

    model.add(Conv2D(filters=128, kernel_size=(7, 7), padding='same'))
    model.add(BatchNormalization((128, 115, 115)))
    model.add(Activation('relu'))
    model.add(MaxPool2D(poolsize=(3, 3)))

    model.add(Conv2D(filters=192, kernel_size=(3, 3), padding='same'))
    model.add(BatchNormalization((128, 112, 112)))
    model.add(Activation('relu'))
    model.add(MaxPool2D(poolsize=(3, 3)))

    model.add(Conv2D(filters=256, kernel_size=(3, 3), padding='same'))
    model.add(BatchNormalization((128, 108, 108)))
    model.add(Activation('relu'))
    model.add(MaxPool2D(poolsize=(3, 3)))

    model.add(Flatten())
    model.add(Dense(12 * 12 * 256, 4096, init='normal'))
    model.add(BatchNormalization(4096))
    model.add(Activation('relu'))
    model.add(Dense(4096, 4096, init='normal'))
    model.add(BatchNormalization(4096))
    model.add(Activation('relu'))
    model.add(Dense(4096, ARGS.output_dim, init='normal'))
    model.add(BatchNormalization(ARGS.output_dim))
    model.add(Activation('sigmoid'))

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
    model_dir = create_model_dir()
    return path.join(model_dir, 'model.{epoch:02d}-{val_loss:.2f}.hdf5')


def create_model_dir():
    model_name = ARGS.name if ARGS.model is None else str(path.basename(ARGS.model))
    model_name = model_name.split('-')[0]
    model_dir = path.join(SAVE_PATH, model_name)
    if not os.path.exists(model_dir):
        os.mkdir(model_dir)
    return model_dir


def get_tensorboard_path():
    model_dir = create_model_dir()
    return path.join(model_dir, 'logs')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--model", type=str,
                        help="path to the partially trained model - when missing, the model will "
                             "be trained from scratch")
    parser.add_argument("--name", type=str, default="new_model",
                        help="name of new model - ignored when --model argument provided")
    parser.add_argument("--learning_rate", type=float, default=0.0001)
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--batches", type=int)
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

