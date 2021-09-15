import random 

import UniversalClasses


import sys

class Engine:
    def __init__(self, currentSystem):
        self.system = currentSystem
        #self.assemblyList = []
        self.moveList = []
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

        self.validMoves = self.currentAssembly.getMoves()

    def step(self):
        if(self.currentIndex < self.lastIndex): 
            move = self.moveList[self.currentIndex]
            self.currentAssembly = self.currentAssembly.performMove(move)

            self.currentIndex = self.currentIndex + 1
            return 0
        else:
            return self.build()
                
    def back(self):
        if(self.currentIndex > 0): 
            self.currentIndex = self.currentIndex - 1
            move = self.moveList[self.currentIndex]
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
        if(len(self.validMoves) == 0): 
            print("Terminal")
            cAssembly.print_size()
            return -1

        self.TimeTaken.append(len(self.validMoves))

        # Update lastIndex
        self.lastIndex = self.lastIndex + 1
        self.currentIndex = self.currentIndex + 1

        # Get next assembly and add to list
        move = random.choice(self.validMoves)

        self.currentAssembly = cAssembly.performMove(move)
        self.moveList.append(move)



        moveX = move["x"]
        moveY = move["y"]

        # If Attachment 
        if move["type"] == "a":
            # Remove other moves for self
            attOldMoves = cAssembly.getAttat(self.system, moveX, moveY)
            self.removeMoves(attOldMoves)

            # Add Attachments for neighbors


            # Add transitions for self

            # Add "v" transitions for North Neighbor (New assembly)


            # Add "h" transitions for W Neighbor (New Assembly)

        elif move["type"] == "t":
            # remove other move for self
            trOldMoves = cAssembly.getTRat(self.system, moveX, moveY)
            self.removeMoves(trOldMoves)

            # remove "v" TR moves from N neighbor
            trOldMoves = cAssembly.getTRat(self.system, moveX, moveY + 1, "v")
            self.removeMoves(trOldMoves)

            # remove "h" TR moves from W Neighbor
            trOldMoves = cAssembly.getTRat(self.system, moveX, moveY + 1, "v")
            self.removeMoves(trOldMoves)

            # add new transitions rules for self
 








 
        return 0


    # It seems this function would be the new bottle neck - TG
    def removeMoves(self, oldMoves):
        if isinstance(oldMoves, None):
            oldMoves = [oldMoves]

        if not isinstance(oldMoves, list):
            oldMoves = [oldMoves]

        for oMove in oldMoves:
            self.validMoves.remove(oMove)
        




    def timeTaken(self):
        if len(self.TimeTaken) > 0:
            return 1 / self.TimeTaken[self.currentIndex - 1]
        else:
            return 0

    
