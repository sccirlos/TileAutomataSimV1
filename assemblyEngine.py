import random 

import UniversalClasses


import sys

class Engine:
    def __init__(self, currentSystem):
        self.system = currentSystem
        #self.assemblyList = []
        self.moveHistory = []
        self.TimeTaken = []
        self.currentIndex = 0
        self.lastIndex = 0



        # Get seed 
        print(self.system.returnSeedStates())

        seedState = random.choice(self.system.returnSeedStates())
        seed = UniversalClasses.Tile(seedState, 0, 0) 
        self.seedAssembly = UniversalClasses.Assembly()
        self.seedAssembly.set_tiles([seed])
        # Changed from adding to list to setting it as the current assembly
        #self.assemblyList.append(seedAssembly)
        self.currentAssembly = self.seedAssembly

        self.nextMoves = self.currentAssembly.getMoves(self.system)
        self.moveDict = {}

        for i in range(len(self.nextMoves)):
            move = self.nextMoves[i]
            x = move["x"]
            y = move["y"]

            if self.moveDict.get(UniversalClasses.toCoords(x , y)) == None: 
                self.moveDict[UniversalClasses.toCoords(x , y)] = []

            self.moveDict[UniversalClasses.toCoords(x , y)].append(move)
            

    def step(self):
        if(self.currentIndex < self.lastIndex): 
            move = self.moveHistory[self.currentIndex]
            self.currentAssembly = self.currentAssembly.performMove(move)

            self.currentIndex = self.currentIndex + 1
            return 0
        else:
            return self.build()
                
    def back(self):
        if(self.currentIndex > 0): 
            self.currentIndex = self.currentIndex - 1
            move = self.moveHistory[self.currentIndex]
            self.currentAssembly = self.currentAssembly.undoMove(move)

    def first(self):
        self.currentIndex = 0
        self.currentAssembly = self.seedAssembly

    def last(self):
        while self.currentIndex < self.lastIndex:
            # Will update current assembly, break if terminal
            if self.step() == -1: break

    def getCurrentAssembly(self):
        return self.currentAssembly

    def getCurrentIndex(self):
        return self.currentIndex

    def build(self):
        # Get current Assembly
        cAssembly = self.getCurrentAssembly()
        #moveList = cAssembly.getMoves(self.system)

        #print(moveList.length())
        # Check if assembly is terminal
        if(len(self.nextMoves) == 0): 
            print("Terminal")
            cAssembly.print_size()
            return -1
        else:
            print(len(self.nextMoves))

        self.TimeTaken.append(len(self.nextMoves))

        # Update lastIndex
        self.lastIndex = self.lastIndex + 1
        self.currentIndex = self.currentIndex + 1

        # Get next move and add to list
        move = random.choice(self.nextMoves)


        coords = UniversalClasses.toCoords(move["x"], move["y"])

        # Remove Old Moves from List
        oldMoves = self.moveDict.get(coords)

        if oldMoves != None:
            print("before: ", len(self.nextMoves))
            # We can delete the whole list
            # If a move we just performed was a attachment we can't attach anything else 
            # If it was a transition it will not be in the same state any longer. 
            # The list would not contain both (A transtion cannot take place with an empty space)
            for oMove in self.moveDict[coords]:
                #print("Removing Move: ", oMove["State1"], " at (", oMove["x"], " , ", oMove["y"])
                #print("oMove: ", oMove)
                self.nextMoves.remove(oMove)
            
            print("middle: ", len(self.nextMoves))
            del self.moveDict[coords]

        coordsN = UniversalClasses.toCoords(move["x"], move["y"] + 1)
        oldMovesN = self.moveDict.get(coordsN)

        # Remove any transtion rules that occur to the north
        if oldMovesN != None:
            if oldMoves[0]["type"] == "t":
                for oMove in self.moveDict[coordsN]:
                    self.nextMoves.remove(oMove)
                del self.moveDict[coordsN]
            

        coordsW = UniversalClasses.toCoords(move["x"] - 1, move["y"])
        oldMovesW = self.moveDict.get(coordsW)

        # Remove rules if they are transitions
        if oldMovesW != None:
            if oldMoves[0]["type"] == "t":
                for oMove in self.moveDict[coordsW]:
                    self.nextMoves.remove(oMove)
                del self.moveDict[coordsW]
            

        # Update assembly and get new moves
        self.currentAssembly = cAssembly.performMove(move)
        self.moveHistory.append(move)
        newMoves = self.currentAssembly.getMovesCoords(move["x"], move["y"], self.system)
        
        neighMoves = []

        if move["type"] == "t":
            if move["dir"] == "v":
                neighMoves = self.currentAssembly.getMovesCoords(move["x"], move["y"] - 1, self.system)
            if move["dir"] == "h":
                neighMoves = self.currentAssembly.getMovesCoords(move["x"] + 1, move["y"], self.system)

        if len(neighMoves) > 0:
            newMoves.extend(neighMoves)

        
        self.nextMoves.extend(newMoves)

        for nMove in newMoves:
            x = nMove["x"]
            y = nMove["y"]

            newCoords = UniversalClasses.toCoords(x, y)
            if self.moveDict.get(newCoords) == None: 
                self.moveDict[UniversalClasses.toCoords(x , y)] = []

            self.moveDict[UniversalClasses.toCoords(x , y)].append(nMove)

        print("after: ", len(self.nextMoves))

        for move in self.nextMoves:
            print("move: ", move)

        return 0

    def timeTaken(self):
        if len(self.TimeTaken) > 0:
            return 1 / self.TimeTaken[self.currentIndex - 1]
        else:
            return 0


    
