# Descriptions:
# search_history is a list
# explored is a list
# action() is a function that generates a list of possible results
from copy import deepcopy
import math
from random import shuffle
import sys
import time

import numpy as np

from action import action

class NPuzzle:

  def __init__(self, N, initial=None):

    # puzzle must be a perfect square
    if math.sqrt(N+1) != int(math.sqrt(N+1)):
      print '> ERROR: Puzzle size must be a perfect square.'
      print '> Example: For a 2x2 puzzle, the size is 4.'
      sys.exit()

    if initial:
      self.initial = deepcopy(initial)
    else:
      self.initial = self.random_initial_state(N)

  # Generate a random initial state of size N
  def random_initial_state(self, N):
    arr = np.arange(N+1)
    shuffle(arr)
    arr = arr.reshape((int(math.sqrt(N))+1, -1))
    return arr

  def solvable(self, goal):

    # Check if the state has no empty slot
    x,y = np.where(goal == 0)
    if not list(x):
      return []

    start_shape = goal.shape[0]

    search_history = []
    possible_moves = action(goal)
    done = False
    search_history.extend(possible_moves)

    # Store visited states as a set of keys to reduce time complexity
    explored_lookup = set()
    for move in possible_moves:
      explored_lookup.add(self._matrix_to_string_key(move))

    # Get all solveable states
    while not done:
      new_states = []

      # search one layer
      while search_history:
        curr = search_history.pop(0)
        # check possible actions for unvisited state
        for step in action(curr):
          str_id = self._matrix_to_string_key(step)
          if str_id not in explored_lookup:
            explored_lookup.add(str_id)
            new_states.append(step)

      if not new_states:
        done = True
      else:
        # begin new layer of searching
        search_history.extend(new_states)

    # decompress back from string to numpy matrix
    explored = []
    for key in explored_lookup:
      explored.append(self._string_key_to_matrix(key, start_shape))

    return explored

  # Convert 2d numpy array (array([[5, 1, 0], [2, 4, 3]])) into string ("5-1-0-2-4-3")
  def _matrix_to_string_key(self, matrix):
    return '-'.join([str(ele) for ele in list(matrix.reshape(matrix.size))])

  # Convert string ("5-1-0-2-4-3") into 2d numpy array (array([[5, 1, 0], [2, 4, 3]]))
  def _string_key_to_matrix(self, string_key, start_shape):
    arr = np.asarray([int(x) for x in string_key.split('-')])
    return arr.reshape((start_shape, -1))

if __name__ == '__main__':
  N = 8
  puzzle = NPuzzle(N)
  st = time.time()
  states = puzzle.solvable(puzzle.initial)
  print '> ({0:.2f} sec) '.format(time.time() - st),
  print 'Finished solving {}-puzzle. There are {} solveable states'.format(N, len(states))

