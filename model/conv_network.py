import tensorflow as tf
import numpy as np


class ConvNetwork(object):
    def __init__(self, model_path):
        self.graph = tf.Graph()
        self.prev = None
        with self.graph.as_default():
            self.sess = tf.Session(graph=self.graph)
            saver = tf.train.import_meta_graph(model_path + ".meta")
            # saver = tf.train.Saver()
            saver.restore(self.sess, model_path)
        # self.sess.run(tf.global_variables_initializer())
        # print [n for n in self.graph.as_graph_def().node]

        # Placeholder - X
        # PLaceholder_1 - Y

        self.y = self.graph.get_tensor_by_name("fc2/add:0")
        self.x = self.graph.get_tensor_by_name("Placeholder:0")
        self.keep_prob = self.graph.get_tensor_by_name("dropout/Placeholder:0")

    def generate_args(self, diff):
        print np.array_equal(diff, self.prev)
        self.prev = diff
        return self.sess.run(self.y, feed_dict={self.x: np.expand_dims(diff, 0), self.keep_prob: 1.0})[0]



if __name__ == '__main__':
    c = ConvNetwork("../hopefully-improved-model-900")
    print c.generate_args(np.ones((100, 100, 3)))



