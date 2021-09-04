import UniversalClasses as uc 
import SaveFile

import math

red = "f03a47"
blue = "3f88c5"
green = "0ead69"
orange = "f39237"
black = "323031"
white = "DFE0E2"


def genDoubleLU(value, base):
    genSys = uc.System(1, [], [], [], [], [], [], [])

    vLen = len(value)
    sqrtLen = math.ceil(math.sqrt(vLen))

    # Add Symbol States
    for i in range(base):
        symState = uc.State(str(i), white)
        genSys.add_State(symState)

    # Create States and add to lists
    aStates = []
    aPrimes = []
    bigAStates = []
    bStates = []

    for i in range(sqrtLen):
        # Little a states (Initial States)
        aStates.append(uc.State(str(i) + "a", red))
        genSys.add_State(aStates[i])
        genSys.add_Initial_State(aStates[i])
        # Big A states
        bigAStates.append(uc.State(str(i) + "A", red))
        genSys.add_State(bigAStates[i])
        # A' (prime) states 
        aPrimes.append(uc.State(str(i) + "a'", red))
        genSys.add_State(aPrimes[i])
        # B states (Initial States)
        bStates.append(uc.State(str(i) + "B", blue))
        genSys.add_State(bStates[i])
        genSys.add_Initial_State(aStates[i])

    # Blank A and A' states
    singleA = uc.State("A", red)
    genSys.add_State(singleA)
    singleAPrime = uc.State("A'", red)
    genSys.add_State(singleAPrime)
    # Seed States
    seedA = uc.State("SA", black)
    genSys.add_State(seedA)
    seedB = uc.State("SB", black)
    #     seedB is an Initial State
    genSys.add_Initial_State(seedB)
    genSys.add_State(seedB)
    # B prime states 
    Bprime = uc.State(str(sqrtLen) + "B'", blue)
    genSys.add_State(Bprime)
    Bprime2 = uc.State(str(sqrtLen) + "B''", blue)
    genSys.add_State(Bprime2)

    # Adding Affinity Rules
    #       Seed Affinities to start building
    affinityA0 = uc.AffinityRule("0a", "SA", "v", 1)
    genSys.add_affinity(affinityA0)
    affinityB0 = uc.AffinityRule("0B", "SB", "v", 1)
    genSys.add_affinity(affinityB0)
    affinitySeed = uc.AffinityRule("SA", "SB", "h", 1)
    genSys.add_affinity(affinitySeed)

    for i in range(sqrtLen):
        if i < sqrtLen - 1:
            # Affinity Rules to build each column
            affA = uc.AffinityRule(str(i) + "a", str(i + 1) + "a", "v", 1)
            genSys.add_affinity(affA)
            affB = uc.AffinityRule(str(i) + "B", str(i + 1) + "B", "v", 1)
            genSys.add_affinity(affB)
            # Affinity Rule to start the next section of the A column
            affGrowA = uc.AffinityRule("0a", str(i) + "A'", "v", 1)
            genSys.add_affinity(affGrowA)


    #       Affinity Rules to grow the next section of the B column
    affGrowB = uc.AffinityRule("0B", str(sqrtLen) + "B''", "v", 1)
    genSys.add_affinity(affGrowB)

    # Transition Rules
    #   Transition for when the sections is complete
    trTop = uc.TransitionRule(str(sqrtLen) + "a", str(sqrtLen) + "B", "A'", str(sqrtLen) + "B", "h")
    genSys.add_transition_rule(trTop)

    # Rule for starting propagation of A state
    AprimeProp = uc.TransitionRule("A'", str(sqrtLen - 1) + "a", "A'", "A", "v")
    genSys.add_transition_rule(AprimeProp)

    # Rule for when A state reaches seed and marked as 0A
    trAseed = uc.TransitionRule("A", "SA", "0A", "SA", "v")
    genSys.add_transition_rule(trAseed)

    # Rule to allow B to transition to allow a string to print
    trAseed = uc.TransitionRule("0B", str(sqrtLen - 1) + "B'", "0B", str(sqrtLen - 1) + "B''", "v")
    genSys.add_transition_rule(trAseed)

    for i in range(sqrtLen):
        # Rule for continued propagation of A state downward
        if i < sqrtLen - 2:
            Aprop = uc.TransitionRule("A", str(i) + "a", "A", "A", "v")
            genSys.add_transition_rule(Aprop)

        # Rule for A state reaches bottom of the column to increment
        if i < sqrtLen - 1:
            trIncA = uc.TransitionRule("A", str(i) + "A'", str(i + 1) + "A", str(i) + "A'", "v")
            genSys.add_transition_rule(trIncA)

        # Rules for propagating the index upward
        propUp = uc.TransitionRule("A", str(i) + "A", str(i) + "A", str(i) + "A", "v")
        genSys.add_transition_rule(propUp)
        propUpPrime = uc.TransitionRule("A'", str(i) + "A", str(i) + "A'", str(i) + "A", "v")
        genSys.add_transition_rule(propUpPrime)

        # Rule allowing B column to start the next section
        if i < sqrtLen - 1:
            trGrowB = uc.TransitionRule(str(i) + "A'", str(sqrtLen - 1) + "B", str(i) + "A'", str(sqrtLen - 1) + "B'", "h")
            genSys.add_transition_rule(trGrowB)

        return genSys


if __name__ == "__main__":
    sys = genDoubleLU("110010001", 2)
    SaveFile.main(sys, "genTest")







