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

    # Record System Temp
    global Temp
    Temp = treeroot.get("Temp")

    # Record All States
    for state_tag in treeroot.find("AllStates/State"):
        label = state_tag.get("Label")
        color = state_tag.get("Color")
        print("Label: "+label+"; Color: "+color)

        tempState = State(label, color)
        CompleteStateSet.append(tempState)

    # Record Initial States
    for state_tag in treeroot.find("InitialStates/State"):
        label = state_tag.get("Label")
        color = state_tag.get("Color")

        tempState = State(label, color)
        InitialStateSet.append(tempState)

    # Record Seed States
    for state_tag in treeroot.find("SeedStates/State"):
        label = state_tag.get("Label")
        color = state_tag.get("Color")

        tempState = State(label, color)
        SeedStateSet.append(tempState)

    # Record Vertical Transitions
    if(treeroot.find("VerticalTransitions/Rule") != None):
        for rule_tag in treeroot.find("VerticalTransitions/Rule"):
            label1 = rule_tag.get("Label1")
            label2 = rule_tag.get("Label2")
            label1Final = rule_tag.get("Label1Final")
            label2Final = rule_tag.get("Label2Final")

            tempRule = TransitionRule(label1, label2, label1Final, label2Final)
            VerticalTransitionRules.append(tempRule)

    # Record Horizontal Transitions
    if(treeroot.find("HorizontalTransitions/Rule") != None):
        for rule_tag in treeroot.find("HorizontalTransitions/Rule"):
            label1 = rule_tag.get("Label1")
            label2 = rule_tag.get("Label2")
            label1Final = rule_tag("Label1Final")
            label2Final = rule_tag("Label2Final")

            tempRule = TransitionRule(label1, label2, label1Final, label2Final)
            HorizontalTransitionRules.append(tempRule)

    # Record Vertical Affinities
    if(treeroot.find("VerticalAffinities/Rule") != None):
        for rule_tag in treeroot.find("Vertical Affinities/Rule"):
            label1 = rule_tag.get("Label1")
            label2 = rule_tag.get("Label2")
            strength = rule_tag.get("Strength")

            tempRule = AffinityRule(label1, label2, strength)
            VerticalAffinityRules.append(tempRule)

    # Record Horizontal Affinities
    if(treeroot.find("HorizontalAffinities/Rule") != None):
        for rule_tag in treeroot.find("HorizontalAffinities/Rule"):
            label1 = rule_tag.get("Label1")
            label2 = rule_tag.get("Label2")
            strength = rule_tag.get("Strength")

            tempRule = AffinityRule(label1, label2, strength)
            HorizontalAffinityRules.append(tempRule)

    print(CompleteStateSet)
    print(InitialStateSet)
    print(SeedStateSet)
