import os
import time
from datetime import datetime

import tensorflow as tf

from src.common.plugin import Plugin

CLUSTER = tf.train.ClusterSpec({'local': ['localhost:2222', 'localhost:2223', 'localhost:2224',
                                          'localhost:2225']})
WORKER_PATH = 'src/nn/reinforcement/distributed/worker.py'
WORKER_PLUGIN_NAME = 'worker'


def main():
    workers = run_workers()

    server = tf.train.Server(CLUSTER, job_name='local', task_index=0)
    tf.reset_default_graph()
    main_var = tf.Variable(initial_value=0.0, name='main')
    worker_var = tf.Variable(initial_value=0.0, name='worker')
    with tf.Session(server.target) as sess:
        sess.run(tf.global_variables_initializer())

        for _ in range(10):
            timestamp_print('Incrementing main var...')
            sess.run(main_var.assign_add(1.0))
            timestamp_print('Checking worker var: {}'.format(sess.run(worker_var)))
            timestamp_print('Sleeping...')
            time.sleep(10)

    for worker in workers:
        worker.terminate()


def run_workers():
    num_workers = 3
    worker_path = os.path.join(os.path.expandvars('$GIMP_PROJECT'), WORKER_PATH)
    workers = [Plugin(worker_path, WORKER_PLUGIN_NAME,
                      [("number", i + 1), ("interval", (i + 1) * 3)], list_args=True)
               for i in range(num_workers)]

    plugins = []
    for worker in workers:
        timestamp_print('Running worker...')
        plugin = worker.run_as_subprocess()
        plugins.append(plugin)
        time.sleep(0.5)

    return plugins


def timestamp_print(message):
    print('{}: {} - {}'.format(datetime.now(), 'main', message))


if __name__ == '__main__':
    main()
