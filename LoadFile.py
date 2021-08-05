from PyQt5.QtWidgets import QFileDialog 
import xml.etree.ElementTree as ET

class BaseState:
    def __init__(self, label, color):
        self.label = label #The base state's label
        self.color = color #The base state's color
        self.relevantAffinities = [] #Which elements from the AffinityRules list directly involve this state?
        self.relevantTranstitions = [] #Which elements from the TransitionRules list directly involve this state?
    def displayBasic(self): #Displays the state's basic information
        print("Label: "+self.label+"; Color: "+self.color)

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
    
    BaseStateSet = [] #Collection of Available Tiles
    AffinityRules = [] #Collection of Affinity Rules
    TransitionRules = [] #Collection of Transition Rules

    #Main: Setting TileSet
    for tile_tag in treeroot.findall('TileTypes/Tile'):
        label = tile_tag.get('Label')
        color = tile_tag.find('color').text
        tempState = BaseState(label, color)
        BaseStateSet.append(tempState)
    print("Base State Set:")
    for element in BaseStateSet:
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
