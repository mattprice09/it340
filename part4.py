from random import shuffle

# An unsorted, always balanced binary tree that adds elements in the order in which they were received.
# Utilizes the iterative deepening DFS algorithm in order to find elements
class Tree:

  class Node:
    def __init__(self, data):
      self.data = data
      self.l = None
      self.r = None

  def __init__(self, root_data):
    self.root = self.Node(root_data)

  # Adds a value in the next open available slot (first open slot in deepest unfilled layer)
  def add_unsorted(self, data):
    if self.root == None:
      self.root = self.Node(data)

    queue = [self.root]
    while queue:
      curr = queue.pop(0)
      if not curr:
        continue
      if curr.l == None:
        curr.l = self.Node(data)
        return
      elif curr.r == None:
        curr.r = self.Node(data)
        return
      else:
        queue.append(curr.l)
        queue.append(curr.r)

  # helper to recursively search for item in tree
  def _depth_limited_search(self, node, goal, limit):
    if node == None:
      return -1
    if node.data == goal:
      # found goal
      return limit
    if limit == 0:
      # don't go any deeper
      return -2

    cutoff = False
    # Left subtree
    res = self._depth_limited_search(node.l, goal, limit-1)
    if res >= 0:
      return res
    elif res == -2:
      cutoff = True
    # Right subtree
    res = self._depth_limited_search(node.r, goal, limit-1)
    if res >= 0:
      return res
    elif res == -2:
      cutoff = True
    if cutoff:
      return -2

    # No solution found
    return -1

  # initial recursive call
  def depth_limited_search(self, goal, limit):
    return self._depth_limited_search(self.root, goal, limit)

  # Use the IDS algorithm to find an item in a tree
  # Returns the depth of the item if found, otherwise -1 if not found
  def find(self, goal):
    depth = 0
    searchable = True
    # Expand by 1 depth at a time
    while searchable:
      res = self.depth_limited_search(goal, depth)
      if res == -1:
        # There is no solution
        searchable = False
      elif res >= 0:
        # Found solution
        return depth

      # Check next depth layer
      depth += 1

    return -1

  # helper that recursively prints tree in pre-order fashion
  def _print_tree(self, lvl, node):
    if not node:
      return

    indent = ''
    for i in range(lvl):
      indent += '\t'
    print '{}{}'.format(indent, node.data)
    self._print_tree(lvl+1, node.l)
    self._print_tree(lvl+1, node.r)

  # Print the tree's node data in a pre-order fashion
  def print_tree(self):
    self._print_tree(0, self.root)


# Get a new tree with N randomly generated integer values
def generate_random_tree(size):
  nums = [i for i in range(size)]
  shuffle(nums)

  tree = Tree(nums[0])
  curr = nums.pop(0)
  while nums:
    curr = nums.pop(0)
    tree.add_unsorted(curr)
  return tree

if __name__ == '__main__':
  N = 85
  tree = generate_random_tree(N)
  # tree.print_tree()

  level = tree.find(N+1)
  if level != -1:
    print 'ERROR: the element should not have existed in the tree'
  level = tree.find(N-1)
  if level == -1:
    print 'ERROR: the element should have been found'

  print 'Success.'

