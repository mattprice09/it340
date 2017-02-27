from copy import deepcopy
import math
from random import random as rand
from random import randint, shuffle
import time

from fitness import fitness


# Represents an 8-queens object
class EightQueens:

  def __init__(self, initial=[]):
    if initial:
      if isinstance(initial, list):
        self.initial = initial
      elif isinstance(initial, str):
        self.initial = [int(i) for i in initial.split('-')]
    else:
      self.initial = self.random_initial_state()

    self.state = deepcopy(self.initial)
    self.fitness = fitness(self.state)

  def __str__(self):
    return '-'.join([str(i) for i in self.initial])

  # Mutate the state by moving a random queen to a random (new) spot on the board
  def mutate(self):
    i = randint(0, 7)
    before = self.state[i]
    r = randint(1, 8)
    while r == before:
      r = randint(1, 8)
    self.state[i] = r
    self.fitness = fitness(self.state)

  # Create random initial state
  def random_initial_state(self):
    arr = [i for i in range(1, 9)]
    shuffle(arr)
    return arr

# Generate a random new population
def new_population(n):
  population = []
  for i in range(n):
    population.append(EightQueens())
  return population

# Helper to get childrens' DNA
def reproduce(x, y):
  c = randint(1, len(x))
  return x[0:c] + y[c:len(x)]

def genetic_algorithm(population, num_random_restarts=1000):

  restart_population_size = len(population)

  while num_random_restarts >= 0:
    while len(population) > 1:
      # Create list in order to emulate accurate probabilities of choosing parents
      randoms = []
      for i in range(len(population)):
        for j in range(int(population[i].fitness)):
          randoms.append(i)
      shuffle(randoms)

      # Each pair of parents creates 1 child
      child_population = []
      fittest_child_sc = -1
      for i in range(int(math.floor(len(population)/2))):

        # Get random parents
        x = randoms[randint(0, len(randoms)-1)]
        y = randoms[randint(0, len(randoms)-1)]
        while y == x:
          y = randoms[randint(0, len(randoms)-1)]
        x = population[x]
        y = population[y]

        child = reproduce(str(x), str(y))
        child = EightQueens(child)
        # 10% chance to mutate
        if rand() <= 0.1 and child.fitness != 28:
          child.mutate()
        child_population.append(child)

      # Stop if we found a solution, otherwise run GA on new child population
      population = child_population
      for child in population:
        if child.fitness == 28:
          return population

    population = new_population(restart_population_size)
    num_random_restarts -= 1

  return child_population

if __name__ == '__main__':

  restart_pop_size = 30
  num_random_restarts = 1000

  # Test-run the algorithm 20 times
  times = []
  nsuccess = 0
  ntests = 40
  for i in range(ntests):
    population = new_population(restart_pop_size)

    st = time.time()
    best_fit = -1

    # Initial population
    for eq in population:
      best_fit = max(eq.fitness, best_fit)
      # print 'Initial fitness: {}'.format(eq.fitness)
    
    # Final population
    population = genetic_algorithm(population, num_random_restarts=num_random_restarts)
    for eq in population:
      best_fit = max(eq.fitness, best_fit)
      # print 'Final fitness: {}'.format(eq.fitness)

    if best_fit == 28:
      print 'Found solution! ({} sec)'.format(time.time() - st)
      nsuccess += 1
    else:
      print 'No solution found after {} seconds'.format(time.time() - st)
      # print 'Best solution was fitness score: {}'.format(best_fit)
    times.append(time.time() - st)

  # print results
  avgtime = 0
  for t in times:
    avgtime += t
  avgtime /= ntests
  print 'RESULTS (restart_pop_size={}, num_random_restarts={}'.format(restart_pop_size, num_random_restarts)
  print 'Average time taken to run genetic algorithm: {}'.format(avgtime)
  print '% Success of genetic algorithm implementation: {} %'.format((float(nsuccess) / float(ntests))*100.0)


