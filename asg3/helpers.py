import re


def tokenize(text):
  
  # remove non alphanumeric characters
  text = re.sub(r'(\'|-|/|\\)', '', text)
  text = re.sub(r'\W', ' ', text)
  text = re.sub(r'\s+', ' ', text)
  return [s.strip() for s in text.split() if s.strip() and not (len(s.strip()) == 1 and s.strip() not in ['a', 'i', 'o', 'u'])]
