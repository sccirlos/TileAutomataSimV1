from UniversalClasses import System, State, AffinityRule, TransitionRule
import SaveFile

# Global Variables
seed_states = []
initial_states = []
complete_states = []
vertical_affinities = []
horizontal_affinities = []
vertical_transitions = []
horizontal_transitions = []

# Figure Key:
# A = Stickman Standing
# B = Stickman Waving
# C = Stickman Running
# D = Stickman Handstand


def build_A(string, string_position):
    # Main: Construct Linker for New Macro
    if(string_position == 0):  # If this figure is the 1st on the string...
        # Attach the figure to the root
        tempRule = AffinityRule('X', 'A0', 'h', 1)
        horizontal_affinities.append(tempRule)
    else:  # Otherwise, attach it to the previous figure.
        # Note: '*' represents terminal tile of a figure macro.
        # End of figure before new one
        label1 = string[string_position-1] + str(string_position-1) + '*'
        label2 = 'A' + str(string_position)
        tempRule = AffinityRule(label1, label2, 'h', 1)
        horizontal_affinities.append(tempRule)
    # Now do what is needed for both of the above scenarios.
    label = 'A' + str(string_position)
    tempState = State(label, '00ff00')
    initial_states.append(tempState)
    complete_states.append(tempState)

    # Main: Construct Figure Macro
    # Sub: Grass for Figure
    tempLabels = ["A!", "A@", "A#", "A*"]
    # TO-DO from here: Make the grass and finish the rest of the body
    for label in tempLabels:
        tempState = State(label, '00ff00')
        initial_states.append(tempState)
        complete_states.append(tempState)
    # Connect to the 'seed' of the Macro (A)
    horizontal_affinities.append(AffinityRule('A', tempLabels[0], 'h', 1))
    # Connect the 'internal' grass tiles together.

    # Sub: Left Leg
    # First, handle state rules
    tempState = State('ALL1', '000000')
    initial_states.append(tempState)
    complete_states.append(tempState)
    tempState = State('ALL2', 'ffffff')
    initial_states.append(tempState)
    complete_states.append(tempState)
    tempState = State('ALL3', '000000')
    initial_states.append(tempState)
    complete_states.append(tempState)
    # Second, handle affinity rules
    label2 = 'A' + str(string_position)
    tempRule = AffinityRule('ALL1', label2, 'v', 1)
    vertical_affinities.append(tempRule)
    tempRule = AffinityRule('ALL2', 'ALL1', 'v', 1)
    vertical_affinities.append(tempRule)
    tempRule = AffinityRule('ALL2', 'ALL3', 'h', 1)
    horizontal_affinities.append(tempRule)

    # Sub: Right Leg; Reflection of Left Leg basically.


def main(input_string=None):
    string_position = 0

    # If the user doesn't input a string, make a random string of figures.
    if(input_string == None):
        pass
    # Otherwise, make the string of figures the user wants.
    else:
        # Create Seed
        tempState = State('X', '00ff00')  # Green
        seed_states.append(tempState)

        # Add to the System depending on what character is read from the input
        for letter in input_string:
            if(letter == 'A'):
                build_A(input_string, string_position)
            elif(letter == 'B'):
                pass
            elif(letter == 'C'):
                pass
            elif(letter == 'D'):
                pass
            string_position += 1  # Increment string position
    tempSystem = System(1, complete_states, initial_states, seed_states, vertical_affinities,
                        horizontal_affinities, vertical_transitions, horizontal_transitions)
    SaveFile.main(tempSystem, ["FGTest.xml"])


main('A')
