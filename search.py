# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
import searchAgents

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

'''
A search algorithm that traverses through a graph and
returns a list of directions to a specific goal state.
Takes in a problem object and a data structure to "hold" states.
'''
def generalSearch(problem,frontier):
    visited = {} # Holds all visited states
    directions = [] # Directions to a goal state
    initialState = problem.getStartState()
    print 'Start:' , initialState
    frontier.push([(initialState,'Start',0)])
    paths = []

    while not frontier.isEmpty():
        path = frontier.pop()
        # print path
        state = path[len(path)-1][0] # Get last state on path
        #print state

        # Check if current state is a goal
        if problem.isGoalState(state):
            temp = []
            # Print path to goal state
            #print path
            # Return all directions that lead to goal state
            for trip in path:
                temp.append(trip[1]) # Get direction to path
            # Remove invalid direction
            temp.remove('Start')
            # Check for more goals
            if isinstance(problem,searchAgents.CornersProblem):
                if state in problem.goals:
                    # Save directions to corner
                    directions = temp[:]
                    problem.goals.remove(state) # Remove goal state
                    # Restart search at goal state
                    visited.clear()
                    while not frontier.isEmpty():
                        frontier.pop()
                # If all the goal states have been visited:
                if not problem.goals:
                    # Join paths to corners
                    return directions
            else:
                directions = temp[:]
                return directions

        # Proceed to state's successors
        if state not in visited:
            visited[state] = 1 # Mark state as visited
            # Push unvisited states to stack
            for s in problem.getSuccessors(state):
                if s[0] not in visited:
                    # Push path to univisted succesor onto frontier
                    sPath = path[:] # Copy current path
                    sPath.append(s) # Append succesor to path
                    frontier.push(sPath)

    return []

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    dataStruct = util.Stack()
    return generalSearch(problem,dataStruct)

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    dataStruct = util.Queue()
    return generalSearch(problem,dataStruct)

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    #costFunc = lambda somePath: if len(somePath) > 1: problem.getCostOfActions([s[1] for s in somePath])
    def costFunc(somePath):
        tempList = []
        for s in somePath:
        # If the direction is valid...
            if s[1] != 'Start':
                tempList.append(s[1])
        return problem.getCostOfActions(tempList)

    '''
    The priority queue will store the path with the lowest cost to
    the goal state in the root of the heap. This way the algorithm
    only chooses paths that have the lowest cost, instead of choosing
    deepest (dfs) or shallowest paths (bfs).
    '''
    dataStruct = util.PriorityQueueWithFunction(costFunc)
    return generalSearch(problem,dataStruct)

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""

    def aStarFunc(somePath):
        tempList = []
        for s in somePath:
        # If the direction is valid...
            if s[1] != 'Start':
                tempList.append(s[1])
        return problem.getCostOfActions(tempList) + heuristic(somePath[len(somePath)-1][0],problem)

    dataStruct = util.PriorityQueueWithFunction(aStarFunc)
    return generalSearch(problem,dataStruct)

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
