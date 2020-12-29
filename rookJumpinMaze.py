'''
    Author: Cameron Peeters
    Program: Rook Jumping Maze

    Abstract: 
        Creates a random nXn maze and finds the goal states using 
        an implementation of hill climbing algorithm.

    Algorithms:
        DFS, BFS, hillClimbDescent, and simulatedAnnealing.
'''

import random, time;
random.seed(random.random() % time.time())

class RJM:
    def __init__(self, n, i=0):
        self._iterations = i
        self._size = self.setSize(n)
        self._startPosition = (0, 0)
        self._goalPosition = (self._size - 1, self._size - 1)
        self._currentPosition = self._startPosition
        self._rjm = [[random.randint(1,self._size-1) for i in range(self._size)] for j in range(self._size)]
        self._states = [[' ' for i in range(self._size)] for j in range(self._size)]
        self._startState = "B0"
        self._goalState = "F4"
        self._moves = [["--" for i in range(self._size)] for j in range(self._size)]
        self._pathNum = 1000000
        self.initStates()

    def setSize(self, n):
        maxSize, minSize = 10, 5
        if n > maxSize:
            n = maxSize
            print("Size set to Max 'n' of 10")
        elif n < minSize:
            n = minSize
            print("Size set to Min 'n' of 5")
        return n

    def initStates(self, rjm=None):
        if rjm == None:
            rjm = self._rjm.copy()

        rjm[self._goalPosition[0]][self._goalPosition[1]] = 0
        key = 'A'
        for r in range(self._size):
            key = chr(ord(key)+1)
            for c in range(self._size):
                a = key + str(c)
                self._states[r][c]= a


    def getNeighbors(self, rjm= None):
        if rjm ==None:
            rjm = self._rjm.copy()

        def add(adj_list, a, b):
            adj_list.setdefault(a, []).append(b)

        adj_list = {}

        for r in range(self._size):
            for c in range(self._size):
    
                currentState = self._states[r][c]
                self._currentPosition = (r,c)
                    
                key = self._states[r][c]
                moveWeight = rjm[r][c]

                rightMoves = self._size - c - 1
                leftMoves = self._size - rightMoves - 1
                downMoves = self._size - r - 1
                upMoves = self._size - downMoves - 1 
                 
                #right move
                if moveWeight <= rightMoves and rightMoves > 0:
                    neighbour = self._states[r][c + moveWeight]
                    add(adj_list, key, neighbour)

                #left move
                if moveWeight <= leftMoves and leftMoves > 0:
                    neighbour = self._states[r][c - moveWeight]
                    add(adj_list, key, neighbour)

                #down move
                if moveWeight <= downMoves and downMoves > 0:
                    neighbour = self._states[r + moveWeight][c]
                    add(adj_list, key, neighbour)

                #right move
                if moveWeight <= upMoves and upMoves > 0:
                    neighbour = self._states[moveWeight-r][c]
                    add(adj_list, key, neighbour)

        return adj_list

    def evaluateRJM(self, graph):
        visited = set()

        def dfs_Recursive(visited, graph, node=self._startState, depth=0):
            if node not in visited and node in graph.keys():
                i = [(index, row.index(node)) for index, row in enumerate(self._states) if node in row]
                r = i[0]
                self._moves[r[0]][r[1]] = depth
                visited.add(node)
                for neighbour in graph[node]:
                    dfs_Recursive(visited, graph, neighbour, depth+1) 

        dfs_Recursive(visited, graph)
            
    def findPathBFS(self, graph):
        start, goal = self._startState, self._goalState
          
        explored = []
        queue = [[start]]

        if start == goal:
            return 

        while queue:
            path = queue.pop(0)
            node = path[-1]
            
            if node not in explored and node in graph.keys():
                neighbours = graph[node]
                
                for neighbour in neighbours:
                    new_path = list(path)
                    new_path.append(neighbour)
                    queue.append(new_path)
                    
                    if neighbour == goal:
                        return new_path
                explored.append(node)

        return explored

    def hillDescent(self, rjm=None):
        if rjm == None:
            rjm = self._rjm.copy()

        bestRJM = self
        
        for i in range(self._iterations):
            iRJM = RJM(self._size)
            graph = self.buildAdjacencyList()
            self.evaluateRJM(graph)
            (goalPos) = self._goalPosition
            if (self._moves[goalPos[0]][goalPos[1]] != '--'):
                self._pathNum = -self._moves[goalPos[0]][goalPos[1]]
                if bestRJM._pathNum < iRJM._pathNum:
                    bestRJM._rjm = iRJM._rjm.copy()

        bestRJM.printRJM(bestRJM._rjm)
        bestRJM.printMovesFromStart(bestRJM)

    def hillDescentRandomRestarts(self, descents, rjm=None):
        if rjm == None:
            rjm = self._rjm.copy()

        bestRJM = self
        
        for i in range(self._iterations):
            
            if i > descents:
                i = 0
                
            iRJM = RJM(self._size)
            graph = self.buildAdjacencyList()
            self.evaluateRJM(graph)
            (goalPos) = self._goalPosition
            
            if (self._moves[goalPos[0]][goalPos[1]] != '--'):
                self._pathNum = -self._moves[goalPos[0]][goalPos[1]]
                if bestRJM._pathNum < iRJM._pathNum:
                    bestRJM._rjm = iRJM._rjm.copy()

        bestRJM.printRJM(bestRJM._rjm)
        bestRJM.printMovesFromStart(bestRJM)

    def hillDescentRandomUphill(self, uphill, rjm=None):
        if rjm == None:
            rjm = self._rjm.copy()

        bestRJM = self
        prob = (1 - uphill)*100
        randNum = random.randint(1,100)
        
        for i in range(self._iterations):
            
            iRJM = RJM(self._size)
            graph = self.buildAdjacencyList()
            self.evaluateRJM(graph)
            (goalPos) = self._goalPosition
            if (self._moves[goalPos[0]][goalPos[1]] != '--'):
                self._pathNum = -self._moves[goalPos[0]][goalPos[1]]
                if bestRJM._pathNum < iRJM._pathNum or (randNum < prob):
                    bestRJM._rjm = iRJM._rjm.copy()

        bestRJM.printRJM(bestRJM._rjm)
        bestRJM.printMovesFromStart(bestRJM)

    def simulatedAnnealing(self, initTemp, decayRate, rjm=None):
        if rjm == None:
            rjm = self._rjm.copy()

        bestRJM = self
        prob = 1-decayRate/initTemp
        randNum = random.randint(1,100)
        
        for i in range(self._iterations):
            
            iRJM = RJM(self._size)
            graph = self.buildAdjacencyList()
            self.evaluateRJM(graph)
            (goalPos) = self._goalPosition
            if (self._moves[goalPos[0]][goalPos[1]] != '--'):
                self._pathNum = -self._moves[goalPos[0]][goalPos[1]]
                if bestRJM._pathNum < iRJM._pathNum or (randNum < prob):
                    bestRJM._rjm = iRJM._rjm.copy()

        bestRJM.printRJM(bestRJM._rjm)
        bestRJM.printMovesFromStart(bestRJM)

    def buildAdjacencyList(self):
        self._currentPosition = (0,0)        
        adjacencyList = self.getNeighbors()
        return adjacencyList

    def printMovesFromStart(self, rjm=None):
        if rjm == None:
            rjm = self._rjm.copy()
        print("Moves from start:")
        graph = self.buildAdjacencyList()
        self.evaluateRJM(graph)
        print("\n".join(" ".join(str(elem) for elem in row) for row in self._moves))
        (goalPos) = self._goalPosition
        
        if (self._moves[goalPos[0]][goalPos[1]] != '--'):
            self._pathNum = -self._moves[goalPos[0]][goalPos[1]]
        
        print(self._pathNum)

    def printRJM(self, rjm=None):
        if rjm == None:
            rjm = self.rjm.copy()
        print("\n".join(" ".join(str(elem) for elem in row) for row in rjm))


def main():
    i = int(input("iterations? "))
    iTemp = int(input("Initial temperature? "))
    decayRate = float(input("Decay rate? "))
    rookJumpingMaze = RJM(5, i)
    rookJumpingMaze.simulatedAnnealing(iTemp, decayRate)

if __name__ == "__main__":
    main()