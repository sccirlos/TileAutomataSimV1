# Fast Engine class
# David Caballero
# Sonya Cirlos
# Timothy Gomez

from PyQt5.QtCore import QRunnable, QThreadPool
from UniversalClasses import toCoords
from assemblyEngine import Engine, printMove
import UniversalClasses as uc

import random

class FastEngine(Engine):
    def fastLast(self):
        self.locks = {}
        # While available move list is empty and number of threads is 0
        print("In fast Engine")
        # Max threads is default to 8? I think tasks queue up if we have more
        print("Max Threads: ", QThreadPool.globalInstance().maxThreadCount())
        while len(self.validMoves) > 0 or QThreadPool.globalInstance().activeThreadCount() > 0:
            # grab random move from avaible moves
            try:
                move = random.choice(self.validMoves)
            except:
                # If the move list is empty the random choice may crash, this just makes it try again
                print("failed random choice")
            else:
                # get the move coords
                moveX = move["x"]
                moveY = move["y"]

                # Call the check locks function, if anything in the neighborhood is locked it goes back to top of loop
                if self.checkLocks(moveX, moveY):
                    
                    # Lock the neighborhood
                    self.locks[toCoords(moveX, moveY)] = 1
                    self.locks[toCoords(moveX + 1, moveY)] = 1
                    self.locks[toCoords(moveX, moveY + 1)] = 1
                    self.locks[toCoords(moveX - 1, moveY)] = 1
                    self.locks[toCoords(moveX, moveY - 1)] = 1
                    self.locks[toCoords(moveX + 1, moveY + 1)] = 1
                    self.locks[toCoords(moveX - 1, moveY + 1)] = 1
                    self.locks[toCoords(moveX + 1, moveY - 1)] = 1
                    self.locks[toCoords(moveX - 1, moveY - 1)] = 1
                    self.locks[toCoords(moveX + 2, moveY)] = 1
                    self.locks[toCoords(moveX, moveY - 2)] = 1

                    ## Taken from build in the engine
                    ## Removes all the moves in the neighborhood. This takes work from the worker threads so they run quicker.
                    ## Removing the moves here in the main thread also takes away the possibility that a worker thread will remove a move we had just chosen.
                    
                    # If Attachment
                    if move["type"] == "a":
                        # Remove other moves for self
                        attOldMoves = self.currentAssembly.getAttat(
                            self.system, moveX, moveY)
                        self.removeMoves(attOldMoves)

                        # remove Attachments for neighbors
                        nAtts = self.currentAssembly.getAttat(
                            self.system, moveX, moveY + 1)
                        self.removeMoves(nAtts)

                        sAtts = self.currentAssembly.getAttat(
                            self.system, moveX, moveY - 1)
                        self.removeMoves(sAtts)

                        wAtts = self.currentAssembly.getAttat(
                            self.system, moveX - 1, moveY)
                        self.removeMoves(wAtts)

                        eAtts = self.currentAssembly.getAttat(
                            self.system, moveX + 1, moveY)
                        self.removeMoves(eAtts)

                    elif move["type"] == "t":
                        # Removing Moves
                        # remove other move for self
                        trOldMoves = self.currentAssembly.getTRat(
                            self.system, moveX, moveY)
                        self.removeMoves(trOldMoves)

                        # remove "v" TR moves from N neighbor
                        vOldMoves = self.currentAssembly.getTRat(
                            self.system, moveX, moveY + 1, "v")
                        self.removeMoves(vOldMoves)

                        # remove "h" TR moves from W Neighbor
                        hOldMoves = self.currentAssembly.getTRat(
                            self.system, moveX - 1, moveY, "h")
                        self.removeMoves(hOldMoves)

                        # remove attachment rules from neighbors
                        nAtts = self.currentAssembly.getAttat(
                            self.system, moveX, moveY + 1)
                        self.removeMoves(nAtts)

                        sAtts = self.currentAssembly.getAttat(
                            self.system, moveX, moveY - 1)
                        self.removeMoves(sAtts)

                        wAtts = self.currentAssembly.getAttat(
                            self.system, moveX - 1, moveY)
                        self.removeMoves(wAtts)

                        eAtts = self.currentAssembly.getAttat(
                            self.system, moveX + 1, moveY)
                        self.removeMoves(eAtts)

                        # Update tile 2
                        # If V rule
                        if move["dir"] == "v":
                            # Removing moves
                            # remove TR from self
                            vOldMoves = self.currentAssembly.getTRat(
                                self.system, moveX, moveY - 1)
                            self.removeMoves(vOldMoves)

                            # Remove "h" rules for SW
                            swMoves = self.currentAssembly.getTRat(
                                self.system, moveX - 1, moveY - 1, "h")
                            self.removeMoves(swMoves)

                            # Remove attachments from neighbors
                            s2Atts = self.currentAssembly.getAttat(
                                self.system, moveX, moveY - 2)
                            self.removeMoves(s2Atts)

                            swAtts = self.currentAssembly.getAttat(
                                self.system, moveX - 1, moveY - 1)
                            self.removeMoves(swAtts)

                            seAtts = self.currentAssembly.getAttat(
                                self.system, moveX + 1, moveY - 1)
                            self.removeMoves(seAtts)

                        # If H rule
                        if move["dir"] == "h":
                            # remove TR from self
                            vOldMoves = self.currentAssembly.getTRat(
                                self.system, moveX + 1, moveY)
                            self.removeMoves(vOldMoves)

                            # Remove "v" rules for NE
                            neMoves = self.currentAssembly.getTRat(
                                self.system, moveX + 1, moveY + 1, "v")
                            self.removeMoves(neMoves)

                            # remove attachments from neighbors
                            e2Atts = self.currentAssembly.getAttat(
                                self.system, moveX + 2, moveY)
                            self.removeMoves(e2Atts)

                            neAtts = self.currentAssembly.getAttat(
                                self.system, moveX + 1, moveY + 1)
                            self.removeMoves(neAtts)

                            seAtts = self.currentAssembly.getAttat(
                                self.system, moveX + 1, moveY - 1)
                            self.removeMoves(seAtts)

                    self.currentAssembly.performMove(move)
                    self.moveList.append(move)

                    # Give move and to worker from thread pool 
                    worker = MoveWorker()
                    worker.give(move, self)
                    # Gives the threadpool our worker class so it can run it's function
                    QThreadPool.globalInstance().start(worker)
                #else:
                    #print("locked")
        print("Done with Fast Engine")
                

    def checkLocks(self, moveX, moveY):
        if self.locks.get(toCoords(moveX, moveY)) == 1:
            return False
        if self.locks.get(toCoords(moveX + 1, moveY)) == 1:
            return False
        if self.locks.get(toCoords(moveX, moveY + 1)) == 1:
            return False
        if self.locks.get(toCoords(moveX - 1, moveY)) == 1:
            return False
        if self.locks.get(toCoords(moveX, moveY - 1)) == 1:
            return False
        if self.locks.get(toCoords(moveX + 1, moveY + 1)) == 1:
            return False
        if self.locks.get(toCoords(moveX - 1, moveY + 1)) == 1:
            return False
        if self.locks.get(toCoords(moveX + 1, moveY - 1)) == 1:
            return False
        if self.locks.get(toCoords(moveX - 1, moveY - 1)) == 1:
            return False
        if self.locks.get(toCoords(moveX + 2, moveY)) == 1:
            return False
        if self.locks.get(toCoords(moveX, moveY - 2)) == 1:
            return False
        
        return True

    def fastAddNewMoves(self, move):
        moveX = move["x"]
        moveY = move["y"]

        # Taken from build in engine, adding moves, this function is called in the worker thread

        # If Attachment
        if move["type"] == "a":

            # Add Attachments for neighbors
            nAtts = self.currentAssembly.getAttat(
                self.system, moveX, moveY + 1)
            self.addMoves(nAtts)

            sAtts = self.currentAssembly.getAttat(
                self.system, moveX, moveY - 1)
            self.addMoves(sAtts)

            wAtts = self.currentAssembly.getAttat(
                self.system, moveX - 1, moveY)
            self.addMoves(wAtts)

            eAtts = self.currentAssembly.getAttat(
                self.system, moveX + 1, moveY)
            self.addMoves(eAtts)

            # Add transitions for self
            newTR = self.currentAssembly.getTRat(self.system, moveX, moveY)
            self.addMoves(newTR)

            # Add "v" transitions for North Neighbor (New assembly)
            vTR = self.currentAssembly.getTRat(
                self.system, moveX, moveY + 1, "v")
            self.addMoves(vTR)

            # Add "h" transitions for W Neighbor (New Assembly)
            hTR = self.currentAssembly.getTRat(
                self.system, moveX - 1, moveY, "h")
            self.addMoves(hTR)

        elif move["type"] == "t":

            # Adding Moves
            # add new transitions rules for self
            newTR = self.currentAssembly.getTRat(self.system, moveX, moveY)
            self.addMoves(newTR)

            # Add "v" transitions for North Neighbor (New assembly)
            vTR = self.currentAssembly.getTRat(
                self.system, moveX, moveY + 1, "v")
            self.addMoves(vTR)

            # Add "h" transitions for W Neighbor (New Assembly)
            hTR = self.currentAssembly.getTRat(
                self.system, moveX - 1, moveY, "h")
            self.addMoves(hTR)

            # remove attachment rules from neighbors
            nAtts = self.currentAssembly.getAttat(
                self.system, moveX, moveY + 1)
            self.addMoves(nAtts)

            sAtts = self.currentAssembly.getAttat(
                self.system, moveX, moveY - 1)
            self.addMoves(sAtts)

            wAtts = self.currentAssembly.getAttat(
                self.system, moveX - 1, moveY)
            self.addMoves(wAtts)

            eAtts = self.currentAssembly.getAttat(
                self.system, moveX + 1, moveY)
            self.addMoves(eAtts)

            # Update tile 2
            # If V rule
            if move["dir"] == "v":

                # Adding Moves
                # Add TR to self
                vNewMoves = self.currentAssembly.getTRat(
                    self.system, moveX, moveY - 1)
                self.addMoves(vNewMoves)

                # Add "h" rules for SW
                swNewMoves = self.currentAssembly.getTRat(
                    self.system, moveX - 1, moveY - 1, "h")
                self.addMoves(swNewMoves)

                # Add attachments from neighbors
                s2Atts = self.currentAssembly.getAttat(
                    self.system, moveX, moveY - 2)
                self.addMoves(s2Atts)

                swAtts = self.currentAssembly.getAttat(
                    self.system, moveX - 1, moveY - 1)
                self.addMoves(swAtts)

                seAtts = self.currentAssembly.getAttat(
                    self.system, moveX + 1, moveY - 1)
                self.addMoves(seAtts)

            # If H rule
            if move["dir"] == "h":

                # add TR from self
                vNewMoves = self.currentAssembly.getTRat(
                    self.system, moveX + 1, moveY)
                self.addMoves(vNewMoves)

                # add "v" rules for ne
                neMoves = self.currentAssembly.getTRat(
                    self.system, moveX + 1, moveY + 1, "v")
                self.addMoves(neMoves)

                # add attachments from neighbors
                e2Atts = self.currentAssembly.getAttat(
                    self.system, moveX + 2, moveY)
                self.addMoves(e2Atts)

                neAtts = self.currentAssembly.getAttat(
                    self.system, moveX + 1, moveY + 1)
                self.addMoves(neAtts)

                seAtts = self.currentAssembly.getAttat(
                    self.system, moveX + 1, moveY - 1)
                self.addMoves(seAtts)

    

