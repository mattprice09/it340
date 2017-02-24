# -*- coding: utf-8 -*-
"""
Created on Mon Jan 09 13:23:41 2017

@author: xfang13

The Romania problem
"""
import random
import time

Romania_Map = {'Oradea':[('Zerind',71),('Sibiu',151)],
         'Zerind':[('Arad',75),('Oradea',71)],
         'Arad':[('Zerind',75),('Sibiu',140),('Timisoara',118)],
         'Timisoara':[('Arad',118),('Lugoj',111)],
         'Lugoj':[('Timisoara',111),('Mehadia',75)],
         'Mehadia':[('Lugoj',70),('Drobeta',75)],
         'Drobeta':[('Mehadia',75),('Craiova',120)],
         'Craiova':[('Drobeta',120),('Rimnicu Vilcea',146),('Pitesti',138)],
         'Rimnicu Vilcea':[('Craiova',146),('Sibiu',80),('Pitesti',97)],
         'Sibiu':[('Oradea',151),('Arad',140),('Fagaras',99),('Rimnicu Vilcea',80)],
         'Fagaras':[('Sibiu',99),('Bucharest',211)],
         'Pitesti':[('Rimnicu Vilcea',97),('Craiova',138),('Bucharest',101)],
         'Bucharest':[('Fagaras',211),('Pitesti',101),('Giurgiu',90),('Urziceni',85)],
         'Giurgiu':[('Bucharest',90)],
         'Urziceni':[('Bucharest',85),('Vaslui',142),('Hirsova',98)],
         'Neamt':[('Iasi',87)],
         'Iasi':[('Neamt',87),('Vaslui',92)],
         'Vaslui':[('Iasi',92),('Urziceni',142)],
         'Hirsova':[('Urziceni',98),('Eforie',86)],
         'Eforie':[('Hirsova',86)]       
        }

class PathFinderAgent(object):

  class PathNode:
    def __init__(self):
      self.parent = ''
      self.state = 'OPEN'
      self.path_cost = 0


  def __init__(self, Map):
    self._map_as_nested_dict(Map)
    self.nodes = { key: self.PathNode() for key in self.map }
    self.route = []
    self.total_cost = 0

  def _map_as_nested_dict(self, Map):
    self.map = {}
    for key in Map:
      self.map[key] = { k: cost for k, cost in Map[key] }

  def _set_route_data(self):
    self.route = []
    city = self.current_city
    while self.nodes[city].state != 'START':
      self.route.append(city)
      city = self.nodes[city].parent
    self.route.append(city)
    self.route = list(reversed(self.route))

  def _unvisit_node(self):
    if self.nodes[self.current_city].state == 'START':
      print '\n> No route could be found.'
      return False

    self.nodes[self.current_city].path_cost == 0
    self.nodes[self.current_city].state == 'OPEN'
    self.current_city = self.nodes[self.current_city].parent
    return True

  def _visit_node(self, parent, child):
    self.nodes[child].state = 'VIS'
    self.nodes[child].parent = parent
    # print parent
    # print child
    self.nodes[child].path_cost = self.nodes[parent].path_cost + self.map[parent][child]
    self.current_city = child

  def solve(self, start, end):
    flag = True
    self.current_city = start
    self.nodes[self.current_city].state = 'START'
    while flag:
      if self.current_city == end:
        flag = False
      else:
        #Make a list of next cities: Observing
        cities = self.map[self.current_city]
        #See if the destination is in the next cities' list
        if end in cities:
          self._visit_node(self.current_city, end)
        else:
          moved = False
          while not moved:
            for child in cities:
              if self.nodes[child].state == 'OPEN':
                self._visit_node(self.current_city, child)
                moved = True
                break
            if not moved:
              success_move = self._unvisit_node()

              # Check if we we're stuck
              if not success_move:
                self.nodes[self.current_city].state == 'OPEN'
                self.current_city = ''
                flag = False
                break
              moved = True

    self.total_cost = self.nodes[self.current_city].path_cost
    self._set_route_data()
        
if __name__ == '__main__':
  st = time.time()
  agent = PathFinderAgent(Romania_Map)
  agent.solve('Arad','Neamt')
  print agent.route, agent.total_cost
  print '{} seconds'.format(st - time.time())    
