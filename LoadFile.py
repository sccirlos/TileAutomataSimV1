from PyQt5.QtWidgets import QFileDialog
import xml.etree.ElementTree as ET

BaseStateSet = []  # Collection of Available Base States


class BaseState:
    def __init__(self, label, color):
        self.label = label  # The base state's label
        self.color = color  # The base state's color
        # Which elements from the AffinityRules list directly involve this state?
        self.relevantAffinities = []
        # Which elements from the TransitionRules list directly involve this state?
        self.relevantTranstitions = []
    # Getters

    def returnLabel(self):
        return self.label

    def returnColor(self):
        return self.color

    def returnRelevantAffinities(self):
        return self.relevantAffinities

    def returnRelevantTransitions(self):
        return self.relevantTranstitions
    # Displayers

    def displayBasic(self):  # Displays the state's basic information
        print("Label: "+self.label+"; Color: "+self.color)
    # Appenders

    def appendAffinity(self, rule):
        self.relevantAffinities.append(rule)

    def appendTransition(self, rule):
        self.relevantTranstitions.append(rule)


class AffinityRule:
    def __init__(self, origin, dir, destination):
        self.origin = origin  # Which label will get a new neighbor?
        self.dir = dir  # Which direction will the new neighbor be placed?
        self.destination = destination  # Who's the new neighbor?
    # Getters

    def returnOrigin(self):
        return self.origin

    def returnDir(self):
        return self.dir

    def returnDestination(self):
        return self.destination
    # Displayer

    def displayRule(self):
        if(self.dir == "left"):
            print(self.destination+" connects to the left of " +
                  self.origin+" -> ["+self.destination+","+self.origin+"]")
        else:
            print(self.destination+" connects to the right of " +
                  self.origin+" ->["+self.origin+","+self.destination+"]")


class TransitionRule:
    def __init__(self, originalLeft, originalRight, finalLeft, finalRight):
        self.originalLeft = originalLeft
        self.originalRight = originalRight
        self.finalLeft = finalLeft
        self.finalRight = finalRight
    # Getters

    def returnOriginalLeft(self):
        return self.originalLeft

    def returnOriginalRight(self):
        return self.originalRight

    def returnFinalLeft(self):
        return self.finalLeft

    def returnFinalRight(self):
        return self.finalRight
    # Displayer

    def displayRule(self):
        print("["+self.originalLeft+","+self.originalRight +
              "] -> ["+self.finalLeft+","+self.finalRight+"]")

# I'm sure loading the files will grow to be complicated, so I made this file for anything relating to "Load"


def readxml(file):
    tree = ET.parse(file)
    treeroot = tree.getroot()

    AffinityRules = []  # Collection of Affinity Rules
    TransitionRules = []  # Collection of Transition Rules

    # Main: Setting TileSet
    for tile_tag in treeroot.findall('TileTypes/Tile'):
        label = tile_tag.get('Label')
        color = tile_tag.find('color').text
        tempState = BaseState(label, color)
        BaseStateSet.append(tempState)
    print("Base State Set:")
    for element in BaseStateSet:
        element.displayBasic()

    # Main: Setting System Rules
    # Sub: Setting Affinity Rules
    for rule_tag in treeroot.findall('System/AffinityRules/Rule'):
        origin = rule_tag.get('Tile')
        for direction in rule_tag:
            dir = direction.tag
            destination = direction.text.replace("\"", "")
            tempRule = AffinityRule(origin, dir, destination)
            AffinityRules.append(tempRule)

    # Sub: Setting Transition Rules
    for rule_tag in treeroot.findall('System/TransitionRules/Rule'):
        originalLeft = rule_tag.get('Left')
        originalRight = rule_tag.get('Right')
        finalLeft = rule_tag.find('left').text.replace("\"", "")
        finalRight = rule_tag.find('right').text.replace("\"", "")
        tempRule = TransitionRule(
            originalLeft, originalRight, finalLeft, finalRight)
        TransitionRules.append(tempRule)

    # Main: Displaying Relevant Rules for Each Base State
    print("\nAffinity Rules:")
    if(AffinityRules == []):
        print("NONE")
    else:
        for element in AffinityRules:
            element.displayRule()
    print("\nTransition Rules:")
    if(TransitionRules == []):
        print("NONE")
    else:
        for element in TransitionRules:
            element.displayRule()

    # Main: Assigning Each Tile's Relevant Rules
    for base_state in BaseStateSet:
        tempLabel = base_state.returnLabel()
        for rule in AffinityRules:
            if(tempLabel == rule.returnOrigin()):
                base_state.appendAffinity(rule)
        for rule in TransitionRules:
            if(tempLabel == rule.returnOriginalLeft() or tempLabel == rule.returnOriginalRight()):
                base_state.appendTransition(rule)
