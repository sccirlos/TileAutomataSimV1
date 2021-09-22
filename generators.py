import UniversalClasses as uc
import SaveFile

import math

red = "f03a47"
blue = "3f88c5"
green = "0ead69"
orange = "f39237"
black = "323031"
white = "DFE0E2"



# Must be passed an interger 
def genDoubleIndexStates(vLen):
    seedA = uc.State("SA", black)
    genSys = uc.System(1, [], [], [seedA], [], [], [], [])

    sqrtLen = math.ceil(math.sqrt(vLen))

    # Create States and add to lists

    for i in range(sqrtLen):
        # Little a states (Initial States)
        aState = uc.State(str(i) + "a", red)
        genSys.add_State(aState)
        genSys.add_Initial_State(aState)
        # Big A states
        bigAState = uc.State(str(i) + "A", red)
        genSys.add_State(bigAState)
        # A' (prime) states
        aPrime = uc.State(str(i) + "A'", red)
        genSys.add_State(aPrime)
        # B states (Initial States)
        bState = uc.State(str(i) + "B", blue)
        genSys.add_State(bState)
        genSys.add_Initial_State(bState)

    # Blank A and A' states
    singleA = uc.State("A", red)
    genSys.add_State(singleA)
    singleAPrime = uc.State("A'", red)
    genSys.add_State(singleAPrime)
    # Seed States
    genSys.add_State(seedA)
    seedB = uc.State("SB", black)
    #     seedB is an Initial State
    genSys.add_Initial_State(seedB)
    genSys.add_State(seedB)
    # B prime states
    Bprime = uc.State(str(sqrtLen - 1) + "B'", blue)
    genSys.add_State(Bprime)
    Bprime2 = uc.State(str(sqrtLen - 1) + "B''", blue)
    genSys.add_State(Bprime2)

    # Adding Affinity Rules
    #       Seed Affinities to start building
    affinityA0 = uc.AffinityRule("0a", "SA", "v", 1)
    genSys.add_affinity(affinityA0)
    affinityB0 = uc.AffinityRule("0B", "SB", "v", 1)
    genSys.add_affinity(affinityB0)
    affinitySeed = uc.AffinityRule("SA", "SB", "h", 1)
    genSys.add_affinity(affinitySeed)

    for i in range(sqrtLen - 1):
        # Affinity Rules to build each column
        affA = uc.AffinityRule(str(i + 1) + "a", str(i) + "a", "v", 1)
        genSys.add_affinity(affA)
        affB = uc.AffinityRule(str(i + 1) + "B", str(i) + "B", "v", 1)
        genSys.add_affinity(affB)
        # Affinity Rule to start the next section of the A column
        affGrowA = uc.AffinityRule("0a", str(i) + "A'", "v", 1)
        genSys.add_affinity(affGrowA)

    #       Affinity Rules to grow the next section of the B column
    affGrowB = uc.AffinityRule("0B", str(sqrtLen - 1) + "B'", "v", 1)
    genSys.add_affinity(affGrowB)

    # Transition Rules
    #   Transition for when the sections is complete
    trTop = uc.TransitionRule(
        str(sqrtLen - 1) + "a", str(sqrtLen - 1) + "B", "A'", str(sqrtLen - 1) + "B", "h")
    genSys.add_transition_rule(trTop)

    # Rule for starting propagation of A state
    AprimeProp = uc.TransitionRule(
        "A'", str(sqrtLen - 2) + "a", "A'", "A", "v")
    genSys.add_transition_rule(AprimeProp)

    # Rule for when A state reaches seed and marked as 0A
    trAseed = uc.TransitionRule("A", "SA", "0A", "SA", "v")
    genSys.add_transition_rule(trAseed)

    # Rule to allow B to transition to allow a string to print
    trAseed = uc.TransitionRule(
        "0B", str(sqrtLen - 1) + "B'", "0B", str(sqrtLen - 1) + "B''", "v")
    genSys.add_transition_rule(trAseed)

    for i in range(sqrtLen):
        # Rule for continued propagation of A state downward
        if i < sqrtLen - 2:
            Aprop = uc.TransitionRule("A", str(i) + "a", "A", "A", "v")
            genSys.add_transition_rule(Aprop)

        # Rule for A state reaches bottom of the column to increment
        if i < sqrtLen - 1:
            trIncA = uc.TransitionRule(
                "A", str(i) + "A'", str(i + 1) + "A", str(i) + "A'", "v")
            genSys.add_transition_rule(trIncA)

        # Rules for propagating the A index upward
        propUp = uc.TransitionRule(
            "A", str(i) + "A", str(i) + "A", str(i) + "A", "v")
        genSys.add_transition_rule(propUp)
        propUpPrime = uc.TransitionRule(
            "A'", str(i) + "A", str(i) + "A'", str(i) + "A", "v")
        genSys.add_transition_rule(propUpPrime)

        # Rule allowing B column to start the next section
        if i < sqrtLen - 1:
            trGrowB = uc.TransitionRule(str(
                i) + "A'", str(sqrtLen - 1) + "B", str(i) + "A'", str(sqrtLen - 1) + "B'", "h")
            genSys.add_transition_rule(trGrowB)

    return genSys


