import time
from datetime import datetime

import tensorflow as tf
from gimpfu import *

from src.nn.reinforcement.distributed.demo import CLUSTER


def plugin_main(number, interval):
    server = tf.train.Server(CLUSTER, job_name='local', task_index=number)
    tf.reset_default_graph()
    main_var = tf.Variable(initial_value=0.0, name='main')
    worker_var = tf.Variable(initial_value=0.0, name='worker')
    with tf.Session(server.target) as sess:

        timestamp_print('Waiting for connection...', number)
        sess.run(tf.report_uninitialized_variables())
        while len(sess.run(tf.report_uninitialized_variables())) > 0:
            timestamp_print('Waiting for initialization...', number)
            time.sleep(interval)
        timestamp_print('Variables initialized!', number)

        while True:
            timestamp_print('Checking main var: {}'.format(sess.run(main_var)), number)
            timestamp_print('Incrementing worker var...', number)
            sess.run(worker_var.assign_add(1.0))
            timestamp_print('Sleeping...', number)
            time.sleep(interval)


def timestamp_print(message, number):
    print('{}: {}{} - {}'.format(datetime.now(), 'worker-', number, message))
