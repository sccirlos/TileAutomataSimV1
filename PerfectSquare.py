from UniversalClasses import System, State, AffinityRule, TransitionRule
import SaveFile


# Row Generator
# Note: Actual Row Length = length + 1
def simple_row_generator(length=0):
    symbols = ['@', '#', '$', '!']
    loop_counter = 0

    seed_states = []
    initial_states = []
    complete_states = []
    vertical_affinities = []
    horizontal_affinities = []
    vertical_transitions = []
    horizontal_transitions = []

    if(length > 3):
        # For each sub-system...
        for symbol in symbols:
            if(loop_counter == 0):  # System #0; Row
                # Record Seed, Initial, and Complete States
                for i in range(length):
                    tempState = State(str(i+1)+symbol, 'ffffff')
                    if(i == 0):  # If it's the first tile, make it the seed.
                        seed_states.append(tempState)
                    else:  # Otherwise, make it an initial state.
                        initial_states.append(tempState)
                    complete_states.append(tempState)
                # Record necessary affinity rules
                for i in range(length-1):
                    tempRule = AffinityRule(
                        str(i+1)+symbol, str(i+2)+symbol, 'h', 1)
                    horizontal_affinities.append(tempRule)
            elif(loop_counter == 1):  # System #1; Column
                # Record States again
                for i in range(length):
                    tempState = State(str(i+1)+symbol, 'ffffff')
                    initial_states.append(tempState)
                    complete_states.append(tempState)
                # Establish affinity rules again
                for i in range(length-2):
                    tempRule = AffinityRule(
                        str(i+1)+symbol, str(i+2)+symbol, 'v', 1)
                    vertical_affinities.append(tempRule)
                # Connect System #1 to #0
                tempRule = AffinityRule(
                    str(length)+symbols[0], "1"+symbol, 'v', 1)
                vertical_affinities.append(tempRule)
            elif(loop_counter == 2):  # System #2; Row
                # Record States again
                for i in range(length):
                    tempState = State(str(i+1)+symbol, 'ffffff')
                    initial_states.append(tempState)
                    complete_states.append(tempState)
                # Establish affinity rules again
                for i in range(length-2):
                    tempRule = AffinityRule(
                        str(i+2)+symbol, str(i+1)+symbol, 'h', 1)
                    horizontal_affinities.append(tempRule)
                # Connect System #2 to #1
                tempRule = AffinityRule(
                    "1"+symbol, str(length-1) + symbols[1], 'h', 1)
                horizontal_affinities.append(tempRule)
            else:
                # If we're at System #3, then we're just making filler squares.
                tempState = State(symbol, 'ffff00')
                initial_states.append(tempState)
                complete_states.append(tempState)
                tempState = State(symbol+'\'', '00ffff')
                initial_states.append(tempState)
                complete_states.append(tempState)
                tempRule1 = AffinityRule(symbol, symbol, 'v', 1)
                tempRule2 = AffinityRule(symbol, symbol+'\'', 'h', 1)
                tempRule3 = AffinityRule(symbol+'\'', symbol+'\'', 'h', 1)
                vertical_affinities.append(tempRule1)
                horizontal_affinities.append(tempRule2)
                horizontal_affinities.append(tempRule3)
                # Connect System #3 to #2
                tempRule = AffinityRule(
                    symbol, str(length-1)+symbols[2], 'v', 1)
                vertical_affinities.append(tempRule)
            # Increment loop counter.
            loop_counter += 1
        tempSystem = System(1, complete_states, initial_states, seed_states, vertical_affinities,
                            horizontal_affinities, vertical_transitions, horizontal_transitions)
        SaveFile.main(tempSystem, ["PStest.xml"])


simple_row_generator(25)
