from random import randrange

from UniversalClasses import System
import TAMainWindow
import LoadFile
import SaveFile
import Assembler_Proto

import sys

# Global Variables
currentSystem = None

class Engine:
    def __init__(self):
        self.system = currentSystem
        self.assemblyList = []
        self.currentIndex = 0
        self.lastIndex = 0

        # Get seed 

    def step(self):
        if(self.currentIndex < self.lastIndex): 
            self.currentSystem = self.currentSystem + 1
        else:
            if(self.build() != -1):
                self.currentSystem = self.currentSystem + 1

    def back(self):
        if(self.currentIndex > 0): self.currentSystem = self.currentSystem - 1

    def getCurrAssembly(self):
        return self.assemblyList[self.currentIndex]

    def build(self):
        # Check if assembly is terminal

        # Update lastIndex

        # Get next assembly and add to list

        return

    
