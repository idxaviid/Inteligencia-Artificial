# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


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

class Node():
    def __init__(self, path=[], direction=[], cost=0):
        self.path = path
        self.direction = direction
        self.cost = cost

def genericSearch(searchType, problem, heuristic=None):
    
    if searchType == "DFS":
        fringe = util.Stack()
    elif searchType == "BFS":
        fringe = util.Queue()
    elif searchType == "UCS" or searchType == "A*":
        fringe = util.PriorityQueue()
    else:
        print "Error: invalid searchType"
        exit()

    firstNode = Node([problem.getStartState()])
    closedSet = []

    if searchType == "UCS" or searchType == "A*":
        fringe.push(firstNode, 0)
    else:
        fringe.push(firstNode)

    while not fringe.isEmpty():
        node = fringe.pop()
        currentState = node.path[-1]
        if currentState not in closedSet:
            if problem.isGoalState(currentState):
                return node.direction
            else:
                newNodes = problem.getSuccessors(currentState)
                for newNode in newNodes:

                    newPath = node.path + [newNode[0]]
                    newDirection = node.direction + [newNode[1]]
                    newCost = node.cost + newNode[2]

                    datNewNode = Node(newPath, newDirection, newCost)

                    if searchType == "UCS":
                        fringe.push(datNewNode, newCost)
                    elif searchType == "A*":
                        fringe.push(datNewNode, newCost + heuristic(newNode[0], problem))
                    else:
                        fringe.push(datNewNode)

                closedSet.append(currentState)


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    return genericSearch("DFS", problem)

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"
    return genericSearch("BFS", problem)

def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"
    return genericSearch("UCS", problem)

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"

    return genericSearch("A*", problem, heuristic)
    # fringe = util.PriorityQueue()
    # datNewNode = Node([problem.getStartState()])
    # fringe.push(datNewNode, 0)
    # closedSet = []
    
    # while not fringe.isEmpty() :
    #     node = fringe.pop()
    #     currentState = node.path[-1]
    #     currentCost = node.cost
    #     if currentState in closedSet:
    #         continue
    #     if problem.isGoalState(currentState):
    #         return node.direction
    #     addingNodes = problem.getSuccessors(currentState)
    #     for addNode in addingNodes:
    #         newCost = currentCost+addNode[2]
    #         blahNewNode = Node(node.path + [addNode[0]], node.direction + [addNode[1]], node.cost + newCost)
    #         fringe.push(blahNewNode, newCost+heuristic(addNode[0],problem))
    #     closedSet.append(currentState)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
