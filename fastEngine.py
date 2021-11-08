# Fast Engine class
# David Caballero
# Sonya Cirlos
# Timothy Gomez

from PyQt5.QtCore import QRunnable
from assemblyEngine import Engine

class FastEngine(Engine):
    def last(self):
        self.locks = {}
        # While available move list is empty and number of threads is 0
        
            # grab random move from avaible moves


            # if move neighborhood is not locked 

                
                # Give move and to worker from thread pool 


class MoveWorker(QRunnable):
    def run(self, move):
        # Worker Function to update move list
        # Copy from engine class


        # Unlock locks 
        pass