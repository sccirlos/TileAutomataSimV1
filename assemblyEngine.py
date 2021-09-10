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

        # Get next move 
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



        # Remove any transtion rules that occur to the north

        ## Get the coordinates of the northern Neighbors
        coordsN = UniversalClasses.toCoords(move["x"], move["y"] + 1)
        ## Get any moves that can take place to the north
        oldMovesN = self.moveDict.get(coordsN)
        ## If any exists exist
        if oldMovesN != None:
            ## Check if the moves are transitions
            if oldMovesN[0]["type"] == "t":
                ## For each oMove (old move) remove it from the move list
                for oMove in self.moveDict[coordsN]:
                    self.nextMoves.remove(oMove)
                ## Delete the whole dictionary entry
                del self.moveDict[coordsN]
            



        # Remove W rules if they are transitions
        coordsW = UniversalClasses.toCoords(move["x"] - 1, move["y"])
        oldMovesW = self.moveDict.get(coordsW)

        if oldMovesW != None:
            if oldMovesW[0]["type"] == "t":
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

        


        self.addMoveToLists(newMoves)

        #for nMove in newMoves:
            #x = nMove["x"]
            #y = nMove["y"]

            #newCoords = UniversalClasses.toCoords(x, y)
            #if self.moveDict.get(newCoords) == None: 
            #    self.moveDict[UniversalClasses.toCoords(x , y)] = []

            #self.moveDict[UniversalClasses.toCoords(x , y)].append(nMove)

        print("after: ", len(self.nextMoves))

        for move in self.nextMoves:
            UniversalClasses.printMove(move)

        return 0

    def addMoveToLists(self, moves):
        # If passed a single move make it into a list
        if not isinstance(moves, list):
            moves = [moves]

        for cMove in moves:
            # get the current dictionary for the location 
            x = cMove["x"]
            y = cMove["y"]
            coords = UniversalClasses.toCoords(x, y)
            movesXY = self.moveDict.get(coords)

            if movesXY == None:
                self.moveDict[coords] = [cMove]
                self.nextMoves.append(cMove)
            # we need to check if cMove is already in the list
            elif cMove["type"] == "a":
                # start by assuming the rule isn't already in the list
                uniqueFlag = 1
                # If the move is an attachment add it to the list if it is not already there
                for m in movesXY:
                    # If both 
                    #print("Comparing moves in dictionary")
                    if cMove["state1"].get_label() == m["state1"].get_label():
                        #print("Found a match")
                        uniqueFlag = 0

                if uniqueFlag == 1:
                    self.moveDict.get(coords).append(cMove)
                    self.nextMoves.append(cMove)
            elif cMove["type"] == "t":
                # We cannot accidently add repeat rules for transitions
                self.moveDict.get(coords).append(cMove)
                self.nextMoves.append(cMove)




            


    def timeTaken(self):
        if len(self.TimeTaken) > 0:
            return 1 / self.TimeTaken[self.currentIndex - 1]
        else:
            return 0


    
