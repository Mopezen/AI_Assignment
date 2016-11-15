# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
  """
  This class outlines the structure of a search problem, but doesn't implement
  any of the methods (in object-oriented terminology: an abstract class).
  
  You do not need to change anything in this class, ever.
  """
  
  def getStartState(self):
     """
     Returns the start state for the search problem 
     """
     util.raiseNotDefined()
    
  def isGoalState(self, state):
     """
       state: Search state
    
     Returns True if and only if the state is a valid goal state
     """
     util.raiseNotDefined()

  def getSuccessors(self, state):
     """
       state: Search state
     
     For a given state, this should return a list of triples, 
     (successor, action, stepCost), where 'successor' is a 
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental 
     cost of expanding to that successor
     """
     util.raiseNotDefined()

  def getCostOfActions(self, actions):
     """
      actions: A list of actions to take
 
     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
     """
     util.raiseNotDefined()
           

def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze
  """
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first [p 85].
  
  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm [Fig. 3.7].
  
  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:
  
  print "Start:", problem.getStartState()
  print "Is the start a goal?", problem.isGoalState(problem.getStartState())
  print "Start's successors:", problem.getSuccessors(problem.getStartState())
  """
  "*** YOUR CODE HERE ***"
  stack = util.Stack() #Use a stack for depth first, children of the node were inspecting have higher position
  stack.push(Node(problem.getStartState(),[])) 
  visited = []
  while not stack.isEmpty():
    #Remove the last inserted item into the stack
    node = stack.pop()

    #Check if the node we pop off has been visited
    if node.getStartState() in visited:
      continue

    #Add the node to the visited list
    visited.append(node.getStartState())

    #No weights so we can check if we are at the goal state
    if problem.isGoalState(node.getStartState()):
      return node.getactionsList()
    else:
      #Add the current nodes sucessors to the list
      sucessors = problem.getSuccessors(node.getStartState())
      if len(sucessors) > 0:
        for index in sucessors:
          actionlist = list(node.getactionsList())
          actionlist.append(index[1])
          stack.push(Node(index[0],actionlist))

  return [] #If we can't find the node just return blank actions

def breadthFirstSearch(problem):
  "Search the shallowest nodes in the search tree first. [p 81]"
  "*** YOUR CODE HERE ***"
  queue = util.Queue() #To use a breath first search, utlize a queue so each successor is pushed for children of children
  queue.push(Node(problem.getStartState(),[]))
  visited = []
  while not queue.isEmpty():
    #Remove the last inserted item into the queue
    node = queue.pop()


    #Check if the node we pop off has been visited, if so skip over it
    if node.getStartState() in visited:
      continue

    #Add the node to the visited list
    visited.append(node.getStartState())

    #No weights so we can check if we are at the goal state
    if problem.isGoalState(node.getStartState()):
      #print "We found the node!", node.getactionsList()
      return node.getactionsList()
    else:
      #Add the current nodes sucessors to the list
      sucessors = problem.getSuccessors(node.getStartState())
      if len(sucessors) > 0:
        for index in sucessors:

          actionlist = list(node.getactionsList())
          actionlist.append(index[1])
          queue.push(Node(index[0],actionlist))

  return []
  util.raiseNotDefined()
      
def uniformCostSearch(problem):
  "Search the node of least total cost first. "
  "*** YOUR CODE HERE ***"
  queue = util.PriorityQueue() #PQueue so that nodes are order based on cost
  queue.push(Node(problem.getStartState(),[]),problem.getCostOfActions([])) #Push the sucessor node based on its cost
  visited = []
  while not queue.isEmpty():
    #Remove the last inserted item into the queue
    node = queue.pop()


    #Check if the node we pop off has been visited, if so skip over it
    if node.getStartState() in visited:
      continue

    #Add the node to the visited list
    visited.append(node.getStartState())

    #The nodes are ordered based on cost so it's okay to check if the current node it the problem state. If so it will be the optimal solution
    if problem.isGoalState(node.getStartState()):
      #print "We found the node!", node.getactionsList()
      return node.getactionsList()
    else:
      #Add the current nodes sucessors to the list
      sucessors = problem.getSuccessors(node.getStartState())
      if len(sucessors) > 0:
        for index in sucessors:
          actionlist = list(node.getactionsList())
          actionlist.append(index[1])
          queue.push(Node(index[0],actionlist),problem.getCostOfActions(actionlist))

  return []
  util.raiseNotDefined()

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  "*** YOUR CODE HERE ***"
  queue = util.PriorityQueue()
  #Use a heurisitic to define our cost 
  queue.push(Node(problem.getStartState(),[]),problem.getCostOfActions([]) + heuristic(problem.getStartState(),problem)) 
  visited = []
  while not queue.isEmpty():
    #Remove the last inserted item into the queue
    node = queue.pop()


    #Check if the node we pop off has been visited, if so skip over it
    if node.getStartState() in visited:
      continue

    #Add the node to the visited list
    visited.append(node.getStartState())

    if problem.isGoalState(node.getStartState()):
      #print "We found the node!", node.getactionsList()
      return node.getactionsList()
    else:
      #Add the current nodes sucessors to the list
      sucessors = problem.getSuccessors(node.getStartState())
      if len(sucessors) > 0:
        for index in sucessors:
          actionlist = list(node.getactionsList())
          actionlist.append(index[1])
          queue.push(Node(index[0],actionlist),problem.getCostOfActions(actionlist)+heuristic(index[0],problem))
  util.raiseNotDefined()

#Class I use to define the current node we are at. It includes the state were at and the actions to get to that state
class Node:
  def __init__(self, state, actions):
    self.state = state
    self.actions = actions
  def getStartState(self):
    return self.state
  def getactionsList(self):
    return self.actions

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch