# These classes are used for Loading and Saving Files and Communicating with general_TA_simulator.

class State:
    def __init__(self, label, color):
        self.label = label
        self.color = color

    # Getters
    def returnLabel(self):
        return self.label

    def returnColor(self):
        return self.color

class Tile:
    # label
    # # changes or list of changes (start num)
    # maybe list of affinities pairs (state, direction)
    # boolean can_change
    
    def __init__(self, s, _x, _y):
        self.state = s
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

# Not in use right now.
class SeedAssemblyTile:
    def __init__(self, label, x, y):
        self.label = label
        self.x = x
        self.y = y


class AffinityRule:
    def __init__(self, label1, label2, dir, strength):
        self.label1 = label1  # Left/Upper label
        self.label2 = label2  # Right/Bottom label
        self.dir = dir  # Horizontal or Vertical
        self.strength = strength  # Bond Strength (as a string)

    # Getters
    def returnLabel1(self):
        return self.label1

    def returnLabel2(self):
        return self.label2

    def returnDir(self):
        return self.dir

    def returnStr(self):
        return self.strength


class TransitionRule:
    def __init__(self, label1, label2, label1Final, label2Final, dir):
        self.label1 = label1
        self.label2 = label2
        self.label1Final = label1Final
        self.label2Final = label2Final
        self.dir = dir

    # Getters
    def returnLabel1(self):
        return self.label1

    def returnLabel2(self):
        return self.label2

    def returnLabel1Final(self):
        return self.label1Final

    def returnLabel2Final(self):
        return self.label2Final

    def returnDir(self):
        return self.dir


# System is used for the assembler; represents the data in the XML
class System:
    # Horizontal Hash Rule
    # Vertical Hash Rules
    # Horizontal Transition Rules
    # Vertical Transition Rules
    # Temp int
    # Initial List of States
    # Seed Assembly Object
    def __init__(self, temp, states, initial_states, seed_assembly, seed_states=None, vertical_affinities_list=None, horizontal_affinities_list=None, vertical_transitions_list=None, horizontal_transitions_list=None, tile_vertical_transitions=None, tile_horizontal_transitions=None):
        self.temp = temp
        self.states = states
        self.initial_states = initial_states
        self.seed_assembly = seed_assembly
        self.seed_states = seed_states

        # List versions of rules
        # Takes 2 tiles [N][S] and returns the glue strength between them as an int
        self.vertical_affinities_list = vertical_affinities_list
        # Takes 2 tiles [W][E] and returns the glue strength between them as an int
        self.horizontal_affinities_list = horizontal_affinities_list
        # Takes 2 tiles [N][S] and and returns the transition pair
        self.vertical_transitions_list = vertical_transitions_list
        # Takes 2 tiles [W][E] and returns the transition pair
        self.horizontal_transitions_list = horizontal_transitions_list

        #Takes tile and returns vertical transition pairs
        self.tile_vertical_transitions = tile_vertical_transitions 
        #Takes tile and returns horizontal transition pairs
        self.tile_horizontal_transitions = tile_horizontal_transitions 

        # Establish dictionaries
        self.vertical_affinities_dict = {}
        self.horizontal_affinities_dict = {}
        self.vertical_transitions_dict = {}
        self.horizontal_transitions_dict = {}

        # Translate list versions into dictionary versions
        for rule in vertical_affinities_list:
            label1 = rule.returnLabel1()
            label2 = rule.returnLabel2()
            str = rule.returnStr()

            self.vertical_affinities_dict[label1, label2] = str
        for rule in horizontal_affinities_list:
            label1 = rule.returnLabel1()
            label2 = rule.returnLabel2()
            str = rule.returnStr()

            self.horizontal_affinities_dict[label1, label2] = str
        for rule in vertical_transitions_list:
            label1 = rule.returnLabel1()
            label2 = rule.returnLabel2()
            label1Final = rule.returnLabel1Final()
            label2Final = rule.returnLabel2Final()

            self.vertical_transitions_dict[label1, label2] = (
                label1Final, label2Final)
        for rule in horizontal_transitions_list:
            label1 = rule.returnLabel1()
            label2 = rule.returnLabel2()
            label1Final = rule.returnLabel1Final()
            label2Final = rule.returnLabel2Final()

            self.horizontal_transitions_dict[label1, label2] = (
                label1Final, label2Final)

    # Getters
    def returnTemp(self):
        return self.temp

    def returnStates(self):
        return self.states

    def returnInitalStates(self):
        return self.initial_states

    def returnSeedStates(self):
        return self.seed_states

    def returnVerticalAffinityDict(self):
        return self.vertical_affinities_dict

    def returnHorizontalAffinityDict(self):
        return self.horizontal_affinities_dict

    def returnVerticalTransitionDict(self):
        return self.vertical_transitions_dict

    def returnHorizontalTransitionDict(self):
        return self.horizontal_transitions_dict

    def get_tile_vertical_transitions(self):
        return self.tile_vertical_transitions

    def get_tile_horizontal_transitions(self):
        return self.tile_horizontal_transitions

    # Displayers

    def displayVerticalAffinityDict(self):
        print(self.vertical_affinities_dict)

    def displayHorizontalAffinityDict(self):
        print(self.horizontal_affinities_dict)

    def displayVerticalTransitionDict(self):
        print(self.vertical_transitions_dict)

    def displayHorizontalTransitionDict(self):
        print(self.horizontal_transitions_dict)

    # TO DO Update these to write to a dictionary, and to use lists of objects from universalClasses.py

    def set_tile_vertical_transitions(self, tile_vt):
        self.tile_vertical_transitions = tile_vt

    def set_tile_horizontal_transitions(self, tile_ht):
        self.tile_horizontal_transitions = tile_ht

    def add_transition_rule(self, tr, direct):
        if direct == "v":
            self.vertical_transitions.append(tr)
        else:
            self.horizontal_transitions.append(tr)

    def add_affinity(self, a, direct):
        if direct == "v":
            self.vertical_affinities.append(a)
        else:
            self.horizontal_affinities.append(a)