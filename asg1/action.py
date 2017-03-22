# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 17:13:01 2017

@author: xfang13
8-puzzle problem using DFS and BFS
"""

import numpy as np
import copy


def action(state):
  x,y = np.where(state == 0)
  x = x[0]
  y = y[0]
  result = []
  if x + 1 < state.shape[0]:
    state_copy = copy.deepcopy(state)
    temp = state_copy[x][y]
    state_copy[x][y] = state_copy[x+1][y]
    state_copy[x+1][y] = temp
    result.append(state_copy)
  if x - 1 >= 0:
    state_copy = copy.deepcopy(state)
    temp = state_copy[x][y]
    state_copy[x][y] = state_copy[x-1][y]
    state_copy[x-1][y] = temp
    result.append(state_copy)
  if y + 1 < state.shape[0]:
    state_copy = copy.deepcopy(state)
    temp = state_copy[x][y]
    state_copy[x][y] = state_copy[x][y+1]
    state_copy[x][y+1] = temp
    result.append(state_copy)
  if y - 1 >= 0:
    state_copy = copy.deepcopy(state)
    temp = state_copy[x][y]
    state_copy[x][y] = state_copy[x][y-1]
    state_copy[x][y-1] = temp
    result.append(state_copy)
    
  return result


if __name__ == '__main__':
  results = action(np.asarray([[0,1],[2,3]])) 
  print results