# Can be passed an interger or string (binary string)
def genSqrtBinString(value):
    if isinstance(value, int):
        value = bin(value)[2:]


    revValue = value[::-1]
    genSys = genDoubleIndexStates(len(value))

    sqrtLen = math.ceil(math.sqrt(len(value)))

    # Add Binary Symbol states
    state0 = uc.State("0", orange)
    state1 = uc.State("1", green)
    genSys.add_State(state0)
    genSys.add_State(state1)

    for i in range(sqrtLen):
        for j in range(sqrtLen):
            if i == sqrtLen - 1:
                labelB = str(j) + "B"
            elif j < sqrtLen - 1:
                labelB = str(j) + "B"
            else:
                labelB = str(j) + "B''"

            if j < sqrtLen - 1:
                labelA = str(i) + "A"
            else:
                labelA = str(i) + "A'"

            index = (i * sqrtLen) + j
            if index < len(value):
                symbol = str(revValue[index])
            else:
                symbol = "1"

            tr = uc.TransitionRule(labelA, labelB, labelA, symbol, "h")
            genSys.add_transition_rule(tr)

    return genSys


# Can be passed an interger or string (binary string)
def genSqrtBinCount(value):
    if isinstance(value, int):
        # Since the system has one column that is behind the start of the counter 
        # we subtract one to 


        # get the cieling of the log of the number
        # This tells us how long the string will be
        bits = math.ceil(math.log(value, 2))

        # Get the number we're counting up to 
        # The assembly stops at after overflow so we add one to the max count
        maxCount = 2**bits + 1
        start = maxCount - value
        startBin = bin(start)[2:]

        # Need to add leading 0s
        count0 = bits - len(startBin)
        lead0 = ""
        for i in range(count0):
            lead0 = lead0 + "0"


        value = lead0 + startBin

    sqrtLen = math.ceil(math.sqrt(len(value)))

    print("Length: ", value)

    #binString = format(value, "b")
    genSys = genSqrtBinString(value)

    # Add states for binary counter

    # New Initial States
    # State for indicating carry
    carry = uc.State("c", blue)
    genSys.add_State(carry)
    genSys.add_Initial_State(carry)

    # State for indicating no carry
    noCarry = uc.State("nc", red)
    genSys.add_State(noCarry)
    genSys.add_Initial_State(noCarry)

    ##
    incState = uc.State("+", black)
    genSys.add_State(incState)
    genSys.add_Initial_State(incState)

    northWall = uc.State("N", black)
    genSys.add_State(northWall)
    genSys.add_Initial_State(northWall)

    # Other States

    southWall = uc.State("S", black)
    genSys.add_State(southWall)

    zeroCarry = uc.State("0c", orange)
    genSys.add_State(zeroCarry)

    #<Rule Label1="N" Label2="2A'" Dir="v" Strength="1"></Rule>
    northAff = uc.AffinityRule("N", str(sqrtLen - 1) + "A'", "v")
    genSys.add_affinity(northAff)
    # <Rule Label1="SB" Label2="+" Dir="h" Strength="1"></Rule>
    incSeed = uc.AffinityRule("SB", "+", "h")
    genSys.add_affinity(incSeed)
    #        <Rule Label1="S" Label2="+" Dir="h" Strength="1"></Rule>
    incAff = uc.AffinityRule("S", "+", "h")
    genSys.add_affinity(incAff)
    #        <Rule Label1="c" Label2="+" Dir="v" Strength="1"></Rule>
    carInc = uc.AffinityRule("c", "+", "v")
    genSys.add_affinity(carInc)
    #        <Rule Label1="c" Label2="0c" Dir="v" Strength="1"></Rule>
    carryAff = uc.AffinityRule("c", "0c", "v")
    genSys.add_affinity(carryAff)
    #        <Rule Label1="nc" Label2="1" Dir="v" Strength="1"></Rule>
    nc1 = uc.AffinityRule("nc", "1", "v")
    genSys.add_affinity(nc1)
    #        <Rule Label1="nc" Label2="0" Dir="v" Strength="1"></Rule>
    nc0 = uc.AffinityRule("nc", "0", "v")
    genSys.add_affinity(nc0)

    # <Rule Label1="0" Label2="c" Label1Final="0" Label2Final="1" Dir="h"></Rule>
    carry0TR = uc.TransitionRule("0", "c", "0", "1", "h")
    genSys.add_transition_rule(carry0TR)
    # <Rule Label1="0" Label2="nc" Label1Final="0" Label2Final="0" Dir="h"></Rule>
    noCarry0TR = uc.TransitionRule("0", "nc", "0", "0", "h")
    genSys.add_transition_rule(noCarry0TR)
    # <Rule Label1="1" Label2="c" Label1Final="1" Label2Final="0c" Dir="h"></Rule>
    zeroCarryTR = uc.TransitionRule("1", "c", "1", "0c", "h")
    genSys.add_transition_rule(zeroCarryTR)
    # <Rule Label1="1" Label2="nc" Label1Final="1" Label2Final="1" Dir="h"></Rule>
    noCarry1TR = uc.TransitionRule("1", "nc", "1", "1", "h")
    genSys.add_transition_rule(noCarry1TR)
    # <Rule Label1="1" Label2="+" Label1Final="1" Label2Final="S" Dir="v"></Rule>
    next1TR = uc.TransitionRule("1", "+", "1", "S", "v")
    genSys.add_transition_rule(next1TR)
    # <Rule Label1="0" Label2="+" Label1Final="0" Label2Final="S" Dir="v"></Rule>
    next0TR = uc.TransitionRule("0", "+", "0", "S", "v")
    genSys.add_transition_rule(next0TR)
    # <Rule Label1="1" Label2="0c" Label1Final="1" Label2Final="0" Dir="v"></Rule>
    down1TR = uc.TransitionRule("1", "0c", "1", "0", "v")
    genSys.add_transition_rule(down1TR)
    # <Rule Label1="0" Label2="0c" Label1Final="0" Label2Final="0" Dir="v"></Rule>
    down0TR = uc.TransitionRule("0", "0c", "0", "0", "v")
    genSys.add_transition_rule(down0TR)

    return genSys


