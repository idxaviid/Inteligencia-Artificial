# multiAgents.py
# --------------
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





from util import manhattanDistance
from game import Directions
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
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        # Hago una lista de la comida que queda
        foodList = newFood.asList()

        valor = 0
        distMin = 100

        # Compruebo la distancia del fantasma mas cercano
        distMin = min(manhattanDistance(newPos, fantasma.getPosition()) for fantasma in newGhostStates)

        # Si el fantasma estara a distancia 0 o 1, devuelvo el minimo valor
        if (distMin <= 1):
            valor = -1000
        # En caso contrario, devuelvo un valor que dependera de lo cerca que este la comida mas cercana
        else:
            if len(foodList) > 0:
                distancia = min(manhattanDistance(newPos, food) for food in foodList)
                valor = (10.0/distancia)

        # Para que no se quede quieto, por esta accion devolvere un valor pequenyo,
        # pero aun asi mayor que el de tener un fantasma al lado
        if action == "Stop":
            valor = -500

        # El valor a retornar sera la suma de la puntuacion de la partida + el valor calculado
        return successorGameState.getScore() + valor

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

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"

        # Hago la llamada inicial al algoritmo, mandandole:
        # estado actual, profundidad y la id de agente 0 (pacman)
        return self.minimax(gameState, self.depth, 0)[1]

    def minimax(self, estado, profundidad, agente):

        # Cuando el numero de agente iguale a la cantidad de agentes del juego,
        # querra decir que le vuelve a tocar al Pacman.
        # Por lo que volvera a ser el agente 0 y se decrementara la profundidad en 1
        if agente == estado.getNumAgents():
            agente = 0
            profundidad -= 1

        # Cogemos las acciones legales que tiene el estado
        acciones = estado.getLegalActions(agente)
        # Inicializo resultado, que sera la accion a realizar
        resultado = None

        # Si llega a profundidad 0 o no hay acciones disponibles para ese estado,
        # devuelve el valor de la funcion de evaluacion
        if profundidad == 0 or not acciones:
            return self.evaluationFunction(estado), None

        # Juega Pacman, maximizo
        if agente == 0:
            # Inicializo variable a -infinito
            a = -float("inf")
            # Compruebo para cada accion disponible
            for accion in acciones:
                # Genero el sucesor del estado con esa accion
                sucesor = estado.generateSuccessor(agente, accion)
                # Saco el valor maximo y la accion correspondiente a ese valor
                # llamando recursivamente a minimax con el siguiente agente
                nueva_a = max(a, self.minimax(sucesor, profundidad, agente+1)[0])
                if nueva_a > a:
                    a = nueva_a
                    resultado = accion
            # Devuelvo el valor y la accion del valor
            return a, resultado

        # Juegan fantasmas, minimizo
        else:
            # Inicializo variable a +infinito
            b = float("inf")
            # Compruebo para cada accion disponible
            for accion in acciones:
                # Genero el sucesor del estado con esa accion
                sucesor = estado.generateSuccessor(agente, accion)
                # Saco el valor minimo y la accion correspondiente a ese valor
                # llamando recursivamente a minimax con el siguiente agente
                nueva_b = min(b, self.minimax(sucesor, profundidad, agente+1)[0])
                if nueva_b < b:
                    b = nueva_b
                    resultado = accion
            # Devuelvo el valor y la accion del valor
            return b, resultado


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        # Hago la llamada inicial al algoritmo, mandandole:
        # estado actual, profundidad, la id de agente 0 (pacman),
        # la alfa inicial (-oo) y la beta inicial (+oo)
        return self.minimax_poda(gameState, self.depth, 0, -float("inf"), float("inf"))[1]

    def minimax_poda(self, estado, profundidad, agente, alfa, beta):

        # Cuando el numero de agente iguale a la cantidad de agentes del juego,
        # querra decir que le vuelve a tocar al Pacman.
        # Por lo que volvera a ser el agente 0 y se decrementara la profundidad en 1
        if agente == estado.getNumAgents():
            agente = 0
            profundidad -= 1

        # Cogemos las acciones legales que tiene el estado
        acciones = estado.getLegalActions(agente)
        # Inicializo resultado, que sera la accion a realizar
        resultado = None

        # Si llega a profundidad 0 o no hay acciones disponibles para ese estado,
        # devuelve el valor de la funcion de evaluacion
        if profundidad == 0 or not acciones:
            return self.evaluationFunction(estado), None

        # Juega Pacman, maximizo
        if agente == 0:
            # Inicializo variable a -infinito
            v = -float("inf")
            # Compruebo para cada accion disponible
            for accion in acciones:
                # Genero el sucesor del estado con esa accion
                sucesor = estado.generateSuccessor(agente, accion)
                # Saco el valor maximo y la accion correspondiente a ese valor
                # llamando recursivamente a minimax con el siguiente agente
                nueva_v = max(v, self.minimax_poda(sucesor, profundidad, agente+1, alfa, beta)[0])
                if nueva_v > v:
                    v = nueva_v
                    resultado = accion
                # Si el valor es mayor a beta, podo y devuelvo el valor
                if v > beta:
                    return v, resultado
                # Sino es mayor, guardo como alfa el maximo entre el valor y la alfa actual
                alfa = max(v, alfa)
            # Devuelvo el valor y la accion del valor
            return v, resultado

        # Juegan fantasmas, minimizo
        else:
            # Inicializo variable a +infinito
            v = float("inf")
            # Compruebo para cada accion disponible
            for accion in acciones:
                # Genero el sucesor del estado con esa accion
                sucesor = estado.generateSuccessor(agente, accion)
                # Saco el valor minimo y la accion correspondiente a ese valor
                # llamando recursivamente a minimax con el siguiente agente
                nueva_v = min(v, self.minimax_poda(sucesor, profundidad, agente+1, alfa, beta)[0])
                if nueva_v < v:
                    v = nueva_v
                    resultado = accion
                # Si el valor es menor a alfa, podo y devuelvo el valor
                if v < alfa:
                    return v, resultado
                # Sino es menor, guardo como beta el minimo entre el valor y la beta actual
                beta = min(v, beta)
            # Devuelvo el valor y la accion del valor
            return v, resultado


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

        # Hago la llamada inicial al algoritmo, mandandole:
        # estado actual, profundidad y la id de agente 0 (pacman)
        return self.expectimax(gameState, self.depth, 0)[1]

    def expectimax(self, estado, profundidad, agente):

        # Cuando el numero de agente iguale a la cantidad de agentes del juego,
        # querra decir que le vuelve a tocar al Pacman.
        # Por lo que volvera a ser el agente 0 y se decrementara la profundidad en 1
        if agente == estado.getNumAgents():
            agente = 0
            profundidad -= 1

        # Cogemos las acciones legales que tiene el estado
        acciones = estado.getLegalActions(agente)
        # Inicializo resultado, que sera la accion a realizar
        resultado = None

        # Si llega a profundidad 0 o no hay acciones disponibles para ese estado,
        # devuelve el valor de la funcion de evaluacion
        if profundidad == 0 or not acciones:
            return self.evaluationFunction(estado), None

        # Juega Pacman, maximizo
        if agente == 0:
            # Inicializo variable a -infinito
            a = -float("inf")
            # Compruebo para cada accion disponible
            for accion in acciones:
                # Genero el sucesor del estado con esa accion
                sucesor = estado.generateSuccessor(agente, accion)
                # Saco el valor maximo y la accion correspondiente a ese valor
                # llamando recursivamente a minimax con el siguiente agente
                nueva_a = max(a, self.expectimax(sucesor, profundidad, agente+1)[0])
                if nueva_a > a:
                    a = nueva_a
                    resultado = accion
            # Devuelvo el valor y la accion del valor
            return a, resultado

        # Juegan fantasmas
        else:
            # Inicializo variable a 0
            b = 0
            # Compruebo para cada accion disponible
            for accion in acciones:
                # Genero el sucesor del estado con esa accion
                sucesor = estado.generateSuccessor(agente, accion)
                # Calculo y devuelvo el valor medio de cada accion de ese sucesor
                # para devolver el valor medio de ese sucesor
                b +=  self.expectimax(sucesor, profundidad, agente+1)[0] / float(len(acciones))
            # Devuelvo el valor de ese sucesor
            return b, None


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: Utilizo el score del juego, la distancia a la comida mas cercana,
      la distancia media a la comida, la distancia al fantasma mas cercano
      y el tiempo asustado de los fantasmas para calcular el valor a devolver con
      un calculo que he obtenido a base de pruebas e ir afinando los valores a usar
    """
    "*** YOUR CODE HERE ***"

    pos = currentGameState.getPacmanPosition()
    food = currentGameState.getFood()
    foodList = food.asList()
    nFood = len(foodList)
    ghostStates = currentGameState.getGhostStates()
    score = currentGameState.getScore()

    # Inicializo la distancia a la comida mas cercana y la distancia media a la comida a 1
    cercanaC, mediaC = 1, 1
    # Si hay comida, calculo la distancia Manhattan para cada comida
    # Y saco la distancia a la comida mas cercana y la distancia media de la comida
    if nFood > 0:
        distanciasComida = [manhattanDistance(pos, comida) for comida in foodList]
        cercanaC = min(distanciasComida)
        mediaC = sum(distanciasComida)/nFood

    # Calculo la distancia Manhattan del fantasma mas cercano
    cercanoF = min(manhattanDistance(pos,fantasma.getPosition()) for fantasma in ghostStates)
    # Si esta mas cerca de 3, devuelvo -1
    if cercanoF < 3:
        return -1

    # Devuelvo el tiempo del estado asustado de los fantasmas
    scared = ghostStates[0].scaredTimer

    # El valor a devolver sera el resultado de un calculo en el que se usaran los valores
    # obtenidos anteriormente
    return score + 1.0/(cercanaC + mediaC) + 1.0/cercanoF + scared


class BoundedIntelligenceMaxAgent(MultiAgentSearchAgent):

    def getAction(self, gameState):
        return self.BoundedIntelligenceMax(gameState, self.depth, 0)[1]

    def BoundedIntelligenceMax(self, estado, profundidad, agente):

        if agente == estado.getNumAgents():
            agente = 0
            profundidad -= 1

        acciones = estado.getLegalActions(agente)
        resultado = None

        if profundidad == 0 or not acciones:
            return self.evaluationFunction(estado), None

        if agente == 0:
            a = -float("inf")
            for accion in acciones:
                sucesor = estado.generateSuccessor(agente, accion)
                nueva_a = max(a, self.BoundedIntelligenceMax(sucesor, profundidad, agente+1)[0])
                if nueva_a > a:
                    a = nueva_a
                    resultado = accion
            return a, resultado

        else:
            b = []
            for accion in acciones:
                sucesor = estado.generateSuccessor(agente, accion)
                b.append(self.BoundedIntelligenceMax(sucesor, profundidad, agente+1)[0])
            b.sort()
            i = 0
            x = 0
            for valor in b:
                x += (float(len(acciones)) - i) * valor
                i += 1
            return (2 * x) / (float(len(acciones)) * (float(len(acciones))+1)), None



# Abbreviation
better = betterEvaluationFunction

