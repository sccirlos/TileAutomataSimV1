from generators import genSqrtBinCount
import UniversalClasses as uc
import SaveFile

import math

red = "f03a47"
blue = "3f88c5"
green = "0ead69"
orange = "f39237"
black = "323031"
white = "DFE0E2"


def genQuadIndexStates(vLen):
    rt4Len = math.ceil(vLen**(1.0/4.0))

    seedA = uc.State("SA", black)
    genSys = uc.System(1, [], [], [seedA], [], [], [], [])

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
    #     seedD is an Initial State
    seedD = uc.State("SD", black)
    genSys.add_Initial_State(seedD)
    genSys.add_State(seedD)

    # Blank A and A' states
    singleA = uc.State("A", red)
    genSys.add_State(singleA)
    genSys.add_Initial_State(singleA)
    singleAPrime = uc.State("A'", red)
    genSys.add_State(singleAPrime)
    genSys.add_Initial_State(singleAPrime)
    # Blank B and B' states
    singleB = uc.State("B", blue)
    genSys.add_State(singleB)
    genSys.add_Initial_State(singleB)
    BPrime = uc.State("B'", blue)
    genSys.add_State(BPrime)
    genSys.add_Initial_State(BPrime)
    BPrime2 = uc.State("B''", blue)
    genSys.add_State(BPrime2)
    # Blank C and C' states
    singleC = uc.State("C", orange)
    genSys.add_State(singleC)
    genSys.add_Initial_State(singleC)
    singleCPrime = uc.State("C'", orange)
    genSys.add_State(singleCPrime)
    genSys.add_Initial_State(singleCPrime)


    # Large Letter States
    for i in range(rt4Len):
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
        # Base C states
        southCState = uc.State(str(i) + "Cs", orange)
        genSys.add_State(southCState)
        # C prime states
        Cprime = uc.State(str(i) + "C'", orange)
        genSys.add_State(Cprime)
        Cprime2 = uc.State(str(i) + "C''", orange)
        genSys.add_State(Cprime2)
        # D states (Initial States)
        dState = uc.State(str(i) + "D", green)
        genSys.add_State(dState)
        genSys.add_Initial_State(dState)
        # Base D states
        southDState = uc.State(str(i) + "Ds", green)
        genSys.add_State(southDState)
        genSys.add_Initial_State(southDState)

        # C prime states
    
    Dprime = uc.State(str(rt4Len - 1) + "D'", green)
    genSys.add_State(Dprime)

    ### Affinity Rules
    #       Seed Affinities to start building seed row and attach first tile of D column
    affinityD0 = uc.AffinityRule("0Ds", "SD", "v", 1)
    genSys.add_affinity(affinityD0)
    affinitySeed = uc.AffinityRule("SA", "SB", "h", 1)
    genSys.add_affinity(affinitySeed)
    affinitySeed2 = uc.AffinityRule("SB", "SC", "h", 1)
    genSys.add_affinity(affinitySeed2)
    affinitySeed3 = uc.AffinityRule("SC", "SD", "h", 1)
    genSys.add_affinity(affinitySeed3)

    # Affinities to build D column
    for i in range(rt4Len - 1):
        affD = uc.AffinityRule(str(i) + "D", str(i) + "Ds", "v", 1)
        genSys.add_affinity(affD)
        affDs = uc.AffinityRule(str(i + 1) + "Ds", str(i) + "D", "v", 1)
        genSys.add_affinity(affDs)

    affLD = uc.AffinityRule(str(rt4Len - 1) + "D", str(rt4Len - 1) + "Ds", "v", 1)
    genSys.add_affinity(affLD)

    # The last state of the D column allows for C' to attach to the left 
    affLD = uc.AffinityRule("C'", str(rt4Len - 1) + "D", "h", 1)
    genSys.add_affinity(affLD)
    # C prime allows for the C states to attach below
    affCPrime = uc.AffinityRule("C'", "C", "v", 1)
    genSys.add_affinity(affCPrime)
    affCDown = uc.AffinityRule("C", "C", "v", 1)
    genSys.add_affinity(affCDown)

    # The last state of the C column allows for B' to attach to the left 
    affLC = uc.AffinityRule("B'", str(rt4Len - 1) + "C'", "h", 1)
    genSys.add_affinity(affLC)
    # B prime allows for the B states to attach below
    affBPrime = uc.AffinityRule("B'", "B", "v", 1)
    genSys.add_affinity(affBPrime)
    affBDown = uc.AffinityRule("B", "B", "v", 1)
    genSys.add_affinity(affBDown)

    # The last state of the B column allows for A' to attach to the left 
    affLB = uc.AffinityRule("A'", str(rt4Len - 1) + "B'", "h", 1)
    genSys.add_affinity(affLB)
    # B prime allows for the B states to attach below
    affAPrime = uc.AffinityRule("A'", "A", "v", 1)
    genSys.add_affinity(affAPrime)
    affADown = uc.AffinityRule("A", "A", "v", 1)
    genSys.add_affinity(affADown)

    # Affinity for D column to grow
    affDgrow = uc.AffinityRule("0Ds", str(rt4Len - 1) + "D'", "v", 1)
    genSys.add_affinity(affDgrow)

    ### Transitions
    # Rule for when A/B/C state reaches seed and marked as 0As/0Bs
    trAseed = uc.TransitionRule("A", "SA", "0As", "SA", "v")
    genSys.add_transition_rule(trAseed)
    trBseed = uc.TransitionRule("B", "SB", "0Bs", "SB", "v")
    genSys.add_transition_rule(trBseed)
    trCseed = uc.TransitionRule("C", "SC", "0Cs", "SC", "v")
    genSys.add_transition_rule(trCseed)

    for i in range(rt4Len):
        iA = str(i) + "A"
        iB = str(i) + "B"
        iC = str(i) + "C"
        # Rules for propagating the A/B/C index upward
        propUpA = uc.TransitionRule("A", iA, iA + "s", iA, "v")
        genSys.add_transition_rule(propUpA)
        propUpAs = uc.TransitionRule("A", iA + "s", iA, iA + "s", "v")
        genSys.add_transition_rule(propUpAs)
        propUpPrimeA = uc.TransitionRule("A'", iA + "s", iA + "'", iA + "s", "v")
        genSys.add_transition_rule(propUpPrimeA)

        propUpB = uc.TransitionRule("B", iB, iB + "s", iB, "v")
        genSys.add_transition_rule(propUpB)
        propUpBs = uc.TransitionRule("B", iB + "s", iB, iB + "s", "v")
        genSys.add_transition_rule(propUpBs)
        propUpPrimeB = uc.TransitionRule("B'", iB + "s", iB + "'", iB + "s", "v")
        genSys.add_transition_rule(propUpPrimeB)

        propUpC = uc.TransitionRule("C", iC, iC + "s", iC, "v")
        genSys.add_transition_rule(propUpC)
        propUpCs = uc.TransitionRule("C", iC + "s", iC, iC + "s", "v")
        genSys.add_transition_rule(propUpCs)
        propUpPrimeC = uc.TransitionRule("C'", iC + "s", iC + "'", iC + "s", "v")
        genSys.add_transition_rule(propUpPrimeC)


    rtCP = str(rt4Len - 1) + "C'"
    rtCP2 = str(rt4Len - 1) + "C''"
    rtBP = str(rt4Len - 1) + "B'"
    rtBP2 = str(rt4Len - 1) + "B''"
    
    for i in range(rt4Len - 1):
        iAP = str(i) + "A'"
        iBP = str(i) + "B'"
        iCP = str(i) + "C'"

        i1As = str(i + 1) + "As"
        i1Bs = str(i + 1) + "Bs"
        i1Cs = str(i + 1) + "Cs"



        # Transition Rule for when C reach the top of the column
        growCD = uc.TransitionRule(iCP, str(rt4Len - 1) + "D", iCP, str(rt4Len - 1) + "D'", "h")
        genSys.add_transition_rule(growCD)

        growBC = uc.TransitionRule(iBP, rtCP, iBP, rtCP2, "h")
        genSys.add_transition_rule(growBC)

        growAB = uc.TransitionRule(iAP, rtBP, iAP, rtBP2, "h")
        genSys.add_transition_rule(growAB)

        # Transitions to increment A/B/C column from not the seed
        trAinc = uc.TransitionRule("A", iAP, i1As, iAP, "v")
        genSys.add_transition_rule(trAinc)
        trBinc = uc.TransitionRule("B", iBP, i1Bs, iBP, "v")
        genSys.add_transition_rule(trBinc)
        trCinc = uc.TransitionRule("C", iCP, i1Cs, iCP, "v")
        genSys.add_transition_rule(trCinc)

    # Once the B column complete and transition the C column to double prime D can start growing again
    resetCD = uc.TransitionRule(rtCP2, str(rt4Len - 1) + "D", rtCP2, str(rt4Len - 1) + "D'", "h")
    genSys.add_transition_rule(resetCD)   

    # We need to add a special case TR for when the C column is building down and see C double prime
    resetC2 = uc.TransitionRule("C", rtCP2, "0Cs", rtCP2, "v")
    genSys.add_transition_rule(resetC2)
    resetB2 = uc.TransitionRule("B", rtBP2, "0Bs", rtBP2, "v")
    genSys.add_transition_rule(resetB2)

    # B double prime transitions C prime to C double prime
    doublePrimeProp = uc.TransitionRule(rtBP2, rtCP, rtBP2, rtCP2, "h")
    genSys.add_transition_rule(doublePrimeProp)

    return genSys



if __name__ == "__main__":
    sys = genQuadIndexStates(81)
    SaveFile.main(sys, ["quadTest.xml"])

