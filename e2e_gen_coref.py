import os
import sys
import time
import json
import numpy as np

import cgi
import BaseHTTPServer
import ssl

import tensorflow as tf
import coref_model as cm
import util

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

def create_example(text):
    raw_sentences = sent_tokenize(text)
    sentences = [word_tokenize(s) for s in raw_sentences]
    speakers = [["" for _ in sentence] for sentence in sentences]
    return {
        "doc_key": "nw",
        "clusters": [],
        "sentences": sentences,
        "speakers": speakers,
      }

def print_predictions(example):
    words = util.flatten(example["sentences"])
    for cluster in example["predicted_clusters"]:
        print(u"Predicted cluster: {}".format([" ".join(words[m[0]:m[1]+1]) for m in cluster]))

def get_predictions(example):
    words = util.flatten(example["sentences"])
    clusters = []
    for cluster in example["predicted_clusters"]:
        clusters.append([" ".join(words[m[0]:m[1]+1]) for m in cluster])
    return clusters

def make_predictions(text, model):
    example = create_example(text)
    tensorized_example = model.tensorize_example(example, is_training=False)
    feed_dict = {i:t for i,t in zip(model.input_tensors, tensorized_example)}
    _, _, _, mention_starts, mention_ends, antecedents, antecedent_scores, head_scores = session.run(model.predictions + [model.head_scores], feed_dict=feed_dict)

    predicted_antecedents = model.get_predicted_antecedents(antecedents, antecedent_scores)

    example["predicted_clusters"], _ = model.get_predicted_clusters(mention_starts, mention_ends, predicted_antecedents)
    example["top_spans"] = zip((int(i) for i in mention_starts), (int(i) for i in mention_ends))
    example["head_scores"] = head_scores.tolist()
    return example


util.set_gpus()

name = "final" # final
port = None
keyfile = None
certfile = None

print "Running experiment: {}.".format(name)
config = util.get_config("experiments.conf")[name]
config["log_dir"] = util.mkdirs(os.path.join(config["log_root"], name))

util.print_config(config)
model = cm.CorefModel(config)

saver = tf.train.Saver()
log_dir = config["log_dir"]
pass

with tf.Session() as session:
    checkpoint_path = os.path.join(log_dir, "model.max.ckpt")
    saver.restore(session, checkpoint_path)

    text = "Although he didn't like it, Bob was chosen as the leader"
    print_predictions(make_predictions(text, model))
