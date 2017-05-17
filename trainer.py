from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import sys

from tensorflow.examples.tutorials.mnist import input_data
from tensorflow.python.saved_model import builder as saved_model_builder
from tensorflow.python.saved_model import tag_constants

from models.simple_mlp import simple_fn
from models.simple_autoencoder import autoencoder_fn
from data.fn import input_fn

import tensorflow as tf

MODEL_DIR = "tmp/training"
FLAGS = tf.app.flags.FLAGS
tf.app.flags.DEFINE_string('mode', 'simple', 'simple or autoencoder.')


def euclidean_distance_metric_fn(predictions, labels):

  return


def main(_):

  print("running in mode: ", FLAGS.mode)

  model_fn = simple_fn
  if FLAGS.mode == "autoencoder":
    model_fn = autoencoder_fn

  mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

  est = tf.contrib.learn.Estimator(
      model_fn=model_fn,
      model_dir=MODEL_DIR,
      config=tf.contrib.learn.RunConfig(save_checkpoints_secs=30))
  exp = tf.contrib.learn.Experiment(
      estimator=est,
      eval_steps=1,
      min_eval_frequency=1,
      train_input_fn=lambda: input_fn(mnist.train, 100),
      eval_input_fn=lambda: input_fn(mnist.test, 100),
      eval_metrics={
          "accuracy": tf.metrics.accuracy,
      })
  exp.train_and_evaluate()


if __name__ == '__main__':
  tf.logging.set_verbosity(tf.logging.INFO)
  tf.app.run()