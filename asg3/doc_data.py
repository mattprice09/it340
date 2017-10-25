from copy import deepcopy
import json
import re

from errors import Asg3Error
from helpers import tokenize


class DocData:
  """
    Represents doc data in a structured format.
      docs: list of tuples containing the data.
        tuple[0] is the doc string, tuple[1] indicates
        whether it is positive or non-positive.
        -1 -> unknown
        0 -> negative
        1 -> positive
      label_count: keeps a count of the number of docs by label
      name: given id for the object
      words: all unique words from data, mapped to list of 
        indexes of docs that use that word
  """


  def __init__(self, name, priors):
    self.docs = []
    self.label_count = {}
    self.name = name
    self.priors = deepcopy(priors)
    self.vocab = set()
    self.words = {}

    # initialize vars
    for i in range(2):
      self.label_count[i] = 0


  def add_doc(self, doc, flag):
    """ 
      Adds doc and doc components to class data.
        -1 -> unknown
        0 -> negative
        1 -> positive
    """

    self.docs.append((doc, flag))
    
    # add the doc's words
    tokens = tokenize(doc)

    # update the vocab
    self.vocab.update(tokens)

    if flag != -1:
      self.label_count[flag] += len(tokens)

    # get the number of times that this word appears in the doc
    word_counts = {}
    for word in tokens:
      if word not in word_counts:
        word_counts[word] = 0
      word_counts[word] += 1
      
    # increment all of the word counts
    for word in tokens:
      if word not in self.words:
        self.words[word] = {}
      self.words[word][len(self.docs)-1] = word_counts[word]

    # for word in tokens:
    #   if word not in self.words:
    #     self.words[word] = set()
    #   # associate this word with the index of this doc
    #   self.words[word].add(len(self.docs)-1)


  def add_docs(self, docs, flag):
    """
      Add doc data to the object. Must specify the label to use for all included docs.
        -1 -> unknown
        0 -> negative
        1 -> positive
    """
    if flag not in [-1, 0, 1]:
      raise Asg3Error('flag')

    for doc in docs:
      self.add_doc(doc, flag)


  def load(self, doc_data_obj):
    """
      Loads a model from a saved one
    """
    obj = json.load(doc_data_obj)
    self.docs = obj['docs']
    self.label_count = obj['label_count']
    self.name = obj['name']
    self.priors = obj['priors']
    self.vocab = set(obj['vocab'])
    self.words = {w: set(self.words[w]) for w in obj['words']}


  def num_positive(self):
    return self.label_count[1]


  def num_positive_docs(self):
    n = 0
    for doc in self.docs:
      if doc[1] == 1:
        n += 1
    return n


  def num_negative(self):
    return self.label_count[0]


  def num_negative_docs(self):
    n = 0
    for doc in self.docs:
      if doc[1] == 0:
        n += 1
    return n


  def stringify(self):
    """
      Saves the model to a file for later loading
    """
    return json.dumps({
      'docs': self.docs,
      'label_counts': self.label_count,
      'name': self.name,
      'priors': self.priors,
      'vocab': list(self.vocab),
      'words': {w: list(self.words[w]) for w in self.words}
    })


  def vocab_size(self):
    return len(self.vocab)

