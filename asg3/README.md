# Asg3

This project is a Naive Bayesian Classifier that attempts to predict whether an email is spam or non-spam. It uses the Multi-Variate Bernoulli Event Model.

To run the program, simply run:

```
$ python main.py
```

There are 1200 emails total in the dataset. By default, the program will use 1000 emails for the training set and 200 emails for the testing set, split evenly between spam/non-spam emails. The emails are randomly chosen at runtime.

There is an option to change this distribution of data between training/testing. To change the amount of training data to use for each spam and non-spam, specify the `-n` option at runtime. For example, if you want to use 900 emails for training and 300 for testing, run:

```
$ python main.py -n 900
```

Thus for clarification, the following two commands are equivalent:

```
$ python main.py
$ python main.py -n 1000
```
