from PyQt5.QtCore import QObject, pyqtSignal

# Multithreading
# 
# https://realpython.com/python-pyqt-qthread/
# 

# Worker
# Just a class that a thread can call functions from, apparently needs to inherit from Object
class Player(QObject):
    # Signals

    # A signal that will 'emit' once the work is done (or whenever you call the emit() function)
    finished = pyqtSignal()

    # default __init__ requires some fancy parameters that I didn't feel like learning about
    # must call this and give it the UiWindow
    def give_ui(self, ui):
        self.ui = ui

    # the main function that gets ran, does not really have to be called run, could be any function really
    def run(self):
        while((self.ui.Engine.step() != -1) and self.ui.play == True):
            self.ui.time = self.ui.time + (self.ui.Engine.timeTaken())
            self.ui.draw_move(self.ui.Engine.getCurrentMove(), 1)

        # tell whoever cares about the work being completed
        self.finished.emit()