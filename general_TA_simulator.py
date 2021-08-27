from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtGui import QPainter, QBrush, QPen

from PyQt5.QtCore import Qt
from random import randrange

from UniversalClasses import System
import TAMainWindow
import LoadFile
import SaveFile
import Assembler_Proto

import sys

# Global Variables
currentSystem = None

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

def toCoords(x, y):
    return "(" + str(x) + "," + str(y) + ")"

class Tile:
    # label
    # # changes or list of changes (start num)
    # maybe list of affinities pairs (state, direction)
    # boolean can_change
    
    def __init__(self, l, _x, _y):
        self.label = l
        self.x = _x
        self.y = _y

    def __str__(self):
        s = self.label + " (" + self.x + ", " + self.y + ")"
        return s

    def get_label(self):
        return self.label

    def set_label(self, l):
        self.label = l
class Assembly:
    def __init__(self):
        self.label = ""
        self.tiles = [] #tuple of (label, x, y)
        self.coords = {} #mapping of strings (x, y) to tiles
        self.leftMost = 0
        self.rightMost = 0
        self.upMost = 0
        self.downMost = 0

    def get_label(self):
        return self.label
    def set_label(self, l):
        self.label = l
            
    def get_tiles(self):
        return self.tiles

    def set_tiles(self, t):
        self.tiles = t

        for tileI in self.tiles:
            self.coords["(" + str(tileI.x) + "," + str(tileI.y) + ")" ] = tileI
            # TO DO update boundaries


    # Sonya on attachments
    def get_attachments(self, sy): #takes in a system
        attachments_list = []
        # sys_attachments = sy.get_initial_states()
        # sys_v_transition_rules = sy.get_vertical_transition_rules
        
        
        for iX in range(self.leftMost, self.rightMost + 1):
            for iY in range(self.downMost, self.upMost + 1):

                # Check if position is empty
                if self.coords.get(toCoords(iX, iY)) != None: continue

                # Get each neighbor
                neighborN = self.coords.get(toCoords(iX, iY + 1))
                neighborS = self.coords.get(toCoords(iX, iY - 1))
                neighborE = self.coords.get(toCoords(iX + 1, iY))
                neighborW = self.coords.get(toCoords(iX - 1, iY))


                # Calcuate the str of each tile attaching at this position
                for iTile in sy.getInitialStates():
                    attStr = 0

                    if(neighborN != None):
                        stren = (sy.get_vertical_affinities())[neighborN.get_label()][iTile]
                        if(stren != None): attStr += stren
                    if(neighborS != None):
                        stren = (sy.get_vertical_affinities())[iTile][neighborS.get_label()]
                        if(stren != None): attStr += stren
                    if(neighborE != None):
                        stren = (sy.get_horizontal_affinities())[iTile][neighborE.get_label()]
                        if(stren != None): attStr += stren
                    if(neighborW != None):
                        stren = (sy.get_horizontal_affinities())[neighborW.get_label()][iTile]
                        if(str != None): attStr += stren

                    if attStr >= sy.getTemp():
                        attMove = {"type": "a"}

                        attMove["x"] = iX
                        attMove["y"] = iY
                        attMove["state1"] = iTile.get_label()

                        attachments_list.append(attMove)

            #ttc = (i-1, i)
            #ttl = (t1, t2)
            #print(ttl)
            #if ttl in sys_attachments:
                #attachments_list.append((ttc, ttl, sys_attachments[ttl]))
        return attachments_list     
                                    # ORIGINAL tuple of ((coord pair), (current labels), (transition labels))
    def set_attachments(self, att): # tuple of ((type: ), (x: ), (y: ), (state1: ))
        a = Assembly()
        a.label = self.label + "A " + att["state1"] 
        a.tiles = self.tiles
        #change = trans[0][0]
       # print(a.tiles[change][0])
        #print(trans[2][1])
       # print(trans[0])
        #a.tiles[change] = trans[2][1]
        print("New Assembly Tiles: ", a.tiles)

        ########## TO DO Update boundaries
        att_tile = Tile(att["state1"], att["x"], att["y"])
        a.tiles[att["x"]][att["y"]] = att_tile

        return a
    
    #Elise on transitions    
    def get_transitions(self, sy): #takes in a system
            #t1 = (self.tiles[i-1][0])
            #t2 = (self.tiles[i][0])
            #ttc = (i-1, i)
            #ttl = (t1, t2)
            
            #print(ttl)
            #if ttl in sys_h_tr:
                #transitions_list.append((ttc, ttl, sys_h_transition_rules[ttl]))
        
        transitions_list = []
        sys_h_tr = sy.get_horizontal_transition_rules()
        sys_v_tr = sy.get_vertical_transition_rules()
        sys_h_tiles = sy.get_tile_horizontal_transitions()
        sys_v_tiles = sy.get_tile_vertical_transitions()

        # Check each tile in the assembly
        for iTile in self.tiles:
           # print(sys_h_tiles[iTile.get_label()])
            if isinstance(sys_h_tiles[iTile.get_label()], tuple):
                iHTranRules = sys_h_tr[sys_h_tiles[iTile.get_label()]]
            else:
                for tiles in sys_h_tiles[iTile.get_label()]:
                    iHTranRules = sys_h_tr[tiles]

            if isinstance(sys_v_tiles[iTile.get_label()], tuple):
                iVTranRules = sys_v_tr[sys_v_tiles[iTile.get_label()]]
            else:
                for tiles in sys_v_tiles[iTile.get_label()]:
                    iVTranRules = sys_v_tr[tiles]

            # Get only the south and east neighbors of iTile
            neighborS = self.coords.get(toCoords(iTile.x, iTile.y - 1))
            neighborE = self.coords.get(toCoords(iTile.x + 1, iTile.y))

            if(neighborS != None):
                # second dictionary
                # rules = iVTranRules.get(neighborS.get_label())
                rules = []
                rules.append(iVTranRules)
                if rules != None:
                    move = {"type": "t"}
                    move["x"] = iTile.x
                    move["y"] = iTile.y
                    move["state1"] = iTile.get_label()
                    move["state2"] = neighborS.get_label()

                    # a pair of states may have mutliple rules
                    for i in range(len(rules)):
                        #class is in universal classes
                        move["state1Final"] = rules[i][0] #.returnLabel1Final() 
                        move["state2Final"] = rules[i][1] #.returnLabel2Final() 
                        transitions_list.append(move)

            if(neighborE != None):
                #rules = iHTranRules[neighborE.get_label()]
                rules = []
                rules.append(iHTranRules)
                if rules != None:
                    move = {"type": "t"}
                    move["x"] = iTile.x
                    move["y"] = iTile.y
                    move["state1"] = iTile.get_label()
                    move["state2"] = neighborE.get_label()

                    for i in range(len(rules)):
                        #print(rules[i])
                        move["state1Final"] = rules[i][0] #.returnLabel1Final() 
                        move["state2Final"] = rules[i][1] #.returnLabel2Final() 
                        transitions_list.append(move)

        return transitions_list      
                                     # ORIGINAL ((type: ), (current labels), (transition labels))
    def set_transition(self, trans): # tuple of {'type': 't', 'x': 0, 'y': 0, 'state1': 'S', 'state2': 'A', 'state1Final': 'S', 'state2Final': 'A'}
        a = Assembly()
        a.label = self.label + "T "+ trans["state1Final"] + trans["state2Final"] #originally trans[2][0] + trans[2][1]
        a.tiles = self.tiles
        change = trans["type"]
        
        #print(a.tiles[change])
        print(trans["state2Final"])
        print(trans["type"])
        a.tiles[trans["x"]][trans["y"]] = trans["state2Final"]
        print("New Assembly Tiles: ", a.tiles)
        return a

    def getMoves(self, sy):
        return self.get_attachments(sy) + self.get_transitions(sy)


