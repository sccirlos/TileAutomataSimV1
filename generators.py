import UniversalClasses as uc 
import SaveFile
from components import increment_string, make_prime

import math

red = "f03a47"
blue = "3f88c5"
green = "0ead69"
orange = "f39237"
black = "323031"
white = "DFE0E2"


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
    trTop = uc.TransitionRule(str(sqrtLen - 1) + "a", str(sqrtLen - 1) + "B", "A'", str(sqrtLen - 1) + "B", "h")
    genSys.add_transition_rule(trTop)

    # Rule for starting propagation of A state
    AprimeProp = uc.TransitionRule("A'", str(sqrtLen - 2) + "a", "A'", "A", "v")
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

        # Rules for propagating the A index upward
        propUp = uc.TransitionRule("A", str(i) + "A", str(i) + "A", str(i) + "A", "v")
        genSys.add_transition_rule(propUp)
        propUpPrime = uc.TransitionRule("A'", str(i) + "A", str(i) + "A'", str(i) + "A", "v")
        genSys.add_transition_rule(propUpPrime)

        # Rule allowing B column to start the next section
        if i < sqrtLen - 1:
            trGrowB = uc.TransitionRule(str(i) + "A'", str(sqrtLen - 1) + "B", str(i) + "A'", str(sqrtLen - 1) + "B'", "h")
            genSys.add_transition_rule(trGrowB)

    return genSys


def genSqrtBinString(value):
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

def genSqrtBinCount(value):
    genSys = genSqrtBinString(value)

    # Add states for binary counter
    
    ## New Initial States
    ### State for indicating carry
    carry = uc.State("c", blue)
    genSys.add_State(carry)
    genSys.add_Initial_State(carry)

    ## State for indicating no carry
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
    northAff = uc.AffinityRule("N", "2A'", "v")
    genSys.add_affinity(northAff)
    #<Rule Label1="SB" Label2="+" Dir="h" Strength="1"></Rule>
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

    #<Rule Label1="0" Label2="c" Label1Final="0" Label2Final="1" Dir="h"></Rule>
    carry0TR = uc.TransitionRule("0", "c", "0", "1", "h")
    genSys.add_transition_rule(carry0TR)
    #<Rule Label1="0" Label2="nc" Label1Final="0" Label2Final="0" Dir="h"></Rule>
    noCarry0TR = uc.TransitionRule("0", "nc", "0", "0", "h")
    genSys.add_transition_rule(noCarry0TR)
    #<Rule Label1="1" Label2="c" Label1Final="1" Label2Final="0c" Dir="h"></Rule>
    zeroCarryTR = uc.TransitionRule("1", "c", "1", "0c", "h")
    genSys.add_transition_rule(zeroCarryTR)
    #<Rule Label1="1" Label2="nc" Label1Final="1" Label2Final="1" Dir="h"></Rule>
    noCarry1TR = uc.TransitionRule("1", "nc", "1", "1", "h")
    genSys.add_transition_rule(noCarry1TR)
    #<Rule Label1="1" Label2="+" Label1Final="1" Label2Final="S" Dir="v"></Rule>
    next1TR = uc.TransitionRule("1", "+", "1", "S", "v")
    genSys.add_transition_rule(next1TR)
    #<Rule Label1="0" Label2="+" Label1Final="0" Label2Final="S" Dir="v"></Rule>
    next0TR = uc.TransitionRule("0", "+", "0", "S", "v")
    genSys.add_transition_rule(next0TR)
    #<Rule Label1="1" Label2="0c" Label1Final="1" Label2Final="0" Dir="v"></Rule>
    down1TR = uc.TransitionRule("1", "0c", "1", "0", "v")
    genSys.add_transition_rule(down1TR)
    #<Rule Label1="0" Label2="0c" Label1Final="0" Label2Final="0" Dir="v"></Rule>
    down0TR = uc.TransitionRule("0", "0c", "0", "0", "v")
    genSys.add_transition_rule(down0TR)

    return genSys

class LinesGenerator:
    def __init__(self, line_len=None, num_st=None):
        
        self.seedA = uc.State("S", black)
        self.genSys = uc.System(1, [], [], [self.seedA], [], [], [], [])   
        self.num_states = num_st
        self.line_length = line_len
        if not line_len == None:
            self.bit_len = line_len.bit_length
        else:
            self.bit_len = None 
        pass

    
class NLength_LineGenerator(LinesGenerator):
    
    def __init__(self, line_len=None):
        self.reseed_states = []
        return super(LinesGenerator, self).__init__(line_len)  

    def generate_states(self):
        # New Initial States
        ## Add B0
        b0 = uc.State("B0", white)
        self.genSys.add_State(b0)
        self.genSys.add_Initial_State(b0)
        ## Add B'0
        bp0 = uc.State("B'0", white)
        self.genSys.add_State(bp0)
        
        
        for i in range(self.bit_len):
            
            pass

    def reseed_states(self):
        
        pass    


if __name__ == "__main__":
    #sys = genDoubleIndexStates(16)
    #SaveFile.main(sys, ["genTest16.xml"])

    #sys = genDoubleIndexStates(25)
    #SaveFile.main(sys, ["genTest25.xml"])

    #sys = genSqrtBinString("110010001")
    #SaveFile.main(sys, ["genTestString.xml"])

    #sys = genSqrtBinString("1110100101000101")
    #SaveFile.main(sys, ["genTestString16.xml"])

    #sys = genSqrtBinCount("110010001")
    #SaveFile.main(sys, ["genTestString.xml"])

    #tallSys = genDoubleIndexStates(100)
    #SaveFile.main(tallSys, ["tallSys.xml"])

    #sys = genSqrtBinCount("111010101")
    #SaveFile.main(sys, ["genTestCount.xml"])

    sys = genSqrtBinCount("110011100")
    SaveFile.main(sys, ["biggerTestCount.xml"])







