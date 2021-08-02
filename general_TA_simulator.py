from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog 
from random import randrange
import TAMainWindow
import LoadFile

import sys
#General Seeded TA Simulator 


#Takes in:
    #Seed State 
    #Set of States
    #Set of Transition Rules
    #Set of Affinities
# Creates
    # A list of events based on transition rules states and affinities
        # Add a tile or tiles
        # Transition a tile(s)
        # Make new assembly
        # Attach assemblies
    # An Assembly
#Outputs:
    # 
    #GUI showing step by step growth starting with seed state
    #Step button
    #Keep growing until their are no more rules that apply

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
        self.tiles = [] #tuple of (label, x, y)
    def get_label(self):
        return self.label
    def set_label(self, l):
        self.label = l
            
    def get_tiles(self):
        return self.tiles

    def set_tiles(self, t):
        self.tiles = t
    # Sonya on attachments

    #Elise on transitions    
    def get_transitions(self, sy): #takes in a system
        transitions_list = []
        sys_h_transition_rules = sy.get_horizontal_transition_rules()
        # sys_v_transition_rules = sy.get_vertical_transition_rules
        for i in range(1, len(self.tiles)-1):
            t1 = (self.tiles[i-1][0])
            t2 = (self.tiles[i][0])
            ttc = (i-1, i)
            ttl = (t1, t2)
            print(ttl)
            if ttl in sys_h_transition_rules:
                transitions_list.append((ttc, ttl, sys_h_transition_rules[ttl]))
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
    
class System:
    # Horizontal Hash Rule
    # Vertical Hash Rules
    # Horizontal Transition Rules
    # Vertical Transition Rules
    # Temp int
    # Initial List of States
    # Seed Assembly Object
    def __init__(self, temp=None, states=None, initial_states=None, seed_assembly=None, vertical_affinities=None, horizontal_affinities=None, vertical_transition_rules=None, horizontal_transition_rules=None):
        self.temp = temp
        self.vertical_affinities = vertical_affinities #Takes 2 tiles [N][S] and returns the glue strength between them as an int
        self.horizontal_affinities = horizontal_affinities #Takes 2 tiles [W][E] and returns the glue strength between them as an int
        self.vertical_transition_rules = vertical_transition_rules #Takes 2 tiles [N][S] and and returns the transition pair
        self.horizontal_transition_rules = horizontal_transition_rules #Takes 2 tiles [W][E] and returns the transition pair
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

        self.actionLoad.triggered.connect(self.Click_FileSearch) #this is "Load" on the "File" menu
        
        self.pushButton.clicked.connect(self.Click_Run_Simulation) #this button executes the simulation. Afterwards the window updates to show results

    def Click_Run_Simulation(self): # Run application if everythings good
        err_flag = False
        
            
        if(err_flag == False):
            print("all good")
            #display results

    def Click_FileSearch(self, id):
        file = QFileDialog.getOpenFileName(self,"Select XML Document", "","XML Files (*.xml)")
        LoadFile.readxml(file[0])       



if __name__ == "__main__":
    #Basic Dummy Data for Assembly
    tiles = []
    S_tile = ("S", 0, 0)
    tiles.append(S_tile)
    A_tile = ("A", 1, 0)
    tiles.append(A_tile)
    B_tile = ("B", 2, 0)
    tiles.append(B_tile)
    C_tile = ("C", 3, 0)
    tiles.append(C_tile)
    D_tile = ("D", 4, 0)
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
    ht_rules[AB] = AW
    ht_rules[BC] = BX
    ht_rules[CD] = CY
    ht_rules[DE] = DZ
    print("Horizontal Transition Rules: ", ht_rules)
    system.set_horizontal_transition_rules(ht_rules)
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

        