class MoveWorker(QRunnable):
    def give(self, move, engine):
        self.move = move
        self.engine = engine

    def run(self):
        # this function is the majority of the work done by this thread
        self.engine.fastAddNewMoves(self.move)

        moveX = self.move["x"]
        moveY = self.move["y"]

        # Unlock locks 
        self.engine.locks[toCoords(moveX, moveY)] = 0
        self.engine.locks[toCoords(moveX + 1, moveY)] = 0
        self.engine.locks[toCoords(moveX, moveY + 1)] = 0
        self.engine.locks[toCoords(moveX - 1, moveY)] = 0
        self.engine.locks[toCoords(moveX, moveY - 1)] = 0
        self.engine.locks[toCoords(moveX + 1, moveY + 1)] = 0
        self.engine.locks[toCoords(moveX - 1, moveY + 1)] = 0
        self.engine.locks[toCoords(moveX + 1, moveY - 1)] = 0
        self.engine.locks[toCoords(moveX - 1, moveY - 1)] = 0
        self.engine.locks[toCoords(moveX + 2, moveY)] = 0
        self.engine.locks[toCoords(moveX, moveY - 2)] = 0


def paraSquareGen(value):
    seed = uc.State("X0", "DFE0E2")

    sys = uc.System(1, [], [], [seed])

    for i in range(1, value):
        xState = uc.State("X" + str(i), "DFE0E2")
        yState = uc.State("Y" + str(i), "DFE0E2")
        sys.add_State(xState)
        sys.add_State(yState)

        sys.add_Initial_State(xState)
        sys.add_Initial_State(yState)

        xAff = uc.AffinityRule("X" + str(i - 1), "X" + str(i), "h", 1)
        sys.add_affinity(xAff)
        if i > 1:
            yAff = uc.AffinityRule("Y" + str(i), "Y" + str(i -1), "v", 1)
            sys.add_affinity(yAff)

    for i in range(value):
        iAff = uc.AffinityRule("Y1", "X" + str(i), "v", 1)
        sys.add_affinity(iAff)
    
    return sys