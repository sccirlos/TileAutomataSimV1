from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtGui import QPainter, QBrush, QPen

from PyQt5.QtCore import Qt
from random import randrange

from assemblyEngine import Engine
from UniversalClasses import System, Assembly, Tile
import TAMainWindow
import LoadFile
import SaveFile
import Assembler_Proto

import sys

# Global Variables
currentSystem = None
currentAssemblyHistory = []
# General Seeded TA Simulator


# Takes in:
# Seed State
# Set of States
# Set of Transition Rules
# Set of Affinities
# Creates
# A list of events based on transition rules states and affinities
# Add a tile or tiles
# Transition a tile(s)
# Make new assembly
# Attach assemblies
# An Assembly
# Outputs:
#
# GUI showing step by step growth starting with seed state
# Step button
# Keep growing until their are no more rules that apply

class Ui_MainWindow(QMainWindow, TAMainWindow.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        #self.label = QtWidgets.QLabel()
        self.step = 0
        self.time = 0
        self.Engine = None
        self.play = True
        canvas = QtGui.QPixmap(850, 600)
        canvas.fill(Qt.white)
        self.label.setPixmap(canvas)

        self.label_2.setText("")

        # this is "Load" on the "File" menu
        self.actionLoad.triggered.connect(self.Click_FileSearch)

        # "Save" from the "File" menu
        self.actionSave.triggered.connect(self.Click_SaveFile)

        # this button executes the simulation. Afterwards the window updates to show results
        self.pushButton.clicked.connect(self.Click_Run_Simulation)

        self.actionFirst.triggered.connect(self.first_step)

        self.actionPrevious.triggered.connect(self.prev_step)

        self.actionStop.triggered.connect(self.stop_sequence)

        self.actionPlay.triggered.connect(self.play_sequence)

        self.actionNext.triggered.connect(self.next_step)

        self.actionLast.triggered.connect(self.last_step)

    def draw_tiles(self, assembly):
        painter = QPainter(self.label.pixmap())
        pen = QtGui.QPen()
        brush = QtGui.QBrush()
        font = QtGui.QFont()

        pen.setWidth(3)

        brush.setStyle(Qt.SolidPattern)

        pen.setColor(QtGui.QColor("white"))
        brush.setColor(QtGui.QColor("white")) 
        painter.setPen(pen)
        painter.setBrush(brush)
        painter.drawRect(0, 0, 1000, 1000) #this block is drawing a big white rectangle across the screen to "clear" it

        font.setFamily("Times")
        font.setBold(True)
        painter.setFont(font)
        for tile in assembly.tiles: 
            #print(tile[0].color)
            pen.setColor(QtGui.QColor("black"))
            brush.setColor(QtGui.QColor("#" + tile.get_color()))

            painter.setPen(pen)
            painter.setBrush(brush)
            painter.drawRect((tile.x * 40) + 200, (tile.y * -40) + 500, 40, 40)
            painter.drawText((tile.x * 40) + 210, (tile.y * -40) + 525, tile.state.label)

        painter.end()

        #if self.step != 0:
        #    self.label_2.setText("Time elapsed: " + str(self.time) + " seconds")
        #    self.label_3.setText("Current step time: " + str(1/Assembler_Proto.TimeTaken[self.step]) + " seconds")
        #else:
        #    self.label_2.setText("Time elapsed: 0 seconds")
        #    self.label_3.setText("Current step time: 0 seconds")

        self.update()

    def Click_Run_Simulation(self):  # Run application if everythings good
        err_flag = False

        if(err_flag == False):
            self.step = 0
            self.time = 0
            #Assembler_Proto.Main()
            self.draw_tiles(Assembler_Proto.CompleteAssemblyHistory[self.step])

    def Click_FileSearch(self, id):
        file = QFileDialog.getOpenFileName(self, "Select XML Document", "", "XML Files (*.xml)")
        # Simulator must clear all of LoadFile's global variables when the user attempts to load something.
        LoadFile.HorizontalAffinityRules.clear()
        LoadFile.VerticalAffinityRules.clear()
        LoadFile.HorizontalTransitionRules.clear()
        LoadFile.VerticalTransitionRules.clear()
        LoadFile.SeedAssembly.clear()
        LoadFile.SeedStateSet.clear()
        LoadFile.InitialStateSet.clear()
        LoadFile.CompleteStateSet.clear()

        LoadFile.readxml(file[0])

        if self.Engine != None:
            self.Engine.clear()

           # Creating global variables
        global temp
        global states
        global inital_states
        global seed_assembly
        global seed_states
        global vertical_affinities
        global horizontal_affinities
        global vertical_transitions
        global horizontal_transitions

         # Creating a System object from data read.
        temp = LoadFile.Temp
        states = LoadFile.CompleteStateSet
        inital_states = LoadFile.InitialStateSet
        seed_assembly = LoadFile.SeedAssembly
        seed_states = LoadFile.SeedStateSet
        vertical_affinities = LoadFile.VerticalAffinityRules
        horizontal_affinities = LoadFile.HorizontalAffinityRules
        vertical_transitions = LoadFile.VerticalTransitionRules
        horizontal_transitions = LoadFile.HorizontalTransitionRules

        # Establish the current system we're working with
        currentSystem = System(temp, states, inital_states, seed_assembly, seed_states, vertical_affinities,
                               horizontal_affinities, vertical_transitions, horizontal_transitions)
        print("\nSystem Dictionaries:")
        print("Vertical Affinities:")
        currentSystem.displayVerticalAffinityDict()
        print("Horizontal Affinities:")
        currentSystem.displayHorizontalAffinityDict()
        print("Vertical Transitions:")
        currentSystem.displayVerticalTransitionDict()
        print("Horizontal Transitions:")
        currentSystem.displayHorizontalTransitionDict()

        self.step = 0
        self.time = 0
        self.Engine = Engine(currentSystem)
        #a = Assembly()
        #t = Tile(currentSystem.returnSeedStates(), 0, 0)
        #a.tiles.append(t)
        #currentAssemblyHistory.append(a)
        #Assembler_Proto.Main()
        self.draw_tiles(self.Engine.assemblyList[self.step])

    def Click_SaveFile(self):
        # Creating a System object from data read.
        temp = LoadFile.Temp
        states = LoadFile.CompleteStateSet
        inital_states = LoadFile.InitialStateSet
        seed_assembly = LoadFile.SeedAssembly
        seed_states = LoadFile.SeedStateSet
        vertical_affinities = LoadFile.VerticalAffinityRules
        horizontal_affinities = LoadFile.HorizontalAffinityRules
        vertical_transitions = LoadFile.VerticalTransitionRules
        horizontal_transitions = LoadFile.HorizontalTransitionRules

        # Establish the current system we're working with
        currentSystem = System(temp, states, inital_states, seed_assembly, seed_states, vertical_affinities,
                               horizontal_affinities, vertical_transitions, horizontal_transitions)

        SaveFile.main(currentSystem)

    # self.draw_tiles(LoadFile.) #starting assembly goes here
        

    def first_step(self):
        self.stop_sequence()
        self.step = 0
        self.time = 0
        self.draw_tiles(self.Engine.assemblyList[self.step])

    def prev_step(self):
        self.stop_sequence()
        if self.step > 0:
            self.time = self.time - (1/Assembler_Proto.TimeTaken[self.step]) #Might need to go below
            self.step = self.step - 1
            self.draw_tiles(Assembler_Proto.CompleteAssemblyHistory[self.step])

    def next_step(self):
        self.stop_sequence()
        if self.Engine.build() != -1:
            self.step = self.step + 1
            #self.time = self.time + (1/Assembler_Proto.TimeTaken[self.step]) #Might need to go above
            self.draw_tiles(self.Engine.assemblyList[self.step])

    def last_step(self):
        self.stop_sequence()
        current = self.step
        self.step = len(Assembler_Proto.CompleteAssemblyHistory) - 1
        while (current != self.step):
            current = current + 1
            self.time = self.time + (1/Assembler_Proto.TimeTaken[current]) 

        self.draw_tiles(Assembler_Proto.CompleteAssemblyHistory[self.step])
       

    def play_sequence(self):
        self.play = True
        print(len(Assembler_Proto.CompleteAssemblyHistory))
        while(self.step < len(Assembler_Proto.CompleteAssemblyHistory) and self.play == True):
            print(self.step)
            self.draw_tiles(Assembler_Proto.CompleteAssemblyHistory[self.step])
            
            loop = QtCore.QEventLoop()
            if self.step != 0:
                QtCore.QTimer.singleShot(int(1000 / Assembler_Proto.TimeTaken[self.step]), loop.quit)
            else:
                QtCore.QTimer.singleShot(1000, loop.quit)
            loop.exec_()
            self.step = self.step + 1
            if self.step != 0 and self.step < len(Assembler_Proto.CompleteAssemblyHistory):
                self.time = self.time + (1/Assembler_Proto.TimeTaken[self.step])

        self.step = len(Assembler_Proto.CompleteAssemblyHistory) - 1 #this line is here to prevent a crash that happens if you click last after play finishes
        self.stop_sequence()

    def stop_sequence(self):
        self.play = False


if __name__ == "__main__":
    
    #App Stuff
    app = QApplication(sys.argv)
    w = Ui_MainWindow()
    w.show()
   
    sys.exit(app.exec_())
#