class Ui_MainWindow(QMainWindow, TAMainWindow.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        #self.label = QtWidgets.QLabel()
        self.step = 0
        self.time = 0
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
        for tile in assembly: 
            pen.setColor(QtGui.QColor("black"))
            brush.setColor(QtGui.QColor("#" + tile.color))

            painter.setPen(pen)
            painter.setBrush(brush)
            painter.drawRect((tile.x * 40) + 200, (tile.y * -40) + 500, 40, 40)
            painter.drawText((tile.x * 40) + 210, (tile.y * -40) + 525, tile.label)

        painter.end()

        if self.step != 0:
            self.label_2.setText("Time elapsed: " + str(self.time) + " seconds")
            self.label_3.setText("Current step time: " + str(1/Assembler_Proto.TimeTaken[self.step]) + " seconds")
        else:
            self.label_2.setText("Time elapsed: 0 seconds")
            self.label_3.setText("Current step time: 0 seconds")

        self.update()

    def Click_Run_Simulation(self):  # Run application if everythings good
        err_flag = False

        if(err_flag == False):
            self.step = 0
            self.time = 0
            #Assembler_Proto.Main()
            self.draw_tiles(Assembler_Proto.CompleteAssemblyHistory[self.step])

    def Click_FileSearch(self, id):
        # Simulator must clear all of LoadFile's global variables when the user attempts to load something.
        LoadFile.HorizontalAffinityRules.clear()
        LoadFile.VerticalAffinityRules.clear()
        LoadFile.HorizontalTransitionRules.clear()
        LoadFile.VerticalTransitionRules.clear()
        LoadFile.SeedAssembly.clear()
        LoadFile.SeedStateSet.clear()
        LoadFile.InitialStateSet.clear()
        LoadFile.CompleteStateSet.clear()

        file = QFileDialog.getOpenFileName(self, "Select XML Document", "", "XML Files (*.xml)")
        LoadFile.readxml(file[0])

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

        ates = LoadFile.CompleteStateSet
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
        #Assembler_Proto.Main()
        #self.draw_tiles(Assembler_Proto.CompleteAssemblyHistory[self.step])

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
        self.draw_tiles(Assembler_Proto.CompleteAssemblyHistory[self.step])

    def prev_step(self):
        self.stop_sequence()
        if self.step > 0:
            self.time = self.time - (1/Assembler_Proto.TimeTaken[self.step]) #Might need to go below
            self.step = self.step - 1
            self.draw_tiles(Assembler_Proto.CompleteAssemblyHistory[self.step])

    def next_step(self):
        self.stop_sequence()
        if self.step < len(Assembler_Proto.CompleteAssemblyHistory) - 1:
            self.step = self.step + 1
            self.time = self.time + (1/Assembler_Proto.TimeTaken[self.step]) #Might need to go above
            self.draw_tiles(Assembler_Proto.CompleteAssemblyHistory[self.step])

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
