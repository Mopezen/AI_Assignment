# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
from random import randint
import random, util

from game import Agent

class ReflexAgent(Agent):
  """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
  """


  def getAction(self, gameState):
    """
    You do not need to change this method, but you're welcome to.

    getAction chooses among the best options according to the evaluation function.

    Just like in the previous project, getAction takes a GameState and returns
    some Directions.X for some X in the set {North, South, West, East, Stop}
    """
    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions()

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    bestScore = max(scores)
    print "Best Score: ",bestScore
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best

    "Add more of your code here if you want to"

    return legalMoves[chosenIndex]

  def evaluationFunction(self, currentGameState, action):
    """
    Design a better evaluation function here.

    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (oldFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.

    Print out these variables to see what you're getting, then combine them
    to create a masterful evaluation function.
    """
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    oldFood = currentGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    "*** YOUR CODE HERE ***"
    #Get a list of food locations
    foodList = oldFood.asList()
    #Get a list of the ghost locations
    gPosList = successorGameState.getGhostPositions()

    #Setup default ints.
    minManDist = 9999
    minManGhostDist = 9999

    #For each food in the list check the manhattan distance from
    #Pacman. If we get a smaller distance than our current smallest distance
    #record the new distance
    for i in range(len(foodList)):
      currentManDist = manhattanDistance(newPos,foodList[i])
      if currentManDist < minManDist:
        minManDist = currentManDist

    #For each ghost in the list check the manhattan distance from
    #Pacman. If we get a smaller distance than our current smallest distance
    #record the new distance
    for gPos in gPosList:
      currentManDist2 = manhattanDistance(gPos,newPos)
      if currentManDist2 < minManGhostDist:
        minManGhostDist = currentManDist2

    #If we aren't right on a food item check to see how close we are to food versus
    #a ghost. If we are on a food item check to see that we aren't on a ghost also!
    #Lastly if we are on a food item but not on ghost return an extremely postive value.
    if minManDist != 0:
      if minManGhostDist !=0:
        return 2 * (1.0/minManDist) * minManGhostDist
      else:
        if min(newScaredTimes) > 0:
          return 2 * (1.0/minManDist)
        else:
          return -1000000
    else:
      if minManGhostDist !=0:
        return 1000000
      else:
        return -1000000
    return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
  """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
  """
  return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
  """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
  """

  def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
    self.index = 0 # Pacman is always agent index 0
    self.evaluationFunction = util.lookup(evalFn, globals())
    self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent (question 2)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction.

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    "*** YOUR CODE HERE ***"
    #This method is a minmax search for multiple min agents.
    #The inputs are the current state to be evaluated, the depth we are at and the agent number
    def minMaxValue(agentNum,gameState,depth):
      if (depth == self.depth and agentNum == gameState.getNumAgents()) or gameState.isWin() or gameState.isLose():
        return self.evaluationFunction(gameState)
      elif agentNum == gameState.getNumAgents():
        #If the agent number is equal to the number of agents in the list
        #We must be at a max node, so switch over
        agentNum = 0
        depth += 1

      #For the current agent get it's available actions then preform a minmax search on them.
      #Depending on if we're min or max return the mimimun or maximum value respectively
      legalActions = gameState.getLegalActions(agentNum)
      num = 0
      if agentNum == 0:
        legalActions.remove(Directions.STOP)
        num = float('-inf')
      else:
        num = float('inf')
        
      for actions in legalActions:
        if agentNum == 0:
          num = max(num,minMaxValue(agentNum + 1,gameState.generateSuccessor(agentNum, actions),depth))
        else:
          num = min(num,minMaxValue(agentNum + 1,gameState.generateSuccessor(agentNum, actions),depth))
      return num

    #Start the minmax search for the root max node.  
    legalActions = gameState.getLegalActions(0)
    legalActions.remove(Directions.STOP)
    scores = float('-inf')
    operation = None
    for actions in legalActions:
      oldScore = scores
      currentScore = minMaxValue(1,gameState.generateSuccessor(0, actions),1)
      if currentScore > oldScore:
        operation = actions
        scores = currentScore
      elif currentScore == oldScore:
        #If two scores are equal randomize to hopefully avoid loops
        if randint(0,1):
          operation = actions
          scores = currentScore
    return operation

    

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"
    def minMaxValue(agentNum,gameState,depth,alpha,beta):
      if (depth == self.depth and agentNum == gameState.getNumAgents()) or gameState.isWin() or gameState.isLose():
        return self.evaluationFunction(gameState)
      elif agentNum == gameState.getNumAgents():
        agentNum = 0
        depth += 1
      
      legalActions = gameState.getLegalActions(agentNum)
      num = 0
      if agentNum == 0:
        legalActions.remove(Directions.STOP)
        num = float('-inf')
      else:
        num = float('inf')
      
      #For the current agent get it's available actions then preform a minmax search on them.
      #Depending on if we're min or max return the mimimun or maximum value respectively.
      #If we get a value less than alpha or greater than beta then just return that value!     
      for actions in legalActions:
        if agentNum == 0:
          num = max(num,minMaxValue(agentNum + 1,gameState.generateSuccessor(agentNum, actions),depth,alpha,beta))
          if num >= beta:
            return num
          alpha = max(alpha,num)
        else:
          num = min(num,minMaxValue(agentNum + 1,gameState.generateSuccessor(agentNum, actions),depth,alpha,beta))
          if num <= alpha:
            return num
          beta = min(beta,num)
      return num

    legalActions = gameState.getLegalActions(0)
    legalActions.remove(Directions.STOP)
    scores = float('-inf')
    operation = None
    for actions in legalActions:
      oldScore = scores
      currentScore = minMaxValue(1,gameState.generateSuccessor(0, actions),1,float('-inf'),float('inf'))
      if currentScore > oldScore:
        operation = actions
        scores = currentScore
      elif currentScore == oldScore:
        #Randomize to hopefully avoid loops
        if randint(0,1):
          operation = actions
          scores = currentScore
    return operation

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (question 4)
  """

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
  """
  "*** YOUR CODE HERE ***"
  util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

