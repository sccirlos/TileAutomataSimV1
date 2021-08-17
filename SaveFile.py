from LoadFile import InitialStateSet
import xml.etree.ElementTree as ET

from general_TA_simulator import System
from UniversalClasses import State
from UniversalClasses import SeedAssemblyTile
from UniversalClasses import AffinityRule
from UniversalClasses import TransitionRule


def main(system):
    temp = system.get_temp()
    states = system.get_states()
    initial_states = system.get_initial_states()
    seed_assembly = system.get_seed_assembly()
    seed_states = system.get_seed_states()
    vertical_affinities = system.get_vertical_affinities()
    horizontal_affinities = system.get_horizontal_affinities()
    vertical_transitions = system.get_vertical_transition_rules()
    horizontal_transitions = system.get_horizontal_transition_rules()

    # Establish root and add temperature value
    root = ET.Element("System")
    root.set('Temp', temp)

    # Add all states used in the system
    all_states_tag = ET.Element("AllStates")
    root.append(all_states_tag)
    for state in states:
        label = state.returnLabel()
        color = state.returnColor()

        state_tag = ET.SubElement(all_states_tag, "State")
        state_tag.set('Label', label)
        state_tag.set('Color', color)

    # Add all inital states
    initial_states_tag = ET.Element("InitialStates")
    root.append(initial_states_tag)
    for state in initial_states:
        label = state.returnLabel()
        color = state.returnColor()

        state_tag = ET.SubElement(initial_states_tag, "State")
        state_tag.set('Label', label)
        state_tag.set('Color', color)

    # Add all seed states
    seed_states_tag = ET.Element("SeedStates")
    root.append(seed_states_tag)
    for state in seed_states:
        label = state.returnLabel()
        color = state.returnColor()

        state_tag = ET.SubElement(seed_states_tag, "State")
        state_tag.set('Label', label)
        state_tag.set('Color', color)

    # Add vertical transition rules
    vertical_transitions_tag = ET.Element("VerticalTransitions")
    root.append(vertical_transitions_tag)
    for rule in vertical_transitions:
        label1 = rule.returnLabel1()
        label2 = rule.returnLabel2()
        label1Final = rule.returnLabel1Final()
        label2Final = rule.returnLabel2Final()
        dir = rule.returnDir()

        rule_tag = ET.SubElement(vertical_transitions_tag, "Rule")
        rule_tag.set('Label1', label1)
        rule_tag.set('Label2', label2)
        rule_tag.set('Label1Final', label1Final)
        rule_tag.set('Label2Final', label2Final)
        rule_tag.set('Dir', dir)

    # Add horizontal transition rules
    horizontal_transitions_tag = ET.Element("HorizontalTransitions")
    root.append(horizontal_transitions_tag)
    for rule in horizontal_transitions:
        label1 = rule.returnLabel1()
        label2 = rule.returnLabel2()
        label1Final = rule.returnLabel1Final()
        label2Final = rule.returnLabel2Final()
        dir = rule.returnDir()

        rule_tag = ET.SubElement(horizontal_transitions_tag, "Rule")
        rule_tag.set('Label1', label1)
        rule_tag.set('Label2', label2)
        rule_tag.set('Label1Final', label1Final)
        rule_tag.set('Label2Final', label2Final)
        rule_tag.set('Dir', dir)

    # Add vertical affinity rules
    vertical_affinities_tag = ET.Element("VerticalAffinities")
    root.append(vertical_affinities_tag)
    for rule in vertical_affinities:
        label1 = rule.returnLabel1()
        label2 = rule.returnLabel2()
        dir = rule.returnDir()
        str = rule.returnStr()

        rule_tag = ET.SubElement(vertical_affinities_tag, "Rule")
        rule_tag.set('Label1', label1)
        rule_tag.set('Label2'. label2)
        rule_tag.set('Dir', dir)
        rule_tag.set("Strength", str)

    # Add horizontal affinity rules
    horizontal_affinities_tag = ET.Element("HorizontalAffinities")
    root.append(horizontal_affinities_tag)
    for rule in horizontal_affinities:
        label1 = rule.returnLabel1()
        label2 = rule.returnLabel2()
        dir = rule.returnDir()
        str = rule.returnStr()

        rule_tag = ET.SubElement(horizontal_affinities_tag, "Rule")
        rule_tag.set('Label1', label1)
        rule_tag.set('Label2', label2)
        rule_tag.set('Dir', dir)
        rule_tag.set("Strength", str)

    tree = ET.ElementTree(root)
    with open("WritingTest.xml", "wb") as file:
        tree.write(file)
