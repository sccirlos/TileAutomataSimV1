from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog 
from PyQt5.QtGui import QPainter, QBrush, QPen

from PyQt5.QtCore import Qt

import pyqtgraph as pg
import TAMainWindow
import LoadFile
import Assembler_Proto

import sys
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

# class Tile
class Tile:
    # label
    # # changes or list of changes (start num)
    # maybe list of affinities pairs (state, direction)
    # boolean can_change

    def __init__(self, l):
        self.label = l

    def __str__(self):
        return self.label


class Assembly:
    def __init__(self):
        self.label = ""
        self.tiles = []  # tuple of (label, x, y)


class System:
    # Horizontal Hash Rules
    # Vertical Hash Rules
    # Horizontal Transition Rules
    # Vertical Transition Rules
    # Temp int
    # Initial List of States
    # Seed Assembly Object
    def __init__(self, temp=None, states=None, initial_states=None, seed_assembly=None, vertical_affinities=None, horizontal_affinities=None, vertical_transition_rules=None, horizontal_transition_rules=None):
        self.temp = temp
        # Takes 2 tiles [N][S] and returns the glue strength between them as an int
        self.vertical_affinities = vertical_affinities
        # Takes 2 tiles [W][E] and returns the glue strength between them as an int
        self.horizontal_affinities = horizontal_affinities
        # Takes 2 tiles [N][S] and and returns the transition pair
        self.vertical_transition_rules = vertical_transition_rules
        # Takes 2 tiles [W][E] and returns the transition pair
        self.horizontal_transition_rules = horizontal_transition_rules
        self.states = states
        self.initial_states = initial_states
        self.seed_assembly = seed_assembly

    def get_temp(self):
        return self.temp

    def set_temp(self, t):
        self.temp = t

    def get_vertical_affinities(self):
        return self.vertical_affinities

    def set_vertical_affinities(self, v):
        self.vertical_affinities = v

    def get_horizontal_affinities(self):
        return self.horizontal_affinities

    def set_horizontal_affinities(self, h):
        self.horizontal_affinities = h

    def get_vertical_transition_rules(self):
        return self.vertical_transition_rules

    def set_vertical_transition_rules(self, v):
        self.vertical_transition_rules = v

    def get_horizontal_transition_rules(self):
        return self.horizontal_transition_rules

    def set_horizontal_transition_rules(self, v):
        self.horizontal_transition_rules = v

    def get_states(self):
        return self.states

    def set_states(self, s):
        self.states = s

    def get_initial_states(self):
        return self.initial_states

    def set_initial_states(self, s):
        self.initial_states = s

    def get_seed_assembly(self):
        return self.seed_assembly

    def set_seed_assembly(self, s):
        self.seed_assembly = s

    def add_transition_rule(self, tr, direct):
        if direct == "v":
            self.vertical_transition_rules.append(tr)
        else:
            self.horizontal_transition_rules.append(tr)

    def add_affinity(self, a, direct):
        if direct == "v":
            self.vertical_affinities.append(a)
        else:
            self.horizontal_affinities.append(a)
# Step 1: Command Line with File Select
#


class Ui_MainWindow(QMainWindow, TAMainWindow.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        #self.label = QtWidgets.QLabel()
        canvas = QtGui.QPixmap(850, 600)
        canvas.fill(Qt.white)
        self.label.setPixmap(canvas)

        self.actionLoad.triggered.connect(self.Click_FileSearch) #this is "Load" on the "File" menu
        
        self.pushButton.clicked.connect(self.Click_Run_Simulation) #this button executes the simulation. Afterwards the window updates to show results

    def draw_tiles(self, assembly):
        painter = QPainter(self.label.pixmap())
        pen = QtGui.QPen()
        brush = QtGui.QBrush()
        font = QtGui.QFont()

        pen.setWidth(3)

        brush.setStyle(Qt.Dense1Pattern)

        font.setFamily("Times")
        font.setBold(True)
        painter.setFont(font)
        for stuff in assembly:
            #print(stuff.color)
            pen.setColor(QtGui.QColor("black"))
            brush.setColor(QtGui.QColor("#" + stuff.color))

            painter.setPen(pen)
            painter.setBrush(brush)
            painter.drawRect((stuff.x * 40) + 80, (stuff.y * 40) + 80, 40, 40)
            painter.drawText((stuff.x * 40) + 90, (stuff.y * 40) + 105, stuff.label)

        painter.end()
        self.update()

    def Click_Run_Simulation(self): # Run application if everythings good
        err_flag = False

        if(err_flag == False):
            Assembler_Proto.Main()
            self.draw_tiles(Assembler_Proto.AssemblyHistory)

    def Click_FileSearch(self, id):
        file = QFileDialog.getOpenFileName(
            self, "Select XML Document", "", "XML Files (*.xml)")
        LoadFile.readxml(file[0])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Ui_MainWindow()
    w.show()
    sys.exit(app.exec_())
#
