import UniversalClasses as uc
import SaveFile
from components import increment_string, make_prime,  split_nonprime_label, split_prime_label,  check_is_prime, split_label_pnp, transition_to_forward, check_nums_same, check_A_greater, check_A_less, transition_to_backward,  make_not_prime

import math

red = "f03a47"
blue = "3f88c5"
green = "0ead69"
orange = "f39237"
black = "323031"
white = "DFE0E2"
grey = "9EA9A4"
light_blue = "C2DCFE"


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

class LinesGenerator:
    def __init__(self, line_len=None, num_st=None):

        self.seedA = uc.State("S", black)
        self.genSys = uc.System(1, [], [], [self.seedA], [], [], [], [])
        self.num_states = num_st
        self.line_length = line_len
        if not line_len == None:
            self.bit_len = line_len.bit_length()
        else:
            self.bit_len = None
        self.genSys.add_State(self.seedA)


class Freezing_NLength_LineGenerator(LinesGenerator):

    def __init__(self, line_len=None):
        super().__init__(line_len)
        self.reseed_states = []
        self.reseed_state_nums = []
        self.smallest_reseed = None

        self.generate_states()
        self.add_affinities()
        self.add_transitions()



    def generate_states(self):
        # Call Generate Reseed States Function
        self.reseed_states_gen()

        # New Initial States
        ## Add B0

        b0 = uc.State("B0", white)
        self.genSys.add_State(b0)
        self.genSys.add_Initial_State(b0)

        # New Transition States

        if self.line_length > 2:
            bp0 = uc.State("B'0", light_blue)
            self.genSys.add_State(bp0)

            f0 = uc.State("F0", red)
            self.genSys.add_State(f0)


            for i in range(1, self.bit_len):
                if i == (self.bit_len - 1):
                    bState = uc.State("B" + str(i), blue)
                    self.genSys.add_State(bState)
                else:
                    #Add back states that are not B0
                    bState = uc.State("B" + str(i), blue)
                    self.genSys.add_State(bState)
                    ## Add forward states
                    fState = uc.State("F" + str(i), red)
                    self.genSys.add_State(fState)
                    ## Add forward prime states
                    fpState = uc.State("F'" + str(i), orange)
                    self.genSys.add_State(fpState)

    #Used to generate the states that are reseeded
    def reseed_states_gen(self):
        ## The bit length will give one more than the highest power hence subtract 1
        bl = self.bit_len - 1
        ## line length minus seed
        num = self.line_length - 1
        rs = []

        ## Subtracts 2 to bit length from the line length to get the reseed states, decrementing bit length each time and appending if the remaining line length is greater than or equal to 0
        while num > 0:
            if num - 2**bl >= 0:

                if not(num - 2**bl == 0):
                    rState = uc.State("R" + str(bl), grey)
                    self.genSys.add_State(rState)
                    rs.append("R" + str(bl))
                    self.reseed_states.append("R" + str(bl))

                ## If 2^bl immediately equals the line length - 1 then add the only non prime reseed states
                elif math.log2(self.line_length - 1).is_integer():
                    rState = uc.State("R" + str(bl), grey)
                    self.genSys.add_State(rState)
                    rs.append("R" + str(bl))
                    self.reseed_states.append("R" + str(bl))


                rpState = uc.State("R'" + str(bl), grey)
                self.reseed_states.append("R'" + str(bl))

                if rpState.get_label() == "R'1":
                    rs.append("R" + str(bl))
                    r1State = uc.State("R" + str(bl), grey)
                    self.genSys.add_State(r1State)
                    self.reseed_states.append("R" + str(bl))

                rs.append("R'" + str(bl))
                #Now append R' State after checking if it is R'1
                self.genSys.add_State(rpState)
                self.reseed_state_nums.append(bl)


                num = num - 2**bl
            bl = bl - 1
        self.smallest_reseed = rs[-1]
        return

    # Adding Affinities helper methods
    #Actually in use
    def add_reseed_affinities_v2(self):
        # Adds affinity for Seed to first reseed
        rs = self.reseed_states.copy()
        aff = uc.AffinityRule("S", rs[0], "h")
        self.genSys.add_affinity(aff)


        rs_len = len(rs) - 1
        for i in range(rs_len):
            # Adds affinity between reseeds in order eg (R3, R'3), (R'3, R1)
            if (i + 1) <= rs_len:
                aff = uc.AffinityRule(rs[i], rs[i+1], "h")
                self.genSys.add_affinity(aff)

            # Adds affinities between non primes and B'0
            if not ("'" in rs[i] and i > 0):
                aff = uc.AffinityRule(rs[i], "B'0", "h")
                self.genSys.add_affinity(aff)

                if not (rs[i] == "R1"):
                    aff = uc.AffinityRule(rs[i], rs[i], "h")
                    self.genSys.add_affinity(aff)

            elif not(i == rs_len):
                aff = uc.AffinityRule(rs[i], "B0", "h")
                self.genSys.add_affinity(aff)

    def add_affinities_v2(self):
        # Const states

        CONST_STATES = self.genSys.return_list_of_state_labels()
        dynamic_states = self.genSys.return_list_of_state_labels()
        # West affinities to pop
        west_affs_to_complete = self.genSys.return_list_of_state_labels()
        west_affs_completed = []
        west_affs_to_complete.remove(self.smallest_reseed)
        west_affs_to_complete.remove("B'0")
        west_affs_to_complete.remove("B0")

        # West affinities completed
        # A list of forward states
        # a list of backward states
        # A list of Reseed no prime
        # list of reseed primes
        #
        # copy of state list
        bl = self.bit_len
        for i in range(0, bl):
            for j, wa in enumerate(west_affs_to_complete):
                if not (wa == "S"):
                    wa_num = split_label_pnp(wa)[1]

                    if "R'" in wa:
                        rwa_next = self.reseed_state_nums.index(wa_num) + 1
                        if i < self.reseed_state_nums[rwa_next]:
                            brp = "B" + str(i)
                            Aff = uc.AffinityRule(wa, brp, "h")
                            self.genSys.add_affinity(Aff)

                            frp = "F" + str(i)
                            Aff = uc.AffinityRule(wa, frp, "h")
                            self.genSys.add_affinity(Aff)

                        elif i == self.reseed_state_nums[rwa_next] and not(i == 0):
                            brp = "B" + str(i)
                            Aff = uc.AffinityRule(wa, brp, "h")
                            self.genSys.add_affinity(Aff)
                        else:
                            comp = west_affs_to_complete.pop(j)
                            west_affs_completed.append(comp)

                    elif "R" in wa:
                        if i <= wa_num and not(i == 0):
                            brp = "B" + str(i)
                            Aff = uc.AffinityRule(wa, brp, "h")
                            self.genSys.add_affinity(Aff)
                        if i == 0 and wa == self.reseed_states[0]:

                            brp = "B'0"
                            Aff = uc.AffinityRule(wa, brp, "h")
                            self.genSys.add_affinity(Aff)


                    elif "B" in wa:
                        if not(i == 0):
                            if i == wa_num and i > 1:
                                brp = "B" + str(i)
                                Aff = uc.AffinityRule(wa, brp, "h")
                                self.genSys.add_affinity(Aff)
                            # If i is one less than wa_num
                            elif (i - 1) == wa_num and wa_num >= 1:
                                brp = "B" + str(i)
                                Aff = uc.AffinityRule(brp, wa,"h")
                                self.genSys.add_affinity(Aff)



                    elif "F'" in wa:
                        if i <= wa_num:
                            b = "B" + str(i)
                            Aff = uc.AffinityRule(wa, b, "h")
                            self.genSys.add_affinity(Aff)
                            if i < wa_num:
                                f = "F" + str(i)
                                Aff = uc.AffinityRule(wa, f, "h")
                                self.genSys.add_affinity(Aff)


                    elif "F" in wa:
                        if i == 0:
                            bp = "B'" + str(i)
                            Aff = uc.AffinityRule(wa, bp, "h")
                            self.genSys.add_affinity(Aff)
                        elif i <= (wa_num + 1) and not(wa == 'F0' or wa == 'F1'):
                            if i > 1:
                                b = "B" + str(i)
                                Aff = uc.AffinityRule(wa, b, "h")
                                self.genSys.add_affinity(Aff)
                            elif i == 1 and not(wa == 'F0' or wa == 'F1'):
                                b = "B" + str(i)
                                Aff = uc.AffinityRule(wa, b, "h")
                                self.genSys.add_affinity(Aff)

                        elif wa == 'F1':
                            b = "B2"
                            Aff = uc.AffinityRule(wa, b, "h")
                            self.genSys.add_affinity(Aff)

                        if i > 0:

                            if wa_num > 1 and i > 1:
                                if wa_num == i:
                                    fp = "F'" + str(i)
                                    Aff = uc.AffinityRule(wa, fp, "h")
                                    self.genSys.add_affinity(Aff)
                                    if i > 1 and wa_num >= i:
                                            f = "F" + str(i)
                                            Aff = uc.AffinityRule(wa, f, "h")
                                            self.genSys.add_affinity(Aff)
                            elif wa_num == 1:
                                fp = "F'1"
                                Aff = uc.AffinityRule(wa, fp, "h")
                                self.genSys.add_affinity(Aff)

                else:
                    b = "B" + str(i)
                    Aff = uc.AffinityRule(wa, b, "h")
                    self.genSys.add_affinity(Aff)
                    if i < (bl -1):
                        f = "F" + str(i)
                        Aff = uc.AffinityRule(wa, f, "h")
                        self.genSys.add_affinity(Aff)



    def add_affinities(self):
        b0Aff = uc.AffinityRule("S","B0", "h")
        self.genSys.add_affinity(b0Aff)

        if self.line_length > 2:

            b0f0Aff = uc.AffinityRule("F0","B0", "h")
            self.genSys.add_affinity(b0f0Aff)

            bp0f0Aff = uc.AffinityRule("F0","B'0", "h")
            self.genSys.add_affinity(bp0f0Aff)

            b1bp0Aff = uc.AffinityRule("B1","B'0", "h")
            self.genSys.add_affinity(b1bp0Aff)

        self.add_reseed_affinities_v2()
        self.add_affinities_v2()
        return

    def add_seed_transitions(self, labelA, labelB):
        if labelA == "S":
            split_b = split_label_pnp(labelB) #returns a list where element 0 is the state type and element 1 is the number [str, int]
            if split_b[1] == self.reseed_state_nums[0]:
                labelB_Final = self.reseed_states[0]

                tr = uc.TransitionRule(labelA, labelB, labelA, labelB_Final, "h")
                if not (self.genSys.checkHorizontalTransitionsList(tr)):
                    if not(labelB == labelB_Final):
                        self.genSys.add_transition_rule(tr)


            else:
                labelB_Final = transition_to_forward(labelB)

                tr = uc.TransitionRule(labelA, labelB, labelA, labelB_Final, "h")
                if not (self.genSys.checkHorizontalTransitionsList(tr)):
                    if not(labelB == labelB_Final):
                        self.genSys.add_transition_rule(tr)

    def check_next_reseed(self, r_state):
        # This method takes an r_state and returns a pair of the next reseed state and the number of reseed states left
        r_split = split_label_pnp(r_state)
        r_split_index = self.reseed_state_nums.index(r_split[1])
        remain_len = len(self.reseed_state_nums[r_split_index:])
        if r_split_index == (len(self.reseed_state_nums) - 1):
            return (-1, -1, -1)
        next_r_num = self.reseed_state_nums[r_split_index + 1]
        next_r_state_i = self.reseed_states.index(r_state) + 1
        next_r_state = self.reseed_states[next_r_state_i]
        r_pair = (next_r_num, remain_len, next_r_state)
        return r_pair

    def add_reseed_transitions_v2(self, labelA, labelB):
        if "R'" in labelA:
            ## Split the R' label to get num and split B label to get num
            labelA_r_split = split_label_pnp(labelA)
            labelB_split = split_label_pnp(labelB)
            next_r = self.check_next_reseed(labelA)
            if next_r == (-1, -1, -1):
                return
            #Check Bs
            if "B" in labelB and not("'" in labelB):
                # If the B num is less than the next reseed number
                if labelB_split[1] < next_r[0]:
                    if next_r[1] > 0:
                        labelB_Final = transition_to_forward(labelB)
                        tr = uc.TransitionRule(labelA, labelB, labelA, labelB_Final, "h")
                        if not (self.genSys.checkHorizontalTransitionsList(tr)):
                            self.genSys.add_transition_rule(tr)
                    elif next_r[1] == 0:
                        return
                ## if the B num is equal to the next reseed number
                elif labelB_split[1] == next_r[0]:
                    if labelB_split[1] == 0:
                        labelB_Final = "R'" + str(next_r[0])
                        tr = uc.TransitionRule(labelA, labelB, labelA, labelB_Final, "h")
                        if not (self.genSys.checkHorizontalTransitionsList(tr)):
                            self.genSys.add_transition_rule(tr)
                    else:
                        labelB_Final = next_r[2]
                        tr = uc.TransitionRule(labelA, labelB, labelA, labelB_Final, "h")
                        if not (self.genSys.checkHorizontalTransitionsList(tr)):
                            self.genSys.add_transition_rule(tr)

            elif "F" in labelB and not("'" in labelB):
                pass

        # Transitions R, B'0 to R, R' and R, B to R, R
        elif "R" in labelA and not("R" in labelB):
            if "B'" in labelB:
                labelB_Final = make_prime(labelA)
            else:
                labelB_Final = labelA
            tr = uc.TransitionRule(labelA, labelB, labelA, labelB_Final, "h")
            if not (self.genSys.checkHorizontalTransitionsList(tr)):
                self.genSys.add_transition_rule(tr)


    def add_forward_transition(self, labelA, labelB):
        states = self.genSys.return_list_of_state_labels()

        if "F'" in labelA:
            if check_A_greater(labelA, labelB):
                labelB_Final = transition_to_forward(labelB)
                tr = uc.TransitionRule(labelA, labelB, labelA, labelB_Final, "h")
                if not (self.genSys.checkHorizontalTransitionsList(tr)):
                    if not(labelB == labelB_Final):
                        self.genSys.add_transition_rule(tr)

        elif "F" in labelA and labelA in states:
            if "B'" in labelB:
                if check_A_greater(labelA, labelB):
                    labelB_Final = make_prime(labelA)
                    tr = uc.TransitionRule(labelA, labelB, labelA, labelB_Final, "h")
                    if not (self.genSys.checkHorizontalTransitionsList(tr)):
                        self.genSys.add_transition_rule(tr)
            elif "B" in labelB:
                if check_A_greater(labelA, labelB):
                    labelB_Final = labelA
                    tr = uc.TransitionRule(labelA, labelB, labelA, labelB_Final, "h")
                    if not (self.genSys.checkHorizontalTransitionsList(tr)):
                        self.genSys.add_transition_rule(tr)
                if check_nums_same(labelA, labelB) and not(labelB == "B0"):
                    labelB_Final = labelA
                    tr = uc.TransitionRule(labelA, labelB, labelA, labelB_Final, "h")
                    if not (self.genSys.checkHorizontalTransitionsList(tr)):
                        if not(labelB == labelB_Final):
                            self.genSys.add_transition_rule(tr)


    def add_back_transition(self, labelA, labelB):
        if "R" in labelA or "S" in labelA:
            return
        elif "B" in labelA:
            return
        elif "B" in labelB:
            if check_nums_same(labelA, labelB):
                labelA_Final = increment_string(labelA)
                labelA_Final = transition_to_backward(labelA_Final)
                labelA_Final = make_not_prime(labelA_Final)

                if not (labelB == "B0") and check_is_prime(labelA):
                    tr = uc.TransitionRule(labelA, labelB, labelA_Final, labelB, "h")
                    if not (self.genSys.checkHorizontalTransitionsList(tr)):
                        self.genSys.add_transition_rule(tr)

            elif check_A_less(labelA, labelB):
                labelA_Final = labelB
                tr = uc.TransitionRule(labelA, labelB, labelA_Final, labelB, "h")
                if not (self.genSys.checkHorizontalTransitionsList(tr)):
                    self.genSys.add_transition_rule(tr)

    def add_transitions(self):
        #tr = uc.TransitionRule(labelA, labelB, labelA_Final, labelB_Final, "h")
        #self.genSys.add_transition_rule(tr)
        seed = "S"
        b0 = "B0"
        bp0 = "B'0"
        f0 = "F0"
        line_len = self.line_length
        if line_len > 1:
            if line_len == 2:
                tr = uc.TransitionRule(seed, b0, seed, "R'0", "h")
                self.genSys.add_transition_rule(tr)

            elif line_len > 2:
                tr = uc.TransitionRule(seed, b0, seed, f0, "h")
                self.genSys.add_transition_rule(tr)

                tr = uc.TransitionRule(f0, b0, f0, bp0, "h")
                self.genSys.add_transition_rule(tr)

                tr = uc.TransitionRule(f0, bp0, "B1", bp0, "h")
                self.genSys.add_transition_rule(tr)

                if line_len > 4:
                    labelA = seed
                    labelB = "B1"


                    self.add_seed_transitions(labelA, labelB)
                    affinities_list = self.genSys.returnHorizontalAffinityList()


                    for aff in affinities_list:
                        l1 = aff.returnLabel1()
                        l2 = aff.returnLabel2()

                        self.add_seed_transitions(l1, l2)
                        self.add_reseed_transitions_v2(l1, l2)
                        self.add_forward_transition(l1, l2)
                        self.add_back_transition(l1, l2)

        transitions = self.genSys.returnHorizontalTransitionList()




        #transition_rules = self.genSys.returnHorizontalTransitionDict()
        #transition_rules_check_14(transition_rules)
        # B0 F0
        # B0 transitions
        # B'0 transitions

        return

    def return_gen_sys(self):
        return self.genSys
