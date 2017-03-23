from errors import Asg2Error
from helpers import tokenize


class NBClassifier:
  """
    Naive Bayesian classifier to detect email spam.
    Uses the Multi-Variate Bernoulli Event Model.
  """

  def __init__(self, data):
    self.data = data


  def _email_count_for_word(self, word, spam_flag=-1):
    """
      Get the number of emails that use a given word.
      User can specify an optional filter to only count emails
      that are known spam or known non-spam emails.
    """
    if word not in self.data.words:
      # word doesn't exist
      return 0

    if spam_flag == -1:
      # get total number of emails that use the word
      return len(self.data.words[word])

    # get number of emails with given word and label match
    n = 0
    for ind in self.data.words[word]:
      if self.data.emails[ind][1] == spam_flag:
        n+=1
    return n


  def _predict_email(self, x, spam_flag):
    """ Get probability of x being spam/nonspam """
    if spam_flag not in [0, 1]:
      raise Asg2Error('spam_choose')

    # multiply word probabilities for all words in x
    words = tokenize(x)
    prob = 1.0
    for word in words:
      wi = self._email_count_for_word(word, spam_flag=spam_flag)
      prob *= (float(wi) / float(self.data.num_spam()))
    return prob


  def predict_email(self, email, spam_flag):
    """ Predict if email should be classified as spam or nonspam. """
    if spam_flag not in [-1, 0, 1]:
      raise Asg2Error('spam_flag')
    
    prob_spam = _predict_email(email, 1)
    prob_nonspam = _predict_email(email, 0)


