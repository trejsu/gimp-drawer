import os
import threading
import logging as log

import tensorflow as tf
from time import sleep

from src.nn.reinforcement.actor_critic import ActorCriticNet
from src.nn.reinforcement.worker import Worker
from src.nn.reinforcement.gimp import Gimp


def plugin_main():
    num_actions = 50
    gamma = .99  # discount rate for advantage estimation and reward discounting
    state_size = 30000  # Observations are images of 100 * 100 * 3
    action_size = 9  # Agent chooses 9 parameters describing ellipse to draw
    load_model = False
    model_path = os.path.expandvars("$GIMP_PROJECT/result/model/reinforcement")
    renders_path = os.path.expandvars("GIMP_PROJECT/result/renders/reinforcement")

    if not os.path.exists(model_path):
        os.makedirs(model_path)

    if not os.path.exists(renders_path):
        os.makedirs(renders_path)

    tf.reset_default_graph()

    with tf.device("/cpu:0"):
        global_episodes = tf.Variable(0, dtype=tf.int32, name='global_episodes', trainable=False)
        optimizer = tf.train.AdamOptimizer(learning_rate=1e-4)
        global_network = ActorCriticNet(state_size, action_size, scope='global', optimizer=None)
        # num_workers = multiprocessing.cpu_count()
        # temporary solution before figuring out how to handle multiple concurrent gimp environments
        num_workers = 1
        workers = [Worker(Gimp(), i, state_size, action_size, optimizer, model_path,
                          global_episodes) for i in range(num_workers)]
        saver = tf.train.Saver(max_to_keep=5)

    with tf.Session() as sess:
        coordinator = tf.train.Coordinator()
        if load_model:
            log.info('loading model from %s...', model_path)
            ckpt = tf.train.get_checkpoint_state(model_path)
            saver.restore(sess, ckpt.model_checkpoint_path)
            log.info('model loaded successfully')
        else:
            sess.run(tf.global_variables_initializer())

        worker_threads = []
        for worker in workers:
            t = threading.Thread(target=worker.work(num_actions, gamma, sess, coordinator, saver))
            t.start()
            sleep(0.5)
            worker_threads.append(t)
        coordinator.join(worker_threads)