def genTripleIndexStates(vLen):
    seedA = uc.State("SA", black)
    genSys = uc.System(1, [], [], [seedA], [], [], [], [])

    cbrtLen = math.ceil(vLen**(1.0/3.0))

    for i in range(2 * cbrtLen):
        # Little a states (Initial States)
        aState = uc.State(str(i) + "a", red)
        genSys.add_State(aState)
        genSys.add_Initial_State(aState)
        # Little b states (Initial States)
        bState = uc.State(str(i) + "b", blue)
        genSys.add_State(bState)
        genSys.add_Initial_State(bState)

    for i in range(cbrtLen):
        # Big A states
        bigAState = uc.State(str(i) + "A", red)
        genSys.add_State(bigAState)
        # Base A states
        southAState = uc.State(str(i) + "As", red)
        genSys.add_State(southAState)
        # A' (prime) states
        bigAPrime = uc.State(str(i) + "A'", red)
        genSys.add_State(bigAPrime)
        # Big B states
        bigBState = uc.State(str(i) + "B", blue)
        genSys.add_State(bigBState)
        # Base B states
        southBState = uc.State(str(i) + "Bs", blue)
        genSys.add_State(southBState)
        # B prime states
        Bprime = uc.State(str(i) + "B'", blue)
        genSys.add_State(Bprime)
        Bprime2 = uc.State(str(i) + "B''", blue)
        genSys.add_State(Bprime2)
        # C states (Initial States)
        cState = uc.State(str(i) + "C", orange)
        genSys.add_State(cState)
        genSys.add_Initial_State(cState)
        # Base C states
        southCState = uc.State(str(i) + "Cs", orange)
        genSys.add_State(southCState)
        genSys.add_Initial_State(southCState)

    # Blank A and A' states
    singleA = uc.State("A", red)
    genSys.add_State(singleA)
    singleAPrime = uc.State("A'", red)
    genSys.add_State(singleAPrime)
    # Blank B and B' states
    singleB = uc.State("B", blue)
    genSys.add_State(singleB)
    BPrime = uc.State("B'", blue)
    genSys.add_State(BPrime)
    BPrime2 = uc.State("B''", blue)
    genSys.add_State(BPrime2)

    # Little a prime state
    aPrime = uc.State(str((2 * cbrtLen) - 1) + "a'", red)
    genSys.add_State(aPrime)
    # C prime states 
    Cprime = uc.State(str(cbrtLen - 1) + "C'", orange)
    genSys.add_State(Cprime)
    Cprime2 = uc.State(str(cbrtLen - 1) + "C''", orange)
    genSys.add_State(Cprime2)

    # Seed States
    genSys.add_State(seedA)
    #     seedB is an Initial State
    seedB = uc.State("SB", black)
    genSys.add_Initial_State(seedB)
    genSys.add_State(seedB)
    #     seedC is an Initial State
    seedC = uc.State("SC", black)
    genSys.add_Initial_State(seedC)
    genSys.add_State(seedC)


 

    # Adding Affinity Rules
    #       Seed Affinities to start building
    affinityA0 = uc.AffinityRule("0a", "SA", "v", 1)
    genSys.add_affinity(affinityA0)
    affinityB0 = uc.AffinityRule("0b", "SB", "v", 1)
    genSys.add_affinity(affinityB0)
    affinityB0 = uc.AffinityRule("0Cs", "SC", "v", 1)
    genSys.add_affinity(affinityB0)
    affinitySeed = uc.AffinityRule("SA", "SB", "h", 1)
    genSys.add_affinity(affinitySeed)
    affinitySeed2 = uc.AffinityRule("SB", "SC", "h", 1)
    genSys.add_affinity(affinitySeed2)

    for i in range((2 * cbrtLen) - 1):
        # Affinity Rules to build each column
        affA = uc.AffinityRule(str(i + 1) + "a", str(i) + "a", "v", 1)
        genSys.add_affinity(affA)
        affB = uc.AffinityRule(str(i + 1) + "b", str(i) + "b", "v", 1)
        genSys.add_affinity(affB)

    for i in range(cbrtLen - 1):
        affC = uc.AffinityRule(str(i) + "C", str(i) + "Cs", "v", 1)
        genSys.add_affinity(affC)
        affC = uc.AffinityRule(str(i + 1) + "Cs", str(i) + "C", "v", 1)
        genSys.add_affinity(affC)
        # Affinity Rule to start the next section of the A and B column
        affGrowA = uc.AffinityRule("0a", str(i) + "A'", "v", 1)
        genSys.add_affinity(affGrowA)
        affGrowB = uc.AffinityRule("0b", str(i) + "B'", "v", 1)
        genSys.add_affinity(affGrowB)

        affResetB = uc.AffinityRule("0b", str(cbrtLen - 1) + "B''", "v", 1)
        genSys.add_affinity(affResetB)

    # Last C state affinity
        affLC = uc.AffinityRule(str(cbrtLen - 1) + "C",
                                str(cbrtLen - 1) + "Cs", "v", 1)
        genSys.add_affinity(affLC)
        affGrowC = uc.AffinityRule("0Cs", str(cbrtLen - 1) + "C'", "v", 1)
        genSys.add_affinity(affGrowC)
    # State to continue column A
        affGrowA2 = uc.AffinityRule(
            "0a", str((2 * cbrtLen) - 1) + "a'", "v", 1)
        genSys.add_affinity(affGrowA2)

    # Transition Rules
    #   Transition for when the B and C columns of the sections are complete
    trBTop = uc.TransitionRule(str((2 * cbrtLen) - 1) + "b",
                               str(cbrtLen - 1) + "C", "B'", str(cbrtLen - 1) + "C", "h")
    genSys.add_transition_rule(trBTop)
    #   Transition for to start A propagation when B column has reached it's last index
    trATop = uc.TransitionRule(str((2 * cbrtLen) - 1) + "a", str(cbrtLen - 1) + "B'", "A'", str(cbrtLen - 1) + "B'", "h")
    genSys.add_transition_rule(trATop)
 

    # Rule for starting propagation of A state
    AprimeProp = uc.TransitionRule(
        "A'", str((2 * cbrtLen) - 2) + "a", "A'", "A", "v")
    genSys.add_transition_rule(AprimeProp)
    BprimeProp = uc.TransitionRule(
        "B'", str((2 * cbrtLen) - 2) + "b", "B'", "B", "v")
    genSys.add_transition_rule(BprimeProp)

    # Rule for when A/B state reaches seed or last B' and marked as 0As/0Bs
    trAseed = uc.TransitionRule("A", "SA", "0As", "SA", "v")
    genSys.add_transition_rule(trAseed)
    trBseed = uc.TransitionRule("B", "SB", "0Bs", "SB", "v")
    genSys.add_transition_rule(trBseed)
    trBreset = uc.TransitionRule("B", str(cbrtLen - 1) + "B''", "0Bs", str(cbrtLen - 1) + "B''", "v")
    genSys.add_transition_rule(trBreset)

    # Rule to allow B to transition to allow a string to print
    veriB2 = uc.TransitionRule("0Bs", str(
        cbrtLen - 1) + "B'", "0Bs", str(cbrtLen - 1) + "B''", "v")
    genSys.add_transition_rule(veriB2)
    veriC = uc.TransitionRule("0Cs", str(
        cbrtLen - 1) + "C'", "0Cs", str(cbrtLen - 1) + "C''", "v")
    genSys.add_transition_rule(veriC)

    for i in range(2 * cbrtLen - 1):
        # Rule for continued propagation of A state downward
        Aprop = uc.TransitionRule("A", str(i) + "a", "A", "A", "v")
        genSys.add_transition_rule(Aprop)
        Bprop = uc.TransitionRule("B", str(i) + "b", "B", "B", "v")
        genSys.add_transition_rule(Bprop)


    ApropPrime = uc.TransitionRule("A", str(2 * cbrtLen - 1) + "a'", "A" , "A", "v")
    genSys.add_transition_rule(ApropPrime)



    for i in range(cbrtLen):
        # Rule for A state reaches bottom of the column to increment
        if i < cbrtLen - 1:
            trIncA = uc.TransitionRule(
                "A", str(i) + "A'", str(i + 1) + "As", str(i) + "A'", "v")
            genSys.add_transition_rule(trIncA)
            trIncB = uc.TransitionRule(
                "B", str(i) + "B'", str(i + 1) + "Bs", str(i) + "B'", "v")
            genSys.add_transition_rule(trIncB)
            # Rule allowing B column to start the next section
            trGrowA = uc.TransitionRule(str((2 * cbrtLen) - 1) + "a", str(i) + "B'", str((2 * cbrtLen) - 1) + "a'", str(i) + "B'", "h")
            genSys.add_transition_rule(trGrowA)
            # Rule allowing B column to start the next section
            trGrowC = uc.TransitionRule(str(i) + "B'", str(cbrtLen - 1) + "C", str(i) + "B'", str(cbrtLen - 1) + "C'", "h")
            genSys.add_transition_rule(trGrowC)
            # Rule allowing B to start next section after A increments
            trGrowB = uc.TransitionRule(str(i) + "A'", str(cbrtLen - 1) + "B'", str(i) + "A'", str(cbrtLen - 1) + "B''", "h")
            genSys.add_transition_rule(trGrowB)


        # Rules for propagating the A index upward
        propUpA = uc.TransitionRule(
            "A", str(i) + "A", str(i) + "As", str(i) + "A", "v")
        genSys.add_transition_rule(propUpA)
        propUpAs = uc.TransitionRule(
            "A", str(i) + "As", str(i) + "A", str(i) + "As", "v")
        genSys.add_transition_rule(propUpAs)
        propUpPrimeA = uc.TransitionRule(
            "A'", str(i) + "As", str(i) + "A'", str(i) + "As", "v")
        genSys.add_transition_rule(propUpPrimeA)

        propUpB = uc.TransitionRule(
            "B", str(i) + "B", str(i) + "Bs", str(i) + "B", "v")
        genSys.add_transition_rule(propUpB)
        propUpAs = uc.TransitionRule(
            "B", str(i) + "Bs", str(i) + "B", str(i) + "Bs", "v")
        genSys.add_transition_rule(propUpAs)
        propUpPrimeB = uc.TransitionRule(
            "B'", str(i) + "Bs", str(i) + "B'", str(i) + "Bs", "v")
        genSys.add_transition_rule(propUpPrimeB)

        # Rule allowing B to start next section after A increments
        trGrowC = uc.TransitionRule(str(cbrtLen - 1) + "B''", str(cbrtLen - 1) + "C", str(cbrtLen - 1) + "B''", str(cbrtLen - 1) + "C'", "h")
        genSys.add_transition_rule(trGrowC)




    return genSys


