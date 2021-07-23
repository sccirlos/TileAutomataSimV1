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
        self.tiles = []
    
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

    def set_temp(self, s):
        self.states = s

    def get_initial_states(self):
        return self.initial_states 

    def set_initial_states(self, s):
        self.initial_states = s   

    def get_seed_assembly(self):
        return self.seed_assembly

    def set_seed_assembly(self, s):
        self.seed_assembly = s       
# Step 1: Command Line with File Select 
# 

        