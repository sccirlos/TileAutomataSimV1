# Fast Engine class
# David Caballero
# Sonya Cirlos
# Timothy Gomez

from PyQt5.QtCore import QRunnable, QThreadPool
from UniversalClasses import toCoords
from assemblyEngine import Engine

import random

class FastEngine(Engine):
    def fastLast(self):
        self.locks = {}
        # While available move list is empty and number of threads is 0
        print("In fast Engine")
        while len(self.validMoves) > 0 and QThreadPool.activeThreadCount() > 0:
            # grab random move from avaible moves
            try:
                move = random.choice(self.validMoves)
            except:
                continue

            # if move neighborhood is not locked 
            moveX = move["x"]
            moveY = move["y"]


            locked = self.locks.get(toCoords(moveX, moveY))
            if locked != 1:
                
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

                # Give move and to worker from thread pool 
                worker = MoveWorker()
                worker.give(move, self)
                QThreadPool.globalInstance().start(worker)
                #print("made a thread")


class MoveWorker(QRunnable):
    # def __init__(self, move, engine):
    #     super()
    #     self.move = move
    #     self.engine = engine

    def give(self, move, engine):
        self.move = move
        self.engine = engine

    def run(self):
        # Worker Function to update move list
        self.engine.build(self.move)

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