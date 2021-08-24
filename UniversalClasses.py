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