class NonFreezing_Lines_Generator:
    def __init__(self, base_number, digits_number):
        seed = self.add_seed(base_number)
        self.genSys = uc.System(
            1, [], [], [seed], [], [], [], [], [], [])
        self.base_number = base_number
        self.digits_number = digits_number

    def add_seed(self, base_number):
        label = str(base_number) + "i0"
        seed = uc.State(label, light_blue)
        return seed

    def add_states(self):
        # Add states
        #Add empty State
        label = "-"
        self.genSys.add_State(label)
        self.genSys.add_Initial_State(label)

        #Add X State
        label = "X"
        self.genSys.add_State(label)

        #Add Copy State
        label = "C"
        self.genSys.add_State(label)

        #Add Barrow State
        label = "B"
        self.genSys.add_State(label)

        #Add + State
        #Add r State

        for i in range(1, self.digits_number):
            label = str(self.base_number) + "i" + str(i)
            self.genSys.add_State(label)
            self.genSys.add_Initial_State(label)

        for i in range(self.base_number):
            label = str(i)
            rest_label = str(i) + "r"
            self.genSys.add_State(label)
            self.genSys.add_State(rest_label)

            if not(i == 0):
                just_carried_label = str(i) + "+"
                self.genSys.add_State(just_carried_label)

    def add_affinities(self):
        inital_states = self.genSys.returnInitialStates()



if __name__ == "__main__":
    #sys = genDoubleIndexStates(16)
    #SaveFile.main(sys, ["genTest16.xml"])

#if __name__ == "__main__":
    #flag = 0

    #if(flag == 0):



        #states = sys.returnStates()



        #SaveFile.main(sys, ["tripleTest.xml"])

    #if(flag == 1):
        #value = input("Please Enter an interger")
        #sys = genSqrtBinCount(int(value))
        #fileName = input("Please Enter file name: ")  + ".xml"

        #SaveFile.main(sys, [fileName])
        #print("Generated File: saved as ", fileName)


    """ sys = genSqrtBinCount("110011100")
    SaveFile.main(sys, ["biggerTestCount.xml"]) """
    line_len = 100
    linesSys = Freezing_NLength_LineGenerator(line_len)

    sys = linesSys.return_gen_sys()

    str(line_len)
    filename = f'XML_Files/test{line_len}.xml'.format()

    SaveFile.main(sys, [filename])
