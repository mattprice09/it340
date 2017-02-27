# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 08:37:08 2017

@author: xfang13

"""
import numpy as np

def fitness(Input):
  #Input should be a list

  #Step1: make the state out of the Input
  state = np.zeros((8,8))
  for j in range(8):
    state[Input[j]-1][j] = 1
      

  #Step2: find the fitness of the state
  attacks = 0
  k = -1
  for j in range(8):
    k += 1
    #direction 1: the east
    for l in range(k+1,8):
      attacks += state[state[:,j].argmax()][l]
  
    #direction 2: the northeast
    row = state[:,j].argmax()
    column = j
    while row > 0 and column < 7:
      row -= 1
      column += 1
      attacks += state[row][column]
      
    #direction 3: the southeast
    row = state[:,j].argmax()
    column = j
    while row < 7 and column < 7:
      row += 1
      column += 1
      attacks += state[row][column]
      
  return 28 - attacks

        
      
if __name__=='__main__':
  print fitness([2, 4, 7, 4, 8, 5, 1, 3])