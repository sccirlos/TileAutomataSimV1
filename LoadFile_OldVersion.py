from PyQt5.QtWidgets import QFileDialog
import xml.etree.ElementTree as ET

BaseStateSet = []  # Collection of Available Base States
TransitionStateSet = []  # Collection of Available Transition States


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
                  self.origin+" -> ["+self.destination+"|"+self.origin+"]")
        elif(self.dir == "right"):
            print(self.destination+" connects to the right of " +
                  self.origin+" ->["+self.origin+"|"+self.destination+"]")
        elif(self.dir == "up"):
            print(self.destination+" connects to the top of " +
                  self.origin+"->["+self.destination+"/"+self.origin+"]")
        else:
            print(self.destination+" connects to the bottom of " +
                  self.origin+"->["+self.origin+"/"+self.destination+"]")


class TransitionRule:
    def __init__(self, origin, neighbor, bondDir, finalOrigin, finalNeighbor):
        self.origin = origin  # Origin-tile's label
        self.neighbor = neighbor  # Neighbor's label
        # Direction from origin to neighbor, or Direction of the Bond; it's a String.
        self.bondDir = bondDir
        self.finalOrigin = finalOrigin  # Origin-tile's final label/state
        self.finalNeighbor = finalNeighbor  # Neighbor's final label/state

    # Getters
    def returnOrigin(self):
        return self.origin

    def returnNeighbor(self):
        return self.neighbor

    def returnDir(self):
        return self.bondDir

    def returnFinalOrigin(self):
        return self.finalOrigin

    def returnFinalNeighbor(self):
        return self.finalNeighbor

    # Displayer
    def displayRule(self):
        if(self.bondDir == "left"):
            print("["+self.neighbor+"|"+self.origin+"]"" -> [" +
                  self.finalNeighbor+"|"+self.finalOrigin+"]; with "+self.origin+" as the origin.")
        elif(self.bondDir == "right"):
            print("["+self.origin+"|"+self.neighbor+"]"" -> [" +
                  self.finalOrigin+"|"+self.finalNeighbor+"]; with "+self.origin+" as the origin.")
        elif(self.bondDir == "up"):
            print("["+self.neighbor+"/"+self.origin+"]"" -> [" +
                  self.finalNeighbor+"/"+self.finalOrigin+"]; with "+self.origin+" as the origin.")
        else:
            print("["+self.origin+"/"+self.neighbor+"]"" -> [" +
                  self.finalOrigin+"/"+self.finalNeighbor+"]; with "+self.origin+" as the origin.")


def readxml(file):
    tree = ET.parse(file)
    treeroot = tree.getroot()

    AffinityRules = []  # Collection of Affinity Rules
    TransitionRules = []  # Collection of Transition Rules

    if(treeroot.tag == "SingleTile"):
        # Main: Setting BaseStateSet
        for state_tag in treeroot.findall('StateTypes/BaseStates/State'):
            label = state_tag.get('Label')
            color = state_tag.find('color').text
            tempState = BaseState(label, color)
            BaseStateSet.append(tempState)
        print("Base State Set:")
        for element in BaseStateSet:
            element.displayBasic()
        # Main: Setting TransitionStateSet
        for state_tag in treeroot.findall('StateTypes/TransitionStates/State'):
            label = state_tag.get('Label')
            color = state_tag.find('color').text
            tempState = BaseState(label, color)
            TransitionStateSet.append(tempState)
        print("Transition State Set:")
        for element in TransitionStateSet:
            element.displayBasic()

        # Main: Setting System Rules
        # Sub: Setting Affinity Rules
        for rule_tag in treeroot.findall('System/AffinityRules/Rule'):
            origin = rule_tag.get('State')
            for direction in rule_tag:
                dir = direction.tag
                destination = direction.text.replace("\"", "")
                tempRule = AffinityRule(origin, dir, destination)
                AffinityRules.append(tempRule)

        # Sub: Setting Transition Rules
        for rule_tag in treeroot.findall('System/TransitionRules/Rule'):
            origin = rule_tag.get('State')
            for info in rule_tag:
                dir = info.tag
                neighbor = info.get('Neighbor')
                finalOrigin = info.get('finalOrigin')
                finalNeighbor = info.get('finalNeighbor')
                tempRule = TransitionRule(
                    origin, neighbor, dir, finalOrigin, finalNeighbor)
                TransitionRules.append(tempRule)

        # Main: Displaying the System's Rules
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
        print("\n")
        # Main: Assigning Each Tile's Relevant Rules
        for base_state in BaseStateSet:
            tempLabel = base_state.returnLabel()
            for rule in AffinityRules:
                if(tempLabel == rule.returnOrigin()):
                    base_state.appendAffinity(rule)
            for rule in TransitionRules:
                if(tempLabel == rule.returnOrigin()):
                    base_state.appendTransition(rule)
        for transition_state in TransitionStateSet:
            tempLabel = transition_state.returnLabel()
            for rule in AffinityRules:
                if(tempLabel == rule.returnOrigin()):
                    transition_state.appendAffinity(rule)
            for rule in TransitionRules:
                if(tempLabel == rule.returnOrigin()):
                    transition_state.appendTransition(rule)
