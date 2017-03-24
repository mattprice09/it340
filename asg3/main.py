import os
from random import shuffle

from email_data import EmailData
from model import NBClassifier


def _load_data(fp):
  """ Read all .txt files within directory (and all subdirectories) """
  emails = []
  for root, dirs, files in os.walk(fp):
    for fn in files:
      if '.txt' not in fn:
        # emails are ensured to be .txt files
        continue
      # get full filepath of email
      filename = os.path.join(root, fn)
      with open(filename, 'rU') as reader:
        lines = []
        for line in reader:
          if line:
            lines.append(line)
        emails.append('\n'.join(lines))
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

  # training data object
  training_data = EmailData('training')
  training_data.add_emails(nsp_training, 0)
  training_data.add_emails(sp_training, 1)

  # test data object
  test_data = EmailData('test')
  test_data.add_emails(nsp_testing, 0)
  test_data.add_emails(sp_testing, 1)

  return training_data, test_data


def _print_data_info(data):
  """ Helper that prints an EmailData's info """

  print '    -------------------------------'
  fmt = '{:<25} {:<6}'
  print fmt.format('    # spam emails', data.num_spam())
  print fmt.format('    # non-spam emails', data.num_nonspam())
  print fmt.format('    # total emails', len(data.emails))
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


if __name__ == '__main__':

  # Load training/testing data from files
  training_data, test_data = load_data_sets()

  model = NBClassifier()
  model.train(training_data)

  # predict test data
  pred_Y, Y = model.predict_many(test_data)

  # get evaluations
  accuracy, f1, precision, recall = model.get_evaluations(pred_Y, Y)
  
  # print info/results
  print_results(training_data, test_data, accuracy, f1, precision, recall)