def cbrtBinString(value):
    if isinstance(value, int):
        value = bin(value)[2:]


    revValue = value[::-1]
    vLen = len(value)
    genSys = genTripleIndexStates(vLen)

    cbrtLen = math.ceil(vLen**(1.0/3.0))

    genSys = genTripleIndexStates(vLen)

    # Add Binary Symbol states
    state0 = uc.State("0", black)
    state1 = uc.State("1", white)
    genSys.add_State(state0)
    genSys.add_State(state1)

    # Additional Index States are needed
    blankB = uc.State("Bx", blue)
    genSys.add_State(blankB)

    for i in range(cbrtLen):
        # States used to temp store values ND pulled from table
        stateC0 = uc.State(str(i) + "C0", black)
        genSys.add_State(stateC0)
        stateC1 = uc.State(str(i) + "C1", white)
        genSys.add_State(stateC1)

    # No new affinities are used

    # Transitions
    # STEP 1: ND select a value using A and B 
    # i will always be the index of the left state
    for i in range(cbrtLen):
        labelA = str(i) + "A"
        labelAPrime = str(i) + "A'"
        labelB2Prime = str(cbrtLen) + "B''"
        # j will always be index of right state
        for j in range(cbrtLen):
            labelB = str(j) + "B"
            labelBPrime = str(j) + "B'"

            for k in range(cbrtLen - 1):
                bitPos = (i * (cbrtLen**2)) + (j * cbrtLen) + k

                if bitPos >= len(value):
                    bit = 1
                else:
                    bit = revValue[bitPos]

                if bit == "0":
                    labelC = str(k) + "C0"
                elif bit == "1":
                    labelC = str(k) + "C1"
                else:
                    labelC = None
                    print("Not a binary string ")

                tr = uc.TransitionRule(labelA, labelB, labelA, labelC, "h")
                genSys.add_transition_rule(tr)

            # We know any transitions with a prime are on the last row of the section is automatacilly the last C
            lastBitPos = (i * (cbrtLen**2)) + (j * cbrtLen) + cbrtLen - 1

            if bitPos >= len(value):
                lastBit = 1
            else:
                lastBit = revValue[lastBitPos]

            if lastBit == "0":
                labelC = str(k) + "C0"
            elif lastBit == "1":
                labelC = str(k) + "C1"
            else:
                labelC = None
                print("Not a binary string ")

            trPrime = uc.TransitionRule(labelA, labelBPrime, labelA, labelC, "h")
            genSys.add_transition_rule(trPrime)



        ####### TR for last bits (STEP 1)
        lastBitPos = (i * (cbrtLen**2)) + (cbrtLen**2) - 1
        lastBit = revValue[lastBitPos]

        if lastBit == "0":
            labelC = str(k) + "C0"
        elif lastBit == "1":
            labelC = str(k) + "C1"

        tr2Prime = uc.TransitionRule(labelAPrime, labelB2Prime, labelAPrime, labelC, "h")
        genSys.add_transition_rule(tr2Prime)
                
        ###### STEP 2: Error Checking
        for i in range(cbrtLen): 
            labelC0 = str(i) + "C0"
            labelC1 = str(i) + "C1"

            for j in range(cbrtLen):
                labelC = str(j) + "C"

                # If the index matches we grabbed the right value 
                if i == j:
                    tr0 = uc.TransitionRule(labelC0, labelC, labelC0, "0", "h")
                    tr1 = uc.TransitionRule(labelC1, labelC, labelC1, "1", "h")
                else: 
                    # If the index is incorrect we transtion back to the blank assembly
                    tr0 = uc.TransitionRule(labelC0, labelC, "Bx", labelC, "h")
                    tr1 = uc.TransitionRule(labelC1, labelC, "Bx", labelC, "h")

                genSys.add_transition_rule(tr0)
                genSys.add_transition_rule(tr1)
                

            ##### TRs to reset the B tile
            labelB = str(i) + "B"
            labelBs = str(i) + "Bs"
            resetBtr = uc.TransitionRule("Bx", labelBs, labelB, labelBs, "v")
            genSys.add_transition_rule(resetBtr)

    return genSys


    



if __name__ == "__main__":
    flag = 0

    if(flag == 0):
        sys = cbrtBinString("100101011001010110010101010")

        states = sys.returnStates()



        SaveFile.main(sys, ["tripleTest.xml"])

    if(flag == 1):

        value = input("Please Enter an interger")
        sys = genSqrtBinCount(int(value))
        fileName = input("Please Enter file name: ")  + ".xml"

        SaveFile.main(sys, [fileName])
        print("Generated File: saved as ", fileName)









