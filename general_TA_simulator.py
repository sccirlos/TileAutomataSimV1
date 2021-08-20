from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtGui import QPainter, QBrush, QPen

from PyQt5.QtCore import Qt
from random import randrange

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
                        stren = (sy.get_vertical_affinities())[neighborN.getLabel()][iTile]
                        if(stren != None): attStr += stren
                    if(neighborS != None):
                        stren = (sy.get_vertical_affinities())[iTile][neighborS.getLabel()]
                        if(stren != None): attStr += stren
                    if(neighborE != None):
                        stren = (sy.get_horizontal_affinities())[iTile][neighborE.getLabel()]
                        if(stren != None): attStr += stren
                    if(neighborW != None):
                        stren = (sy.get_horizontal_affinities())[neighborW.getLabel()][iTile]
                        if(str != None): attStr += stren

                    if attStr >= sy.getTemp():
                        attMove = {"type": "a"}

                        attMove["x"] = iX
                        attMove["y"] = iY
                        attMove["state1"] = iTile.getLabel

                        attachments_list.append(attMove)



            #ttc = (i-1, i)
            #ttl = (t1, t2)
            #print(ttl)
            #if ttl in sys_attachments:
                #attachments_list.append((ttc, ttl, sys_attachments[ttl]))
        return attachments_list     

    def set_attachments(self, att): # tuple of ((coord pair), (current labels), (transition labels))
        a = Assembly()
        a.label = self.label + "T " #+ 
        a.tiles = self.tiles
        #change = trans[0][0]
       # print(a.tiles[change][0])
        #print(trans[2][1])
       # print(trans[0])
        #a.tiles[change] = trans[2][1]
        print("New Assembly Tiles: ", a.tiles)

        ########## TO DO Update boundaries
        attach = att[0][0]
        a.tiles[attach]



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
            print(sys_h_tiles[iTile.get_label()])
            
            iHTranRules = sys_h_tr[sys_h_tiles[iTile.get_label()]]
            iVTranRules = sys_v_tr[sys_v_tiles[iTile.get_label()]]


            # Get only the south and east neighbors of iTile
            neighborS = self.coords.get(toCoords(iTile.x, iTile.y - 1))
            neighborE = self.coords.get(toCoords(iTile.x + 1, iTile.y))

            if(neighborS != None):
                # second dictionary
                rules = iVTranRules.get(neighborS.getLabel())

                if rules != None:
                    move = {"type": "t"}
                    move["x"] = iTile.x
                    move["y"] = iTile.y
                    move["state1"] = iTile.getLabel()
                    move["state2"] = neighborS.getLabel()

                    # a pair of states may have mutliple rules
                    for i in range(rules.length()):
                        #class is in universal classes
                        move["state1Final"] = rules[i].returnLabel1Final() 
                        move["state2Final"] = rules[i].returnLabel2Final() 
                        transitions_list.append(move)

            if(neighborE != None):
                rules = iHTranRules.get(neighborE.getLabel())
                if rules != None:
                    move = {"type": "t"}
                    move["x"] = iTile.x
                    move["y"] = iTile.y
                    move["state1"] = iTile.getLabel()
                    move["state2"] = neighborE.getLabel()

                    for i in range(rules.length()):
                        move["state1Final"] = rules[i].returnLabel1Final() 
                        move["state2Final"] = rules[i].returnLabel2Final() 
                        transitions_list.append(move)


        return transitions_list      

    def set_transition(self, trans): # tuple of ((coord pair), (current labels), (transition labels))
        a = Assembly()
        a.label = self.label + "T "+ trans[2][0] + trans[2][1]
        a.tiles = self.tiles
        change = trans[0][0]
        print(a.tiles[change][0])
        print(trans[2][1])
        print(trans[0])
        #a.tiles[change] = trans[2][1]
        print("New Assembly Tiles: ", a.tiles)
        return a

    def getMoves(self, sy):
        return self.get_attachments(sy) + self.get_transitions(sy)
    
