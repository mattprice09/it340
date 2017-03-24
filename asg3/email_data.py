import re

from errors import Asg3Error
from helpers import tokenize


class EmailData:
  """
    Represents email data in a structured format.
      emails: list of tuples containing the data.
        tuple[0] is the email string, tuple[1] indicates
        whether it is spam or non-spam.
        -1 -> unknown
        0 -> nonspam
        1 -> spam
      label_count: keeps a count of the number of emails by label
      name: given id for the object
      words: all unique words from data, mapped to list of 
        indexes of emails that use that word
  """


  def __init__(self, name):
    self.emails = []
    self.label_count = {}
    self.name = name
    self.words = {}

    # initialize vars
    for i in range(2):
      self.label_count[i] = 0


  def _add_email(self, email, spam_flag):
    """ Adds email and email components to class data. """
    self.emails.append((email, spam_flag))
    if spam_flag != -1:
      self.label_count[spam_flag] += 1
    # add the email's words
    tokens = tokenize(email)
    for word in tokens:
      if word not in self.words:
        self.words[word] = set()
      # associate this word with the index of this email
      self.words[word].add(len(self.emails)-1)


  def add_emails(self, emails, spam_flag):
    """
      Add email data to the object. Must specify the label to use for all included emails.
        -1 -> unknown
        0 -> nonspam
        1 -> spam
    """
    if spam_flag not in [-1, 0, 1]:
      raise Asg3Error('spam_flag')

    for email in emails:
      self._add_email(email, spam_flag)


  def num_spam(self):
    return self.label_count[1]


  def num_nonspam(self):
    return self.label_count[0]

