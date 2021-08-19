from os import stat
from PyQt5.QtWidgets import QFileDialog
import xml.etree.ElementTree as ET

from UniversalClasses import State
from UniversalClasses import SeedAssemblyTile
from UniversalClasses import AffinityRule
from UniversalClasses import TransitionRule

# System's Affinity Rules
VerticalAffinityRules = []
HorizontalAffinityRules = []
# System's Transition Rules
VerticalTransitionRules = []
HorizontalTransitionRules = []
# Note: Assembly mode is when the system is seeded by an assembly, while SingleTile mode is when it's seeded by a single tile.
# Note2: SeedAssembly is a basic representation of the assembly; it's not actually built.
# The assembler will build the real seed assembly after the XML is loaded.
SeedAssembly = []  # Used in Assembly mode; the assembly used as a seed.
SeedStateSet = []  # Used in SingleTile mode; States that were marked as potential seeds
# States marked as initial states; states that float around the system looking to attach to something.
InitialStateSet = []
CompleteStateSet = []  # All states in the system


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
        # Read and record the system's Temp
        for system_tag in treeroot.findall('System'):
            # Temp doesn't like being an implied global variable lmao
            global Temp
            Temp = system_tag.get("Temp")
        # Read and record affinity rules
        for rule_tag in treeroot.findall('System/AffinityRules/Rule'):
            label1 = rule_tag.get("Label1")  # Rule's label1
            label2 = rule_tag.get("Label2")  # Rule's label2
            dir = rule_tag.get("Dir")  # Rule's dir
            strength = rule_tag.get("Strength")  # Rule's strength

            # Create temp Rule object
            tempRule = AffinityRule(label1, label2, dir, strength)
            # Attach the rule to either HorizontalAffinityRules...
            if(dir == "h"):
                HorizontalAffinityRules.append(tempRule)
            # or VerticalAffinityRules.
            else:
                VerticalAffinityRules.append(tempRule)
        # Read and record transition rules
        for rule_tag in treeroot.findall('System/TransitionRules/Rule'):
            label1 = rule_tag.get("Label1")
            label2 = rule_tag.get("Label2")
            label1Final = rule_tag.get("Label1Final")
            label2Final = rule_tag.get("Label2Final")
            dir = rule_tag.get("Dir")

            tempRule = TransitionRule(
                label1, label2, label1Final, label2Final, dir)
            # Following the same logic from AffinityRules:
            if(dir == "h"):
                HorizontalTransitionRules.append(tempRule)
            else:
                VerticalAffinityRules.append(tempRule)
    # Note: Add an elif if the seed is an assembly

    # Checking Temp:
    print("System Temperature: "+Temp)

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
    print("Horizontal Affinity Rules:")
    if(HorizontalAffinityRules == []):
        print("\tNONE")
    else:
        for rule in HorizontalAffinityRules:
            label1 = rule.returnLabel1()
            label2 = rule.returnLabel2()
            dir = rule.returnDir()
            strength = rule.returnStr()

            print("\t- ["+label1+"/"+label2+"]; Bond Strength: "+strength)
    print("Vertical Affinity Rules:")
    if(VerticalAffinityRules == []):
        print("\tNONE")
    else:
        for rule in VerticalAffinityRules:
            label1 = rule.returnLabel1()
            label2 = rule.returnLabel2()
            dir = rule.returnDir()
            strength = rule.returnStr()

            print("\t- ["+label1+"/"+label2+"]; Bond Strength: "+strength)

    print("Horizontal Transition Rules:")
    if(HorizontalTransitionRules == []):
        print("\tNONE")
    else:
        for rule in HorizontalTransitionRules:
            label1 = rule.returnLabel1()
            label2 = rule.returnLabel2()
            label1Final = rule.returnLabel1Final()
            label2Final = rule.returnLabel2Final()
            dir = rule.returnDir()

            print("\t- ["+label1+"|"+label2+"] -> [" +
                  label1Final+"|"+label2Final+"]")
    print("Vertical Transition Rules:")
    if(VerticalTransitionRules == []):
        print("\tNONE")
    else:
        for rule in VerticalTransitionRules:
            label1 = rule.returnLabel1()
            label2 = rule.returnLabel2()
            label1Final = rule.returnLabel1Final()
            label2Final = rule.returnLabel2Final()
            dir = rule.returnDir()

            print("\t- ["+label1+"/"+label2+"] -> [" +
                  label1Final+"/"+label2Final+"]")
    print("Check complete!")
