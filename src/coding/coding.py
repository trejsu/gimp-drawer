import numpy as np
import os
import time
import matplotlib.pylab as plt

from keras.models import load_model
from src.gimp.draw.draw_line import draw_line as _draw_line
from src.gimp.draw.draw_triangle import draw_triangle as _draw_triangle

ENCODED_PATH = '/tmp/encoded.npy'
DECODED_PATH = '/tmp/decoded.png'
ENCODED_BYTES = '/tmp/encoded_bytes'
ENCODED_AC = '/tmp/encoded_ac'
DECODED_BYTES = '/tmp/decoded_bytes'
IMAGES_PATH = '../data/image/scaled_images/'
ENCODED_TIME_CONSUMING_EXAMPLE = '../result/gimp_images/random/npy/encoded.npy'
AC_ENCODER = '/home/martyna/kod/python/Reference-arithmetic-coding/python/arithmetic-compress.py'
AC_DECODER = '/home/martyna/kod/python/Reference-arithmetic-coding/python/arithmetic-decompress.py'


class RandomEncoder(object):
    def __init__(self):
        pass

    def encode(self, img_path, actions, size, render, to_bytes):
        start = time.time()
        os.system(
            'python ../src/gimp/draw/generate_actions.py --output_path {} --image {} --actions {} {} --size {}'.format(
                ENCODED_PATH, os.path.join(IMAGES_PATH, img_path), actions + 1,
                '--render' if render else '', size))
        action_vectors = np.load(ENCODED_PATH)
        if to_bytes:
            encoded_bytes = action_vectors.astype(np.float32).tobytes()
            print('compressed to action vector of {} bytes'.format(len(encoded_bytes)))
            with open(ENCODED_BYTES, 'wb') as f:
                f.write(encoded_bytes)
            os.system('python {} {} {}'.format(AC_ENCODER, ENCODED_BYTES, ENCODED_AC))
            with open(ENCODED_AC, 'rb') as f:
                encoded_bytes_after_ac = f.read()
            print('compressed with AC to {} bytes'.format(len(encoded_bytes_after_ac)))
            action_vectors = encoded_bytes_after_ac
        end = time.time()
        compression_speed = end - start
        print('compressed in {} sec'.format(compression_speed))
        return action_vectors, compression_speed


class RandomDecoder(object):
    def __init__(self):
        pass

    def decode(self, action_args, size, from_bytes):
        start = time.time()
        if from_bytes:
            os.system('python {} {} {}'.format(AC_DECODER, ENCODED_AC, DECODED_BYTES))
            with open(DECODED_BYTES, 'rb') as f:
                decoded_bytes = f.read()
            print('decompressed from AC to {} bytes'.format(len(decoded_bytes)))
            decoded_action_args = np.frombuffer(decoded_bytes, dtype=np.float32).reshape([-1, 11])
            action_args = decoded_action_args
        np.save(ENCODED_PATH, action_args)
        os.system(
            'python ../src/gimp/draw/draw_from_actions.py --action_args {} --size {} --output_path {}'.format(
                ENCODED_PATH, size, DECODED_PATH))
        image_data = plt.imread(DECODED_PATH)[:, :, :3]
        plt.imshow(image_data)
        end = time.time()
        decompression_speed = end - start
        print('decompressed in {} sec'.format(decompression_speed))
        return decompression_speed


PREDICTOR = 'model.49-0.87'
RECTANGLE = 'model.11-0.02'
ELLIPSE = 'model.17-0.03'
LINE = 'model.08-0.03'
TRIANGLE = 'model.05-0.04'


class CnnEncoder(object):
    def __init__(self):
        self.shape_predictor = load_model('../result/model/shape_small/{}.hdf5'.format(PREDICTOR))
        self.representation_predictors = [
            load_model('../result/model/rectangle_small/{}.hdf5'.format(RECTANGLE)),
            load_model('../result/model/ellipse_small/{}.hdf5'.format(ELLIPSE)),
            load_model('../result/model/line_small/{}.hdf5'.format(LINE)),
            load_model('../result/model/triangle_small/{}.hdf5'.format(TRIANGLE))]

    def encode(self, img):
        start = time.time()
        action = np.argmax(self.shape_predictor.predict(img.reshape([1, 28, 28, 3]))[0])
        args = self.representation_predictors[action].predict(img.reshape([1, 28, 28, 3]))[0]
        end = time.time()
        print('compressed in {} sec'.format(end - start))
        return action, args


class CnnDecoder(object):
    def __init__(self):
        pass

    def decode(self, encoded, size=100):
        start = time.time()
        action, args = encoded
        if action == 0:
            self.draw_ellipse(args, size)
        elif action == 1:
            self.draw_rectangle(args, size)
        elif action == 2:
            self.draw_line(args, size)
        else:
            self.draw_triangle(args, size)
        end = time.time()
        print('decompressed in {} sec'.format(end - start))

    def draw(self, y_, shape, size):
        path_to_image_results = '../result/gimp_images/nn/shapes'
        name = 'jupyter_test.png'
        os.system(
            'python ../src/gimp/draw/draw_selection_shape.py --name {} --shape {} --size {} --r {} '
            '--g {} --b {} --a {} --x {} --y {} --w {} --h {} --rotation {}'.format(name, shape, size, y_[0], y_[1], y_[2], y_[3], y_[4], y_[5], y_[6], y_[7], y_[8]))
        image_data = plt.imread('%s/%s' % (path_to_image_results, name))[ :, :,:3]
        plt.imshow(image_data)

    def draw_rectangle(self, y, size):
        self.draw(y, 'rectangle', size)

    def draw_ellipse(self, y, size):
        self.draw(y, 'ellipse', size)

    def draw_triangle(self, y, size):
        path_to_image_results = '../result/gimp_images/nn/shapes'
        name = 'jupyter_test.png'
        _draw_triangle(name, size, y[0], y[1], y[2], y[3], y[4], y[5], y[6], y[7], y[8], y[9])
        image_data = plt.imread('%s/%s' % (path_to_image_results, name))[ :, :,:3]
        plt.imshow(image_data)

    def draw_line(self, y, size):
        path_to_image_results = '../result/gimp_images/nn/shapes'
        name = 'jupyter_test.png'
        _draw_line(name, size, y[0], y[1], y[2], y[3], y[4], y[5], y[6], y[7], y[8])
        image_data = plt.imread('%s/%s' % (path_to_image_results, name))[ :, :,:3]
        plt.imshow(image_data)