import random 

import UniversalClasses


import sys


### Debugging Functions
def printMove(move):
    if move["type"] == "a":
        print("Attach: ", move["state1"].get_label(), " at ", move["x"], ", ", move["y"])
    if move["type"] == "t":
        print("Transition ", move["state1"].get_label(), ", ", move["state2"].get_label(), " to ", move["state1Final"].get_label(), ", ", move["state2Final"].get_label())
        print(" at ", move["x"], ", ", move["y"])



########
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

        self.validMoves = self.currentAssembly.getMoves(self.system)

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

    def getCurrentMove(self):
        if len(self.moveList) > 0:
            return self.moveList[self.currentIndex]

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

        #print("Next Move: ")
        #printMove(move)


        moveX = move["x"]
        moveY = move["y"]

        # If Attachment 
        if move["type"] == "a":
            # Remove other moves for self
            attOldMoves = cAssembly.getAttat(self.system, moveX, moveY)
            self.removeMoves(attOldMoves)

            # remove Attachments for neighbors
            nAtts = cAssembly.getAttat(self.system, moveX, moveY + 1)
            self.removeMoves(nAtts)

            sAtts = cAssembly.getAttat(self.system, moveX, moveY - 1)
            self.removeMoves(sAtts)

            wAtts = cAssembly.getAttat(self.system, moveX - 1, moveY)
            self.removeMoves(wAtts)

            eAtts = cAssembly.getAttat(self.system, moveX + 1, moveY)
            self.removeMoves(eAtts)

            # Add Attachments for neighbors
            nAtts = self.currentAssembly.getAttat(self.system, moveX, moveY + 1)
            self.addMoves(nAtts)

            sAtts = self.currentAssembly.getAttat(self.system, moveX, moveY - 1)
            self.addMoves(sAtts)

            wAtts = self.currentAssembly.getAttat(self.system, moveX - 1, moveY)
            self.addMoves(wAtts)

            eAtts = self.currentAssembly.getAttat(self.system, moveX + 1, moveY)
            self.addMoves(eAtts)
            

            # Add transitions for self
            newTR = self.currentAssembly.getTRat(self.system, moveX, moveY)
            self.addMoves(newTR)

            # Add "v" transitions for North Neighbor (New assembly)
            vTR = self.currentAssembly.getTRat(self.system, moveX, moveY + 1, "v")
            self.addMoves(vTR)

            # Add "h" transitions for W Neighbor (New Assembly)
            hTR = self.currentAssembly.getTRat(self.system, moveX - 1, moveY, "h")
            self.addMoves(hTR)



        elif move["type"] == "t":
            ### Removing Moves
            # remove other move for self
            trOldMoves = cAssembly.getTRat(self.system, moveX, moveY)
            self.removeMoves(trOldMoves)

            # remove "v" TR moves from N neighbor
            vOldMoves = cAssembly.getTRat(self.system, moveX, moveY + 1, "v")
            self.removeMoves(vOldMoves)

            # remove "h" TR moves from W Neighbor
            hOldMoves = cAssembly.getTRat(self.system, moveX - 1, moveY, "h")
            self.removeMoves(hOldMoves)

            # remove attachment rules from neighbors
            nAtts = cAssembly.getAttat(self.system, moveX, moveY + 1)
            self.removeMoves(nAtts)

            sAtts = cAssembly.getAttat(self.system, moveX, moveY - 1)
            self.removeMoves(sAtts)

            wAtts = cAssembly.getAttat(self.system, moveX - 1, moveY)
            self.removeMoves(wAtts)

            eAtts = cAssembly.getAttat(self.system, moveX + 1, moveY)
            self.removeMoves(eAtts)

            ###### Adding Moves
            # add new transitions rules for self
            newTR = self.currentAssembly.getTRat(self.system, moveX, moveY)
            self.addMoves(newTR)

            # Add "v" transitions for North Neighbor (New assembly)
            vTR = self.currentAssembly.getTRat(self.system, moveX, moveY + 1, "v")
            self.addMoves(vTR)

            # Add "h" transitions for W Neighbor (New Assembly)
            hTR = self.currentAssembly.getTRat(self.system, moveX - 1, moveY, "h")
            self.addMoves(hTR)

            # remove attachment rules from neighbors
            nAtts = self.currentAssembly.getAttat(self.system, moveX, moveY + 1)
            self.addMoves(nAtts)

            sAtts = self.currentAssembly.getAttat(self.system, moveX, moveY - 1)
            self.addMoves(sAtts)

            wAtts = self.currentAssembly.getAttat(self.system, moveX - 1, moveY)
            self.addMoves(wAtts)

            eAtts = self.currentAssembly.getAttat(self.system, moveX + 1, moveY)
            self.addMoves(eAtts)


            # Update tile 2
            # If V rule
            if move["dir"] == "v":
                #### Removing moves
                # remove TR from self
                vOldMoves = cAssembly.getTRat(self.system, moveX, moveY - 1)
                self.removeMoves(vOldMoves)


                # Remove "h" rules for SW
                swMoves = cAssembly.getTRat(self.system, moveX - 1, moveY - 1, "h")
                self.removeMoves(swMoves)
            
                # Remove attachments from neighbors
                s2Atts = cAssembly.getAttat(self.system, moveX, moveY - 2)
                self.removeMoves(s2Atts)

                swAtts = cAssembly.getAttat(self.system, moveX - 1, moveY - 1)
                self.removeMoves(swAtts)

                seAtts = cAssembly.getAttat(self.system, moveX + 1, moveY - 1)
                self.removeMoves(seAtts)

                ### Adding Moves
                # Add TR to self
                vNewMoves = self.currentAssembly.getTRat(self.system, moveX, moveY - 1)
                self.addMoves(vNewMoves)


                # Add "h" rules for SW
                swNewMoves = self.currentAssembly.getTRat(self.system, moveX - 1, moveY - 1, "h")
                self.addMoves(swNewMoves)
            
                # Add attachments from neighbors
                s2Atts = self.currentAssembly.getAttat(self.system, moveX, moveY - 2)
                self.addMoves(s2Atts)

                swAtts = self.currentAssembly.getAttat(self.system, moveX - 1, moveY - 1)
                self.addMoves(swAtts)

                seAtts = self.currentAssembly.getAttat(self.system, moveX + 1, moveY - 1)
                self.addMoves(seAtts)

                

            # If H rule
            if move["dir"] == "h":
                # remove TR from self
                vOldMoves = cAssembly.getTRat(self.system, moveX + 1, moveY)
                self.removeMoves(vOldMoves)

                # Remove "v" rules for NE
                neMoves = cAssembly.getTRat(self.system, moveX + 1, moveY + 1, "v")
                self.removeMoves(neMoves)
            
                # remove attachments from neighbors
                e2Atts = cAssembly.getAttat(self.system, moveX + 2, moveY)
                self.removeMoves(e2Atts)

                neAtts = cAssembly.getAttat(self.system, moveX + 1, moveY + 1)
                self.removeMoves(neAtts)

                seAtts = cAssembly.getAttat(self.system, moveX + 1, moveY - 1)
                self.removeMoves(seAtts)


                # add TR from self
                vNewMoves = self.currentAssembly.getTRat(self.system, moveX + 1, moveY)
                self.addMoves(vNewMoves)

                # add "v" rules for ne
                neMoves = self.currentAssembly.getTRat(self.system, moveX + 1, moveY + 1, "v")
                self.addMoves(neMoves)
            
                # add attachments from neighbors
                e2Atts = self.currentAssembly.getAttat(self.system, moveX + 2, moveY)
                self.addMoves(e2Atts)

                neAtts = self.currentAssembly.getAttat(self.system, moveX + 1, moveY + 1)
                self.addMoves(neAtts)

                seAtts = self.currentAssembly.getAttat(self.system, moveX + 1, moveY - 1)
                self.addMoves(seAtts)
 
        return 0


    # It seems this function would be the new bottle neck - TG
    def removeMoves(self, oldMoves):
        if oldMoves == None:
            return

        if not isinstance(oldMoves, list):
            oldMoves = [oldMoves]

        #print("Removing",  len(oldMoves), "moves")
        for oMove in oldMoves:
            #printMove(oMove)
            self.validMoves.remove(oMove)
        
    def addMoves(self, newMoves):
        if newMoves == None:
            return

        if not isinstance(newMoves, list):
            newMoves = [newMoves]

        #print("Adding",  len(newMoves), "moves")
        for nMove in newMoves:
            #printMove(nMove)
            self.validMoves.append(nMove)



    def timeTaken(self):
        if len(self.TimeTaken) > 0:
            return 1 / self.TimeTaken[self.currentIndex - 1]
        else:
            return 0

    
