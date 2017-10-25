import argparse
from copy import deepcopy
import json
from math import floor
import os
from random import shuffle
import re

from doc_data import DocData
from errors import Asg3Error
from model import NBClassifier


def _load_data(fp):
  """ Read all .txt files within directory (and all subdirectories) """
  docs = []
  for root, dirs, files in os.walk(fp):
    for fn in files:
      if '.txt' not in fn:
        # docs are ensured to be .txt files
        continue
      # get full filepath of doc
      filename = os.path.join(root, fn)
      with open(filename, 'rU') as reader:
        lines = []
        for line in reader:
          if line:
            lines.append(line)
        docs.append('\n'.join(lines))
  return docs


def load_data_sets(pos_dir, neg_dir, prop_training=0.7, randomize=True):
  """ Get a sample data set of size N of either training or testing data """
  positives = _load_data(pos_dir)
  negatives = _load_data(neg_dir)

  print '# negatives: {}'.format(len(negatives))
  print '# positives: {}'.format(len(positives))

  tot = len(positives) + len(negatives)
  priors = {
    '0': float(float(len(negatives)) / float(tot)),
    '1': float(float(len(positives)) / float(tot))
  }

  # combine all docs so that we can shuffle
  all_docs = []
  for doc in negatives:
    all_docs.append((doc.lower(), 0))
  for doc in positives:
    all_docs.append((doc.lower(), 1))

  # split the data into training/testing
  if randomize:
    shuffle(all_docs)
  else:
    # control the randomization
    seed = 0.246374575648
    shuffle(all_docs, lambda: seed)

  cutoff = int(len(all_docs) * prop_training)
  training = all_docs[:cutoff]
  testing = all_docs[cutoff:]

  # training data object
  training_data = DocData('training', priors)
  for doc in training:
    training_data.add_doc(doc[0], doc[1])

  # test data object
  test_data = DocData('test', priors)
  for doc in testing:
    test_data.add_doc(doc[0], doc[1])

  return training_data, test_data


def _print_data_info(data):
  """ Helper that prints an DocData's info """

  print '    -------------------------------'
  fmt = '{:<25} {:<6}'
  print fmt.format('    # positives docs', data.num_positive_docs())
  print fmt.format('    # non-positives docs', data.num_negative_docs())
  print fmt.format('    # total docs', len(data.docs))
  print fmt.format('    # total words', len(data.words))
  print '    -------------------------------'


def print_results(training_data, test_data, accuracy, 
                  f1, precision, recall):
  """ Helper that prints results from a model run """
  
  # print model info
  print '\n> Finished running model.'
  print '\n> Parameters:'
  print '\n  > Training data: '
  _print_data_info(training_data)
  print '\n  > Test data: '
  _print_data_info(test_data)

  # print formatted evaluations
  print '\n> Evaluations:\n'
  fmt = '{:<19} {:<6}'
  print '    -------------------------------'
  print fmt.format('    Accuracy:', accuracy)
  print fmt.format('    F1:', f1)
  print fmt.format('    Precision:', precision)
  print fmt.format('    Recall:', recall)
  print '    -------------------------------'


def view_word_correlations(training_data, prop_words=0.25, n=200):
  """
    View the most commonly co-occurring words
  """

  import pandas as pd

  from helpers import tokenize

  # get the most commonly occurring prop_words % of words
  word_counts = {}
  for word in training_data.words:
    word_counts[word] = len(training_data.words[word])
  swc = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
  most_common_words = set()
  for i in range(len(swc)):
    if i >= (len(training_data.words) * prop_words):
      break
    most_common_words.add(swc[i][0])

  # map words to lists of word counts
  d = {}
  for word in most_common_words:
    d[word] = []
    for doc in training_data.docs:
      tokens = tokenize(doc[0])
      d[word].append(len([t for t in tokens if t == word]))

  df = pd.DataFrame(data = d)

  def get_redundant_pairs(df):
    '''Get diagonal and lower triangular pairs of correlation matrix'''
    pairs_to_drop = set()
    cols = df.columns
    for i in range(0, df.shape[1]):
      for j in range(0, i+1):
        pairs_to_drop.add((cols[i], cols[j]))
    return pairs_to_drop

  def get_top_abs_correlations(df, n):
    au_corr = df.corr().abs().unstack()
    labels_to_drop = get_redundant_pairs(df)
    au_corr = au_corr.drop(labels=labels_to_drop).sort_values(ascending=False)
    return au_corr[0:n]

  print get_top_abs_correlations(df, n=n)


def view_word_results(training_data):
  """ 
    View the proportion of positives to negatives that each words in the model is associated with
  """
  word_map = {}
  for word in training_data.words:
    word_map[word] = {
      '0': 0,
      '1': 0
    }
    for i in training_data.words[word]:
      y = str(training_data.docs[i][1])
      word_map[word][y] += 1

  prop = {}
  for word in word_map:
    prop[word] = float(word_map[word]['1']) / float((word_map[word]['0'] + word_map[word]['1']))
  sorted_prop = sorted(prop.items(), key=lambda x: x[1], reverse=True)
  for word in sorted_prop:
    tot = (word_map[word[0]]['0'] + word_map[word[0]]['1'])
    if tot < 5:
      continue
    print '{}: {} ({} / {})'.format(word[0], word[1], word_map[word[0]]['1'], tot)


if __name__ == '__main__':

  # Allow user to specify N docs to use for training/testing
  cli = argparse.ArgumentParser()
  cli.add_argument('-p', '--proptraining', default=0.7, type=float,
                   help='The proportion of docs to allocate for training data. Default: 1000, Max: 1200')
  args = cli.parse_args()

  pos_dir = 'email_data/no_blacks_positives'
  neg_dir = 'email_data/no_blacks_negatives'

  # Load training/testing data from files
  training_data, test_data = load_data_sets(
    pos_dir, neg_dir,
    prop_training=args.proptraining,
    randomize=True
  )

  # print 'Viewing word correlations...'
  # view_word_correlations(training_data, prop_words=0.05, n=200)
  # raw_input()
 
  print '# training: {}'.format(len(training_data.docs))
  print '# testing: {}'.format(len(test_data.docs))

  # train model
  model = NBClassifier()
  model.train(training_data)

  # predict test data
  pred_Y, Y = model.predict_many(test_data)

  # get evaluations
  accuracy, f1, precision, recall = model.get_evaluations(pred_Y, Y)
  
  # print info/results
  print_results(training_data, test_data, accuracy, f1, precision, recall)


