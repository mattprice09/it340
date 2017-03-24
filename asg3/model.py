from errors import Asg3Error
from helpers import tokenize


class NBClassifier:
  """
    Naive Bayesian classifier to detect email spam.
    Uses the Multi-Variate Bernoulli Event Model.
  """

  def __init__(self):
    pass


  def _email_count_for_word(self, word, spam_flag=-1):
    """
      Get the number of emails that use a given word.
      User can specify an optional filter to only count emails
      that are known spam or known non-spam emails.
    """
    if word not in self.X.words:
      # word doesn't exist
      return 0

    if spam_flag == -1:
      # get total number of emails that use the word
      return len(self.X.words[word])

    # get number of emails with given word and label match
    n = 0
    for ind in self.X.words[word]:
      if self.X.emails[ind][1] == spam_flag:
        n+=1
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


  def _predict_email(self, x, spam_flag):
    """ Get probability of x being spam/nonspam """
    if spam_flag not in [0, 1]:
      raise Asg3Error('spam_choose')

    if spam_flag == 1:
      denom = self.X.num_spam()
    else:
      denom = self.X.num_nonspam()

    # multiply word probabilities for all words in x
    words = tokenize(x)
    prob = 1.0
    for word in words:
      wi = self._email_count_for_word(word, spam_flag=spam_flag)
      # utilize the Laplace Smooth
      prob *= ((float(wi)+1.0) / (float(denom)+2.0))

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


  def predict(self, email):
    """ Predict if email should be classified as spam or nonspam. """
    
    prob_spam = self._predict_email(email, 1)
    prob_nonspam = self._predict_email(email, 0)

    if prob_spam > prob_nonspam:
      return 1
    return 0


  def predict_many(self, X):
    """ Predict many emails """

    pred_Y = []
    Y = []
    for email in X.emails:
      pred_Y.append(self.predict(email[0]))
      Y.append(email[1])

    return pred_Y, Y


  def train(self, X):
    """ Train by simply storing the data """
    self.X = X

