import tensorflow as tf
import numpy as np


class ConvNetwork(object):
    def __init__(self, model_path):
        self.graph = tf.Graph()
        with self.graph.as_default():
            self.sess = tf.Session(graph=self.graph)
            saver = tf.train.import_meta_graph(model_path + ".meta")
            saver.restore(self.sess, model_path)

        self.y_conv = self.graph.get_tensor_by_name("fully_connected2/add:0")
        self.y_ = self.graph.get_tensor_by_name("Placeholder_1:0")
        self.x = self.graph.get_tensor_by_name("Placeholder:0")
        self.keep_prob = self.graph.get_tensor_by_name("dropout/Placeholder:0")
        self.error = self.graph.get_tensor_by_name("Mean:0")

    def generate_args(self, x):
        return self.sess.run(self.y_conv, feed_dict={self.x: np.expand_dims(x, 0), self.keep_prob: 1.0})[0]

    def eval_error(self, X, Y):
        return self.error.eval(session=self.sess, feed_dict={self.x: np.expand_dims(X, 0), self.y_: np.expand_dims(Y, 0), self.keep_prob: 1.0})



