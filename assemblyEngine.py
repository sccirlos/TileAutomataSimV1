import random 

import UniversalClasses


import sys

class Engine:
    def __init__(self, currentSystem):
        self.system = currentSystem
        self.assemblyList = []
        self.currentIndex = 0
        self.lastIndex = 0

        # Get seed 
        print(self.system.returnSeedStates())

        seedState = random.choice(self.system.returnSeedStates())
        seed = UniversalClasses.Tile(seedState, 0, 0) 
        seedAssembly = UniversalClasses.Assembly()
        seedAssembly.set_tiles([seed])
        self.assemblyList.append(seedAssembly)

    def step(self):
        if(self.currentIndex < self.lastIndex): 
            self.currentIndex = self.currentIndex + 1
            return 0
        else:
            return self.build()
                

    def back(self):
        if(self.currentIndex > 0): self.currentIndex = self.currentIndex - 1

    def getCurrentAssembly(self):
        return self.assemblyList[self.currentIndex]

    def getCurrentIndex(self):
        return self.currentIndex

    def build(self):
        # Get current Assembly
        cAssembly = self.getCurrentAssembly()
        moveList = cAssembly.getMoves(self.system)

        #print(moveList.length())
        # Check if assembly is terminal
        if(moveList.length() == 0): return -1


        # Update lastIndex
        self.lastIndex = self.lastIndex + 1
        self.currentIndex = self.currentIndex + 1

        # Get next assembly and add to list
        move = random.choice(moveList)
        newAssembly = cAssembly.performMove(move)
        self.assemblyList.append(newAssembly)
        return 0

    