class System:
    # Horizontal Hash Rule
    # Vertical Hash Rules
    # Horizontal Transition Rules
    # Vertical Transition Rules
    # Temp int
    # Initial List of States
    # Seed Assembly Object
    def __init__(self, temp=None, states=None, initial_states=None, seed_assembly=None, seed_states=None, vertical_affinities=None, horizontal_affinities=None, vertical_transition_rules=None, horizontal_transition_rules=None, tile_vertical_transitions=None, tile_horizontal_transitions=None):
        self.temp = temp
        self.vertical_affinities = vertical_affinities #Takes 2 tiles [N][S] and returns the glue strength between them as an int
        self.horizontal_affinities = horizontal_affinities #Takes 2 tiles [W][E] and returns the glue strength between them as an int
        self.vertical_transition_rules = vertical_transition_rules #Takes 2 tiles [N][S] and and returns the transition pair
        self.horizontal_transition_rules = horizontal_transition_rules #Takes 2 tiles [W][E] and returns the transition pair
        self.tile_vertical_transitions = tile_vertical_transitions #Takes tile and returns vertical transition pairs
        self.tile_horizontal_transitions = tile_horizontal_transitions #Takes tile and returns horizontal transition pairs
        
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

    def set_horizontal_transition_rules(self, h):
        self.horizontal_transition_rules = h

    def get_tile_vertical_transitions(self):
        return self.tile_vertical_transitions

    def set_tile_vertical_transitions(self, tile_vt):
        self.tile_vertical_transitions = tile_vt

    def get_tile_horizontal_transitions(self):
        return self.tile_horizontal_transitions

    def set_tile_horizontal_transitions(self, tile_ht):
        self.tile_horizontal_transitions = tile_ht

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

    def get_seed_states(self):
        return self.seed_states

    # TO DO Update these to write to a dictionary, and to use lists of objects from universalClasses.py
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

        file = QFileDialog.getOpenFileName(
            self, "Select XML Document", "", "XML Files (*.xml)")
        LoadFile.readxml(file[0])

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
    #Basic Dummy Data for Assembly
    tiles = []
    
    S_tile = Tile("S", 0, 0)
    tiles.append(S_tile)
    A_tile = Tile("A", 1, 0)
    tiles.append(A_tile)
    B_tile = Tile("B", 2, 0)
    tiles.append(B_tile)
    C_tile = Tile("C", 3, 0)
    tiles.append(C_tile)
    D_tile = Tile("D", 4, 0)
    tiles.append(D_tile)
    
    assembly = Assembly()
    assembly.set_label("Dummy")
    assembly.set_tiles(tiles)
    st = ["S", "A", "B", "C", "D", "E", "V", "W", "X", "Y", "Z"]
    intst = ["S", "A", "B", "C", "D", "E"]
    
    # still needs transition rules and affinities
    system = System(temp=1, states=st, seed_assembly=assembly, initial_states=intst)

    #add transition rules
    ht_rules = {} #
    vt_rules = {}
    tile_ht = {}
    S = "S"
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    SA = ("S", "A")
    AB = ("A", "B")
    BC = ("B", "C")
    CD = ("C", "D")
    DE = ("D", "E")
    SV = ("S", "V")
    AW = ("A", "W")
    BX = ("B", "X")
    CY = ("C", "Y")
    DZ = ("D", "Z")
    
    tile_ht[S] = SA
    tile_ht[A] = AB
    tile_ht[B] = (AB, BC)
    tile_ht[C] = (BC, CD)
    tile_ht[D] = (CD, DE)

    ht_rules[SA] = SA
    ht_rules[AB] = AW
    ht_rules[BC] = BX
    ht_rules[CD] = CY
    ht_rules[DE] = DZ

    tile_vt[S] = SA
    tile_vt[A] = AB
    tile_vt[B] = (AB, BC)
    tile_vt[C] = (BC, CD)
    tile_vt[D] = (CD, DE)

    vt_rules[SA] = SA
    vt_rules[AB] = AW
    vt_rules[BC] = BX
    vt_rules[CD] = CY
    vt_rules[DE] = DZ
    print("Horizontal Transition Rules: ", ht_rules)
    system.set_horizontal_transition_rules(ht_rules)
    system.set_vertical_transition_rules(vt_rules)
    system.set_tile_horizontal_transitions(tile_ht)
    system.set_tile_vertical_transitions(tile_vt)
    tr_list = assembly.get_transitions(system)
    print("Transitions List: ", tr_list)
    ind = randrange(len(tr_list) -1)
    pickedt = tr_list[ind]
    print(pickedt)
    a1 = assembly.set_transition(pickedt)
    #App Stuff
    app = QApplication(sys.argv)
    w = Ui_MainWindow()
    w.show()
   
    sys.exit(app.exec_())
#
