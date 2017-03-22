import os
from random import shuffle
import sys


def _load_data(fp):
  """ Read all .txt files within directory (and all subdirectories) """
  emails = []
  for root, dirs, files in os.walk(fp):
    for fn in files:
      if '.txt' not in fn:
        # emails are ensured to be .txt files
        continue
      # get full filepath of email
      email = os.path.join(root, fn)
      emails.append(email)
  return emails


def load_data_sets(N_training=500):
  """ Get a sample data set of size N of either training or testing data """
  nonspam = _load_data('email_data/Ham/')
  spam = _load_data('email_data/Spam')

  # randomize subsets for training and testing, for spam and non-spam
  shuffle(nonspam)
  shuffle(spam)
  nsp_training = nonspam[:N_training]
  sp_training = spam[:N_training]
  nsp_testing = nonspam[N_training:]
  sp_testing = spam[N_training:]

  return nsp_training, sp_training, nsp_testing, sp_testing


if __name__ == '__main__':

  nsp_training, sp_training, nsp_testing, sp_testing = load_data_sets()

