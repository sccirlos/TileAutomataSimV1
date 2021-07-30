from PyQt5.QtWidgets import QFileDialog 
import xml.etree.ElementTree as ET

class Tile:
    def __init__(self, label,x, y, color):
        self.label = label #The tile's label
        self.x = x #The tile's starting x-position; Can be used as an int
        self.y = y #The tile's starting y-position; Can be used as an int
        self.color = color
        #NOTE: These attributes could be added directly into the simulation portion rather than the load portion here.
        self.left = "None" #The tile's left neighbor; L&R will be used later to track the tiles.
        self.right = "None" #The tile's right neighbor
        self.relevantAffinities = [] #Which elements from the AffinityRules list directly involve this tile?
        self.relevantTranstitions = [] #Which elements from the TransitionRules list directly involve this tile?
    def displayBasic(self): #Displays the basic information
        print("Label: "+self.label+"; Spawning X-Coordinate: "+self.x+"; Spawning Y-Coordinate: "+self.y+"; Color: "+self.color)

class AffinityRule:
    def __init__(self, origin, dir, destination):
        self.origin = origin #Which label will get a new neighbor?
        self.dir = dir #Which direction will the new neighbor be placed?
        self.destination = destination #Who's the new neighbor?
    def displayRule(self):
        if(self.dir == "left"):
            print(self.destination+" connects to the left of "+self.origin+" -> ["+self.destination+","+self.origin+"]")
        else:
            print(self.destination+" connects to the right of "+self.origin+" ->["+self.origin+","+self.destination+"]")

class TransitionRule:
    def __init__(self, originalLeft, originalRight, finalLeft, finalRight):
        self.originalLeft = originalLeft
        self.originalRight = originalRight
        self.finalLeft = finalLeft
        self.finalRight = finalRight
    def displayRule(self):
        print("["+self.originalLeft+","+self.originalRight+"] -> ["+self.finalLeft+","+self.finalRight+"]")
        
#I'm sure loading the files will grow to be complicated, so I made this file for anything relating to "Load"
def readxml(file):
    tree = ET.parse(file)
    treeroot = tree.getroot()
    
    TileSet = [] #Collection of Available Tiles
    AffinityRules = [] #Collection of Affinity Rules
    TransitionRules = [] #Collection of Transition Rules

    #Main: Setting TileSet
    for tile_tag in treeroot.findall('TileTypes/Tile'):
        label = tile_tag.get('Label')
        xPosition = tile_tag.find('x').text
        yPosition = tile_tag.find('y').text
        color = tile_tag.find('color').text
        tempTile = Tile(label, xPosition, yPosition, color)
        TileSet.append(tempTile)
    print("Inital Tile Set:")
    for element in TileSet:
        element.displayBasic()

    #Main: Setting System Rules
    #Sub: Setting Affinity Rules
    for rule_tag in treeroot.findall('System/AffinityRules/Rule'):
        origin = rule_tag.get('Tile')
        for direction in rule_tag:
            dir = direction.tag
            destination = direction.text.replace("\"", "")
            tempRule = AffinityRule(origin, dir, destination)
            AffinityRules.append(tempRule)
    print("\nAffinity Rules:")
    for element in AffinityRules:
        element.displayRule()

    #Sub: Setting Transition Rules
    for rule_tag in treeroot.findall('System/TransitionRules/Rule'):
        originalLeft = rule_tag.get('Left')
        originalRight = rule_tag.get('Right')
        finalLeft = rule_tag.find('left').text.replace("\"", "")
        finalRight = rule_tag.find('right').text.replace("\"", "")
        tempRule = TransitionRule(originalLeft, originalRight, finalLeft, finalRight)
        TransitionRules.append(tempRule)
    print("\nTransition Rules:")
    for element in TransitionRules:
        element.displayRule()
