import tensorflow as tf
import numpy as np

from tensorflow.python.tools import inspect_checkpoint as chkp


class ConvNetwork(object):
    def __init__(self, model_path):
        self.model_path = model_path
        self.graph = tf.Graph()
        with self.graph.as_default():
            self.sess = tf.Session(graph=self.graph)
            saver = tf.train.import_meta_graph(model_path + ".meta")
            saver.restore(self.sess, model_path)

        self.y_conv = self.graph.get_tensor_by_name("fc2/y_conv:0")
        self.y = self.graph.get_tensor_by_name("y:0")
        self.x = self.graph.get_tensor_by_name("x:0")
        self.keep_prob = self.graph.get_tensor_by_name("dropout/keep_prob:0")
        self.loss = self.graph.get_tensor_by_name("loss/loss:0")

    def generate_args(self, x):
        return self.sess.run(self.y_conv, feed_dict={self.x: np.expand_dims(x, 0), self.keep_prob: 1.0})[0]

    def eval_error(self, X, Y):
        return self.loss.eval(session=self.sess, feed_dict={self.x: X, self.y: Y, self.keep_prob: 1.0})

    def print_tensors(self):
        chkp.print_tensors_in_checkpoint_file(self.model_path, tensor_name='', all_tensors=True)


