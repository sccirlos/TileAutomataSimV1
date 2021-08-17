from os import stat
from PyQt5.QtWidgets import QFileDialog
import xml.etree.ElementTree as ET

AffinityRules = []  # System's Affinity Rules
TransitionRules = []  # System's Transition Rules
# Note: Assembly mode is when the system is seeded by an assembly, while SingleTile mode is when it's seeded by a single tile.
SeedAssembly = []  # Used in Assembly mode; the assembly used as a seed.
SeedStateSet = []  # Used in SingleTile mode; States that were marked as potential seeds
# States marked as initial states; states that float around the system looking to attach to something.
InitialStateSet = []
CompleteStateSet = []  # All states in the system


class State:
    def __init__(self, label, color):
        self.label = label
        self.color = color

    # Getters
    def returnLabel(self):
        return self.label

    def returnColor(self):
        return self.color


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


def readxml(file):
    tree = ET.parse(file)
    treeroot = tree.getroot()

    # If the system has a single tile for its seed:
    if(treeroot.tag == "SingleTile"):
        # Read and record the system's states
        for state_tag in treeroot.findall('StateTypes/State'):
            label = state_tag.get("Label")  # State's label
            color = state_tag.find("color").text  # State's color
            # State's initial status as a string
            initialStatusString = state_tag.find("initial").text
            # State's seed status as a string
            seedStatusString = state_tag.find("seed").text

            # Create a temp State object
            tempState = State(label, color)
            # If the state is an initial state, add it to the list of inital states.
            if(initialStatusString == "true"):
                InitialStateSet.append(tempState)
            # If the state is a seed state, add it to the list of potential seeds.
            if(seedStatusString == "true"):
                SeedStateSet.append(tempState)
            # After those 2 checks, add this state to CompleteStateSet
            CompleteStateSet.append(tempState)
        # Read and record affinity rules
        for rule_tag in treeroot.findall('System/AffinityRules/Rule'):
            label1 = rule_tag.get("Label1")  # Rule's label1
            label2 = rule_tag.get("Label2")  # Rule's label2
            dir = rule_tag.get("Dir")  # Rule's dir
            strength = rule_tag.get("Strength")  # Rule's strength

            print(label1)  # Error check here
            # Create temp Rule object
            tempRule = AffinityRule(label1, label2, dir, strength)
            AffinityRules.append(tempRule)
        # Read and record transition rules
        for rule_tag in treeroot.findall('System/TransitionRules/Rule'):
            label1 = rule_tag.get("Label1")
            label2 = rule_tag.get("Label2")
            label1Final = rule_tag.get("Label1Final")
            label2Final = rule_tag.get("Label2Final")
            dir = rule_tag.get("Dir")

            tempRule = TransitionRule(
                label1, label2, label1Final, label2Final, dir)
            TransitionRules.append(tempRule)

    # Checking States:
    print("All States Used:")
    for state in CompleteStateSet:
        stateLabel = state.returnLabel()
        stateColor = state.returnColor()
        print("\t-Label: "+stateLabel+"; Color: "+stateColor)
    print("Initial States:")
    for state in InitialStateSet:
        stateLabel = state.returnLabel()
        stateColor = state.returnColor()
        print("\t-Label: "+stateLabel+"; Color: "+stateColor)
    print("States that can be used as a seed:")
    for state in SeedStateSet:
        stateLabel = state.returnLabel()
        stateColor = state.returnColor()
        print("\t-Label: "+stateLabel+"; Color: "+stateColor)

    # Checking Rules
    print("Affinity Rules:")
    for rule in AffinityRules:
        label1 = rule.returnLabel1()
        label2 = rule.returnLabel2()
        dir = rule.returnDir()
        strength = rule.returnStr()

        if(dir == "h"):
            print("\t- ["+label1+"|"+label2+"]; Bond Strength: "+strength)
        else:
            print("\t- ["+label1+"/"+label2+"]; Bond Strength: "+strength)
    print("Transition Rules:")
    for rule in TransitionRules:
        label1 = rule.returnLabel1()
        label2 = rule.returnLabel2()
        label1Final = rule.returnLabel1Final()
        label2Final = rule.returnLabel2Final()
        dir = rule.returnDir()

        if(dir == "h"):
            print("\t- ["+label1+"|"+label2+"] -> [" +
                  label1Final+"|"+label2Final+"]")
        else:
            print("\t- ["+label1+"/"+label2+"] -> [" +
                  label1Final+"/"+label2Final+"]")
    print("Check complete!")
