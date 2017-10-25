import math
import re

from errors import Asg3Error
from helpers import tokenize


class NBClassifier:
  """
    Naive Bayesian classifier to detect doc positive.
    Uses the Multi-Variate Bernoulli Event Model.
  """

  def __init__(self):
    pass


  def _doc_count_for_word(self, word, flag=-1):
    """
      Get the number of docs that use a given word.
      User can specify an optional filter to only count docs
      that are known positive or known non-positive docs.
    """
    if word not in self.X.words:
      # word doesn't exist
      return 0

    if flag == -1:
      # get total number of docs that use the word
      return len(self.X.words[word])

    # get number of docs with given word and label match
    n = 0
    for doc_ind in self.X.words[word]:
      if self.X.docs[doc_ind][1] == flag:
        n += self.X.words[word][doc_ind]
    return n


  def _get_evaluations(self, pred_Y, Y):
    """ helper that calculates TP, FP, TN, FN values """

    tp = fp = tn = fn = 0
    for i in range(len(pred_Y)):
      if pred_Y[i] == 1 and Y[i] == 1:
        tp += 1
      elif pred_Y[i] == 0 and Y[i] == 0:
        tn += 1
      elif pred_Y[i] == 1 and Y[i] == 0:
        fp += 1
      else:
        fn += 1
    tp = float(tp)
    fp = float(fp)
    tn = float(tn)
    fn = float(fn)
    return tp, fp, tn, fn


  def _predict_doc(self, x, flag):
    """ Get probability of x being positive/negative """

    if flag == 1:
      denom = self.X.num_positive()
    else:
      denom = self.X.num_negative()
    denom += self.X.vocab_size()

    # multiply word probabilities for all words in x
    words = tokenize(x)
    # prob = 1.0
    # for word in words:
    #   wi = self._doc_count_for_word(word, flag=flag)
    #   # utilize the Laplace Smooth
    #   prob *= ((float(wi)+1.0) / (float(denom)+2.0))

    prob = math.log(self.X.priors[str(flag)])
    for word in words:
      wi = self._doc_count_for_word(word, flag=flag)
      # utilize the Laplace Smooth
      prob += math.log((float(wi)+1.0) / (float(denom)+2.0))

    # prob *= math.log(self.X.priors[str(flag)])

    return prob


  def get_evaluations(self, pred_Y, Y):
    """ Calculate the F1 score from prediction results """
    
    tp, fp, tn, fn = self._get_evaluations(pred_Y, Y)

    # calculate F1
    try:
      precision = tp / (tp+fp)
    except ZeroDivisionError:
      precision = tp
    try:
      recall = tp / (tp+fn)
    except ZeroDivisionError:
      recall = tp
    try:
      f1 = 2.0 * ((precision*recall) / (precision+recall))
    except ZeroDivisionError:
      f1 = 0.0
    # calculate accuracy
    accuracy = (tp+tn) / (tp+fp+tn+fn)

    return accuracy, f1, precision, recall


  def predict(self, doc):
    """ Predict if doc should be classified as positive or negative. """
    
    prob_positive = self._predict_doc(doc, 1)
    prob_negative = self._predict_doc(doc, 0)

    if prob_positive > prob_negative:
      return 1
    return 0


  def predict_many(self, X):
    """ Predict many docs """

    pred_Y = []
    Y = []
    for doc in X.docs:
      pred_Y.append(self.predict(doc[0]))
      Y.append(doc[1])

    return pred_Y, Y


  def save(self):
    """ Save the model into a form that can be loaded back into an object """
    pass


  def train(self, X):
    """ Train by simply storing the data """
    self.X = X

