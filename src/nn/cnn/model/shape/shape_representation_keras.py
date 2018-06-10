import sys
import argparse
import os

import numpy as np
import os.path as path
import tensorflow as tf

from keras.models import Sequential
from keras.layers import Conv2D, MaxPool2D, Flatten, Dense, Dropout, BatchNormalization, Activation, \
    LeakyReLU
from keras.callbacks import EarlyStopping, ModelCheckpoint, TensorBoard
from keras.optimizers import Adam
from keras import backend as K
from keras.regularizers import l2


ARGS = None
SAVE_PATH = path.join(os.path.expandvars("$GIMP_PROJECT"), 'result/model')


def main(_):
    X_train = np.load(path.join(ARGS.dataset_path, "train_X.npy"), mmap_mode="r")
    Y_train = np.load(path.join(ARGS.dataset_path, "train_Y.npy"), mmap_mode="r")
    X_test = np.load(path.join(ARGS.dataset_path, "test_X.npy"), mmap_mode="r")
    Y_test = np.load(path.join(ARGS.dataset_path, "test_Y.npy"), mmap_mode="r")

    activation = 'relu'
    kernel_regularizer = l2(0.01) if ARGS.l2 else None

    model = Sequential()
    model.add(Conv2D(ARGS.conv1_filters, ARGS.conv1_kernel_size, strides=(1, 1),
                     padding='same', kernel_regularizer=kernel_regularizer,
                     input_shape=(ARGS.image_size, ARGS.image_size, ARGS.channels)))
    model.add(BatchNormalization())
    model.add(Activation(activation))
    model.add(MaxPool2D(pool_size=(2, 2), strides=(2, 2), padding='same'))
    model.add(Conv2D(ARGS.conv2_filters, ARGS.conv2_kernel_size, strides=(1, 1),
                     padding='same', kernel_regularizer=kernel_regularizer))
    model.add(BatchNormalization())
    model.add(Activation(activation))
    model.add(MaxPool2D(pool_size=(2, 2), strides=(2, 2), padding='same'))
    model.add(Flatten())
    model.add(Dense(ARGS.fc1_neurons))
    model.add(BatchNormalization())
    model.add(Activation(activation))
    model.add(Dropout(ARGS.dropout))
    model.add(Dense(ARGS.output_dim, activation='sigmoid'))

    callbacks = [EarlyStopping(monitor='val_loss', patience=ARGS.early_stopping_epochs, mode='min'),
                 ModelCheckpoint(get_saving_path(), monitor='val_loss', save_best_only=True,
                                 save_weights_only=False, mode='min', period=1),
                 TensorBoard(log_dir=get_tensorboard_path(), write_images=True)]

    optimizer = Adam(lr=ARGS.learning_rate)
    model.compile(optimizer=optimizer, loss='mse')

    K.set_session(K.tf.Session(config=tf.ConfigProto(inter_op_parallelism_threads=ARGS.threads,
                                                     intra_op_parallelism_threads=ARGS.threads)))
    K.get_session().run(tf.initialize_all_variables())

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
    parser.add_argument("--conv1_filters", default=32, type=int,
                        help="number of filters in first convolutional layer")
    parser.add_argument("--conv2_filters", default=64, type=int,
                        help="number of filters in second convolutional layer")
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
    parser.add_argument("--batch_size", type=int, default=25)
    parser.add_argument("--early_stopping_epochs", type=int, default=10)
    parser.add_argument("--test", action="store_true", help="perform only testing on given model")
    parser.add_argument("--output_dim", type=int, help="number of output values")
    parser.add_argument("dataset_path", type=str)
    parser.add_argument("--channels", type=int, default=3)
    parser.add_argument("--threads", type=int, default=0,
                        help="thread pool for tf session - default number of all logical CPU cores")
    parser.add_argument("--l2", action="store_true")
    ARGS = parser.parse_args()
    tf.app.run(main=main, argv=sys.argv)

