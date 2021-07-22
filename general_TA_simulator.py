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
    
        
     
# Step 1: Command Line with File Select 
#         