# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from statistics import mean
from pyrsistent import v
from util import manhattanDistance
from game import Directions
import random, util
import math

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)

        "*** YOUR CODE HERE ***"
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        
        
        posFood = newFood.asList()
        posGhost = [(ghost.getPosition()[0], ghost.getPosition()[1]) for ghost in newGhostStates if ghost.scaredTimer == 0]
        
        ghostDists = [manhattanDistance(newPos, ghost) for ghost in posGhost]
        minGhostDist = min(ghostDists, default = 1000)

        foodDists = [manhattanDistance(newPos, food) for food in posFood]
        minFoodDist = min(foodDists, default = 5)

        score = (1/(minFoodDist + 0.5)) - (1/(minGhostDist - 0.8)) + (successorGameState.getScore() - currentGameState.getScore())
        return score
        

    

def scoreEvaluationFunction(currentGameState: GameState):
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

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        # ghostIndex = [ i for i in range(1, gameState.getNumAgents())]

        # ##check if we already at terminal state
        # if self.depth == 0 or gameState.isWin() or gameState.isLose():
        #     return self.evaluationFunction

        # Collect Pacman legal moves and successor states
        GhostList = [i for i in range(1, gameState.getNumAgents())]
        

        def max_value(gamestate, depth):  # maximizer for pacman
            if gamestate.isWin() or gamestate.isLose() or depth == self.depth:
                return self.evaluationFunction(gamestate)

            maxval = -math.inf
            for action in gamestate.getLegalActions(0):
                maxval = max(maxval, min_value(gamestate.generateSuccessor(0, action), depth, 1))
            return maxval

        def min_value(gamestate, depth, ghostindex):  # minimizer
            
            if gamestate.isWin() or gamestate.isLose() or depth == self.depth:
                return self.evaluationFunction(gamestate)

            minval = math.inf
            for action in gamestate.getLegalActions(ghostindex):
                if ghostindex == GhostList[-1]: ##last ghost 
                    minval = min(minval, max_value(gamestate.generateSuccessor(ghostindex, action), depth + 1)) ##then goes down the next depth with pacman
                else:
                    minval = min(minval, min_value(gamestate.generateSuccessor(ghostindex, action), depth, ghostindex + 1)) ##otherwise continue to find the value for the current ghost
            return minval

        results = [(action, min_value(gameState.generateSuccessor(0, action), 0, 1)) for action in gameState.getLegalActions(0)]
        results.sort(key=lambda x: x[1])

        return results[-1][0]



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        GhostList = [i for i in range(1, gameState.getNumAgents())]
        

        def max_value(gamestate, depth, alpha, beta):  # maximizer for pacman
            if gamestate.isWin() or gamestate.isLose() or depth == self.depth:
                return self.evaluationFunction(gamestate)

            maxval = -math.inf
            for action in gamestate.getLegalActions(0):
                maxval = max(maxval, min_value(gamestate.generateSuccessor(0, action), depth, 1, alpha, beta))
                if maxval > beta:
                    return maxval
                alpha = max(alpha, maxval)
            return maxval

        def min_value(gamestate, depth, ghostindex, alpha, beta):  # minimizer
            
            if gamestate.isWin() or gamestate.isLose() or depth == self.depth:
                return self.evaluationFunction(gamestate)

            minval = math.inf
            for action in gamestate.getLegalActions(ghostindex):
                if ghostindex == GhostList[-1]: ##last ghost 
                    minval = min(minval, max_value(gamestate.generateSuccessor(ghostindex, action), depth + 1, alpha, beta)) ##then goes down the next depth with pacman
                else:
                    minval = min(minval, min_value(gamestate.generateSuccessor(ghostindex, action), depth, ghostindex + 1, alpha, beta)) ##otherwise continue to find the value for the current ghost
                if minval < alpha:
                    return minval
                beta = min(beta, minval)
            return minval
        
        def alphabeta(gamestate):
            val = -math.inf
            act = None
            alpha = -math.inf
            beta = math.inf

            for action in gamestate.getLegalActions(0):  # maximizing
                tmp = min_value(gameState.generateSuccessor(0, action), 0, 1, alpha, beta)

                if val < tmp:  # same as v = max(v, tmp)
                    val = tmp
                    act = action

                if val > beta:  # pruning leafs
                    return val
                alpha = max(alpha, tmp)

            return act

        return alphabeta(gameState)

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        GhostList = [i for i in range(1, gameState.getNumAgents())]
        

        def max_value(gamestate, depth):  # maximizer for pacman
            if gamestate.isWin() or gamestate.isLose() or depth == self.depth:
                return self.evaluationFunction(gamestate)

            maxval = -math.inf
            for action in gamestate.getLegalActions(0):
                maxval = max(maxval, exp_value(gamestate.generateSuccessor(0, action), depth, 1))
            return maxval
        
        def exp_value(gamestate, depth, ghostindex):  # minimizer
            
            if gamestate.isWin() or gamestate.isLose() or depth == self.depth:
                return self.evaluationFunction(gamestate)

            expectedval = 0
            weight = 1 / len(gamestate.getLegalActions(ghostindex))
            for action in gamestate.getLegalActions(ghostindex):
                if ghostindex == GhostList[-1]: ##last ghost 
                    expectedval += weight * max_value(gamestate.generateSuccessor(ghostindex, action), depth + 1)##then goes down the next depth with pacman
                else:
                    expectedval += weight * exp_value(gamestate.generateSuccessor(ghostindex, action), depth, ghostindex + 1) ##otherwise continue to find the value for the current ghost
            return expectedval

        results = [(action, exp_value(gameState.generateSuccessor(0, action), 0, 1)) for action in gameState.getLegalActions(0)]
        results.sort(key=lambda x: x[1])

        return results[-1][0]

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: the evaluation looks at the current game state and use the following main attributes
    distance to the closest ghost, distance to the closest food pallet, if ghost(s) are scared,
    the remaining food pallets, and current score that we have. Then I played around with the attiribute to
    find the good combinations for the evaluation scoring
    """
    "*** YOUR CODE HERE ***"
    posPacMan = currentGameState.getPacmanPosition() 
    posFood = [food for food in currentGameState.getFood().asList() if food]
    GhostStates = currentGameState.getGhostStates()
    GhostTimers = [ghostState.scaredTimer for ghostState in GhostStates]

    distToGhost = min(manhattanDistance(posPacMan, ghost.getPosition()) for ghost in GhostStates)
    closestFood = min(manhattanDistance(posPacMan, new_Food) for new_Food in posFood) if posFood else 0
    
    scaredLeft = min(GhostTimers)
    remFood = -len(posFood)
    distToGhost = 1 / (distToGhost + 1)
    closestToFood = 1 / (closestFood + 1)
    curScore = currentGameState.getScore() 

    return distToGhost + closestToFood + scaredLeft + curScore + remFood

# Abbreviation
better = betterEvaluationFunction
