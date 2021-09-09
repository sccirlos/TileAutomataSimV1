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
        moveList = cAssembly.getMoves(self.system)

        #print(moveList.length())
        # Check if assembly is terminal
        if(len(moveList) == 0): 
            print("Terminal")
            cAssembly.print_size()
            return -1

        self.TimeTaken.append(len(moveList))

        # Update lastIndex
        self.lastIndex = self.lastIndex + 1
        self.currentIndex = self.currentIndex + 1

        # Get next assembly and add to list
        move = random.choice(moveList)
        self.currentAssembly = cAssembly.performMove(move)
        self.moveList.append(move)
        return 0

    def timeTaken(self):
        if len(self.TimeTaken) > 0:
            return 1 / self.TimeTaken[self.currentIndex - 1]
        else:
            return 0

    
