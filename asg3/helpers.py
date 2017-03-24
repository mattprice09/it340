import re


def tokenize(text):
  
  # remove non alpha-numeric characters
  text = re.sub(r'\W', ' ', text.strip())
  return text.split()
