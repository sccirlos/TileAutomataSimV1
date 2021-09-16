import UniversalClasses as uc 
import SaveFile
from components import increment_string, make_prime, states_test_14, states_test_27, affinities_test_14, split_nonprime_label, split_prime_label, affinities_test_17, affinities_test_9, check_is_prime, split_label_pnp

import math

red = "f03a47"
blue = "3f88c5"
green = "0ead69"
orange = "f39237"
black = "323031"
white = "DFE0E2"
grey = "9EA9A4"
light_blue = "C2DCFE"

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
            self.bit_len = line_len.bit_length()
        else:
            self.bit_len = None 
        self.genSys.add_State(self.seedA)

    
class NLength_LineGenerator(LinesGenerator):
    
    def __init__(self, line_len=None):
        super().__init__(line_len)
        self.reseed_states = []
        self.reseed_state_nums = []
        self.smallest_reseed = None
        self.affinities_by_type = [["Seed Affinities"], ["Self Affinities"], ["Self Prime Affinities"], ["Prime b0 f0 Affinities"], ["Back Walk Affinities"], ["Forward Walk Affinities"]]
        self.generate_states()
        self.add_affinities()
         

    def generate_states(self):
        # Call Generate Reseed States Function
        self.reseed_states_gen()
        
        # New Initial States
        ## Add B0
        
        b0 = uc.State("B0", white)
        self.genSys.add_State(b0)
        self.genSys.add_Initial_State(b0)
        
        # New Transition States
        ## Add B'0
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
                
        print("States Are: ")
        st = self.genSys.return_list_of_state_labels()
        sta = self.genSys.returnStates()
        #states_test_14(st)
        #states_test_27(st)
        for s in sta:
            print(s.get_label())
        

    def reseed_states_gen(self):
        # Generate Reseed States
        ## The bit length will give one more than the highest power hence subtract 1
        bl = self.bit_len - 1
        ## line length minus seed
        num = self.line_length - 1
        rs = []
        
        ## Subtracts number 
        while num > 0:
            
            if num - 2**bl >= 0:
                
                if not(num - 2**bl == 0):
                    rState = uc.State("R" + str(bl), grey)
                    self.genSys.add_State(rState)
                    rs.append("R" + str(bl))
                    self.reseed_states.append("R" + str(bl))
                    
                    
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
        print("Smallest Reseed: " + rs[-1])
        return  
            
    # Adding Affinities helper methods 
    ## Check if label attaches to Seed and create      
    def add_seed_affinity(self, aff_label):
        if aff_label == "S":
            return
        if not("'" in aff_label):
            if aff_label[0] == "R":
                if int(aff_label[1:]) == (self.bit_len - 1):
                    Aff = uc.AffinityRule("S", aff_label, "h")
                    self.genSys.add_affinity(Aff)
                    self.affinities_by_type[0].append(("S", aff_label))
                elif math.log2(self.line_length - 1).is_integer():
                    Aff = uc.AffinityRule("S", aff_label, "h")
                    self.genSys.add_affinity(Aff)   
            else:
                Aff = uc.AffinityRule("S", aff_label, "h")
                self.genSys.add_affinity(Aff)  
                self.affinities_by_type[0].append(("S", aff_label))

    ## Check if label attaches to self and create                      
    def add_self_affinity(self, aff_label):
        if "'" in aff_label or aff_label == "S":
            return
        elif aff_label[1] == "0":
            return
        elif aff_label[1] == "1":
            return
        else:
            Aff = uc.AffinityRule(aff_label, aff_label, "h")
            self.genSys.add_affinity(Aff)
            self.affinities_by_type[1].append((aff_label, aff_label))
            
    ## Check if label attaches to self prime and create
    def add_self_prime_affinity(self, aff_label):
        if aff_label == "S" or "'" in aff_label:
            return
        elif aff_label[1] == "0":
            return
        elif aff_label[0] == "B":
            return
        else:
            l2 = make_prime(aff_label)
            Aff = uc.AffinityRule(aff_label, l2, "h")
            self.genSys.add_affinity(Aff)
            self.affinities_by_type[2].append((aff_label, l2))
            
    ## Check if label is prime and attaches to b0, create
    ## must check if R' is last reseed        
    def add_prime_to_b0_f0_affinity(self, aff_label):
        if aff_label == "S":
            return
        if "'" in aff_label:
            if aff_label[0] == "B" or aff_label == self.smallest_reseed:
                return
            else:
                Aff = uc.AffinityRule(aff_label, "B0", "h")
                self.genSys.add_affinity(Aff)
                self.affinities_by_type[3].append((aff_label, "B0"))
                
                Aff = uc.AffinityRule(aff_label, "F0", "h")
                self.genSys.add_affinity(Aff)
                self.affinities_by_type[3].append((aff_label, "F0"))

    def add_bp0_affinities(self, label):
        if label == "F0":
            Aff = uc.AffinityRule(label, "B'0", "h")
            self.genSys.add_affinity(Aff)
            
        elif label == "B1":
            Aff = uc.AffinityRule(label, "B'0", "h")
            self.genSys.add_affinity(Aff)  
             
        elif not ("'" in label and label == "S"):
            if not (label[0] == "B" and label == self.smallest_reseed):
                Aff = uc.AffinityRule(label, "B'0", "h")
                self.genSys.add_affinity(Aff)

    def add_reseed_prime_to_nextReseed_affinities(self, label):
        
        if label == self.smallest_reseed:
            ## Make R'0 attach to second to last reseed
            if len(self.reseed_states) >= 3 and self.smallest_reseed == "R'0":
                Aff = uc.AffinityRule(self.reseed_states[-2], label, "h")
                self.genSys.add_affinity(Aff)   
            
                
        # If prime and if next reseed state is not R'0
        elif "R'" in label:
            l_index = self.reseed_states.index(label)
            if len(self.reseed_states) -3 >= l_index:
                Aff = uc.AffinityRule(label, self.reseed_states[l_index + 1],"h")
                self.genSys.add_affinity(Aff)   
                
    def add_reseed_affinities_v2(self):        
        rs = self.reseed_states.copy()
        aff = uc.AffinityRule("S", rs[0], "h")
        self.genSys.add_affinity(aff)    
        rs_len = len(rs) - 1
        for i in range(rs_len):
            if (i + 1) <= rs_len:
                aff = uc.AffinityRule(rs[i], rs[i+1], "h")
                self.genSys.add_affinity(aff)
                print(f'( {rs[i]}, {rs[i+1]} )')
            if not (rs[i] == "R'0" or rs[i] == "R'1"):
                aff = uc.AffinityRule(rs[i], rs[i], "h")
                self.genSys.add_affinity(aff)
                print(f'( {rs[i]}, {rs[i]} )')
            if not ("'" in rs[i]):
                aff = uc.AffinityRule(rs[i], "B'0", "h")
                self.genSys.add_affinity(aff)
                print(f'( {rs[i]}, {"Bp0"} )')
            elif not(i == rs_len):
                aff = uc.AffinityRule(rs[i], "B0", "h")
                self.genSys.add_affinity(aff)
           
                

    
                
    def add_reseed_prime_affinities(self):
        
        max_num_split = split_nonprime_label(self.reseed_states[0])
        
        max_num = max_num_split[1]
        rs = self.reseed_states.copy()
        print(rs)
        rs_filtered = list(filter(lambda i: "'" in i, rs))
        print(rs_filtered)
        rsnp_filtered = list(filter(lambda i: not("'" in i), rs))
        
        # Add all affinities between reseed prime and b's equal or smaller than next reseed 
        # and f's that are smaller than next reseed
        # Add all affinities between reseed non prime and b's that are equal or smaller
        curr_i = max_num
        
        for r in rs.reverse():
            if r == "R'0":
                continue
            
            else:
                for i in range(curr_i):
                    if not(i == curr_i):
                        b = "B" + str(i)
                        f = "F" + str(i)
                    
            
        # for i in range(1, max_num):
        #     for j in rs_filtered:
        #         js = split_prime_label(j)
        #         if js[1] == max_num:
        #             bmax = "B" + str(max_num)
        #             rs_aff = uc.AffinityRule(j, bmax, "h")
        #             self.genSys.add_affinity(rs_aff)
                
        #         if js[1] > i:
        #             b = "B" + str(i)
        #             rs_baff = uc.AffinityRule(j, b, "h")
        #             self.genSys.add_affinity(rs_baff)
        #             f = "F" + str(i)
        #             rs_faff = uc.AffinityRule(j, f, "h")
        #             self.genSys.add_affinity(rs_faff)
                        
    def add_fp_affinities(self, label):
        if check_is_prime(label) and not("R'" in label or "B'" in label):
            max_num_split = split_prime_label(label)
            max_num = max_num_split[1]
            
            for i in range(max_num):
                b = "B" + str(i)
                baff = uc.AffinityRule(label, b, "h")
                self.genSys.add_affinity(baff)
                if i < max_num:
                    f = "F" + str(i)
                    faff = uc.AffinityRule(label, f, "h")
                    self.genSys.add_affinity(faff)
                
                    
    def add_affinities_v2(self):
        # Const states 
        print("Affinities V2 Returns: ")
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
                            
                    elif "B" in wa:
                        if not(i == 0):
                            if i == wa_num and i > 1:
                                brp = "B" + str(i)
                                Aff = uc.AffinityRule(wa, brp, "h")
                                self.genSys.add_affinity(Aff)
                            # If i is one less than wa_num   
                            elif (i - 1) == wa_num and wa_num >= 1:
                                brp = "B" + str(i)   
                                Aff = uc.AffinityRule(wa, brp,"h")
                                self.genSys.add_affinity(Aff)
                                
                        if i <= wa_num and not(i == 0):
                            brp = "B" + str(i)
                            Aff = uc.AffinityRule(wa, brp, "h")
                            self.genSys.add_affinity(Aff)
                        pass
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
                        elif i <= (wa_num + 1):
                            b = "B" + str(i)
                            Aff = uc.AffinityRule(wa, b, "h")
                            self.genSys.add_affinity(Aff)
                        if not(i == 0):
                           fp = "F'" + str(i)
                           Aff = uc.AffinityRule(wa, fp, "h")
                           self.genSys.add_affinity(Aff)    
                           if i > 1:
                                f = "F" + str(i)
                                Aff = uc.AffinityRule(wa, f, "h")
                                self.genSys.add_affinity(Aff)          
                else:
                    b = "B" + str(i)
                    Aff = uc.AffinityRule(wa, b, "h")
                    self.genSys.add_affinity(Aff)
                    if i < bl:
                        f = "F" + str(i)
                        Aff = uc.AffinityRule(wa, f, "h")
                        self.genSys.add_affinity(Aff)
                        
        #loop through numbers from 0 to max bit len
        # for i in range(1, bl):
  
        #     b = "B" + str(i)
        #     bp1 = "B" + str(i + 1)
        #     bm1 = "B" + str(i - 1)
        #     f = "F" + str(i)
        #     fp1 = "F" + str(i + 1)
        #     fm1 = "F" + str(i - 1)
        #     fp = "F'" + str(i)
        #     fpp1 = "F'" + str(i + 1)
        #     fpm1 = "F'" + str(i - 1)
            
        #     r = "R" + str(i)   
        #     rp1 = "R" + str(i + 1)
        #     rm1 = "R" + str(i - 1) 
            
        #     rp = "R'" + str(i) 
        #     i_list = [b, bp1, bm1, f, fp1, fm1, fp, fpp1, fpm1, r, rp1, rm1, rp]
        #     i_list = list(filter(lambda x: x in i_list, CONST_STATES)) 
            
        #     # Seed affinities back
        #     if b in i_list:
        #         Aff = uc.AffinityRule("S", b, "h")
        #         self.genSys.add_affinity(Aff)
        #         # B attaches to self if greater than 1
        #         if i > 1:
        #             Aff = uc.AffinityRule(b, b, "h")
        #             self.genSys.add_affinity(Aff)
                    
        #     if bp1 in i_list:
        #         #b can be attached to b+1
        #         Aff = uc.AffinityRule(bp1, b, "h")
        #         self.genSys.add_affinity(Aff)
        #         # f can have b one bigger attached to E
        #         if f in i_list:
        #             Aff = uc.AffinityRule(f, bp1, "h")
        #             self.genSys.add_affinity(Aff)
                    
        #     if f in i_list:
        #         # Seed attaches to f
        #        Aff = uc.AffinityRule("S", f, "h")
        #        self.genSys.add_affinity(Aff)
        #        # f attaches to B'0
        #        Aff = uc.AffinityRule(f, "B'0","h")
        #        self.genSys.add_affinity(Aff)
        #        # F attaches to self
        #        if i > 1:
        #            Aff = uc.AffinityRule(f, f, "h")
        #            self.genSys.add_affinity(Aff)  
                 
        #     if fp in i_list:
        #         # F attaches to f prime
        #         Aff = uc.AffinityRule(f, fp, "h")
        #         self.genSys.add_affinity(Aff)
                
        #     if r in i_list:
        #         Aff = uc.AffinityRule(r, rp, "h")
        #         self.genSys.add_affinity(Aff) 
                
        #         # R attaches to self if greater than 1
        #         if i > 1:
        #             Aff = uc.AffinityRule(r, r, "h")
        #             self.genSys.add_affinity(Aff)  
                
                    
            # seed affinities forward
            #Reseed affinities non prime only b states attach
            # B affinities 
        print("End Affinities V2 Returns")     
                                    
    def add_affinities(self):
        # northAff = uc.AffinityRule("[W]", "[E]'", "h")
        # genSys.add_affinity(northAff)
        states = self.genSys.returnStates()
        b0Aff = uc.AffinityRule("S","B0", "h")
        self.genSys.add_affinity(b0Aff)
        
        b0f0Aff = uc.AffinityRule("F0","B0", "h")
        self.genSys.add_affinity(b0f0Aff)

        bp0f0Aff = uc.AffinityRule("F0","B'0", "h")
        self.genSys.add_affinity(bp0f0Aff)
        
        b1bp0Aff = uc.AffinityRule("B1","B'0", "h")
        self.genSys.add_affinity(b1bp0Aff)
        
        self.add_reseed_affinities_v2()
        self.add_affinities_v2()
        """ if not (math.log2(self.line_length - 1).is_integer()):
            self.add_reseed_prime_affinities()
        first_R_found = False
        
        if len(states) > 2:
            for i in range(1, len(states)):
                l2 = states[i].get_label()
                self.add_seed_affinity(l2)
                self.add_self_affinity(l2)
                self.add_self_prime_affinity(l2)
                self.add_prime_to_b0_f0_affinity(l2)
                self.add_bp0_affinities(l2)
                if not (math.log2(self.line_length- 1).is_integer()):
                    self.add_reseed_prime_to_nextReseed_affinities(l2)
                self.add_fp_affinities(l2) """
                
        #         if "'" in l2 and not(l2 == "B'0"): # Sticks to non prime self
        #             l1 = states[i-1].get_label()
        #             pAff = uc.AffinityRule(l1, l2, "h")
        #             self.genSys.add_affinity(pAff)
        #             bpAff = uc.AffinityRule(l2, "B0", "h")
        #             self.genSys.add_affinity(bpAff)
           
        #             bpAff = uc.AffinityRule(l2, "F0", "h")
        #             self.genSys.add_affinity(bpAff)
                    
                            
        #         # Reseed sticks to seed 
        #         elif l2[0] == "R":
        #             if first_R_found == False:
        #                 first_R_found = True
        #                 sAff = uc.AffinityRule("S", l2, "h")
        #                 self.genSys.add_affinity(sAff) 
        #                 toPop = "F" + l2[1:]
        #                 self.genSys.horizontal_affinities_dict.pop(("S", toPop), None)
                    
                            
                        
        #         elif l2 == "B'0":
        #             bAff = uc.AffinityRule("F0", "B0", "h")  
        #             self.genSys.add_affinity(bAff)   
        #             bAff = uc.AffinityRule("F0", "B'0", "h")
        #             self.genSys.add_affinity(bAff)
        #             bAff = uc.AffinityRule("B1", "B'0", "h")
        #             self.genSys.add_affinity(bAff)
                    
        #         else:        
        #             sAff = uc.AffinityRule("S", l2, "h")
        #             self.genSys.add_affinity(sAff)
        #             l1 = increment_string(l2)
        #             check_l2 = "B" + str(self.bit_len - 1)
        #             if l2 == check_l2:
        #                 pass
        #             elif not(l2 == "F0" or l2 == "B0"):
        #                 if l2[0] == "F":
        #                     fAff = uc.AffinityRule(l1, l2,"h")
        #                     self.genSys.add_affinity(fAff)
        #                     l1 = "B" + l1[1:]
        #                     fAff = uc.AffinityRule(l2, l1, "h")
        #                     self.genSys.add_affinity(fAff)
        #                 elif l2[0] == "B":
        #                     bAff = uc.AffinityRule(l1, l2, "h")  
        #                     self.genSys.add_affinity(bAff) 
                    
        #                 Aff = uc.AffinityRule(l2, l2, "h")
        #                 self.genSys.add_affinity(Aff)    

        
        hd = self.genSys.returnHorizontalAffinityDict() 
        shd = sorted(hd)
        affinities_test_14(shd)
        """ b = 0
        
        s = 3
        e = s - 1
        
        while e <= (len(shd) + s):
            t = list(shd[b:e])
            print(t)
            b = e + 1
            e = e + s """
                
            
                
                     
             
        return 
            
            
           


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

    """ sys = genSqrtBinCount("110011100")
    SaveFile.main(sys, ["biggerTestCount.xml"]) """
    

    linesSys = NLength_LineGenerator(14)







