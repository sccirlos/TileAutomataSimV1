import UniversalClasses as uc
import SaveFile

red = "f03a47"
blue = "3f88c5"
green = "0ead69"
orange = "f39237"
black = "323031"
white = "DFE0E2"
grey = "9EA9A4"
light_blue = "C2DCFE"

class fracGen:
    def __init__(self):
        seed = uc.State("S0", white)
        self.system = uc.System(1, [], [], [seed])
        
        for i in range(5):
            self.system.add_State(uc.State("S" + str(i), white))
            if i != 0:
                self.system.add_Initial_State(uc.State("S" + str(i), white))
                
        self.system.add_State(uc.State("S1'", white))
        
        aff0 = uc.AffinityRule("S0", "S1", "h")
        self.system.add_affinity(aff0)
        aff1 = uc.AffinityRule("S2", "S1", "v")
        self.system.add_affinity(aff1)
        aff2 = uc.AffinityRule("S3", "S2", "v")
        self.system.add_affinity(aff2)
        aff3 = uc.AffinityRule("S4", "S3", "h")
        self.system.add_affinity(aff3)

        trHC1 = uc.TransitionRule("S4", "S3", "w", "ne", "h")
        self.system.add_transition_rule(trHC1)
        trHC2 = uc.TransitionRule("ne", "S2", "ne", "ns", "v")
        self.system.add_transition_rule(trHC2)
        trHC3 = uc.TransitionRule("ns", "S1", "ns", "S1'", "v")
        self.system.add_transition_rule(trHC3)
        trHC4 = uc.TransitionRule("S0", "S1'", "a'_w", "Et_esw", "h")
        self.system.add_transition_rule(trHC4)


        # Add States
        self.affLabels = ["n", "s", "w", "e", "ne", "nw", "se", "sw", "wne", "nes", "esw", "swn", "nesw", "we", "ns"]
        self.northGlues = ["s", "se", "sw", "nes", "esw", "swn", "nesw", "ns"]
        self.southGlues = ["n", "ne", "nw", "wne", "nes", "swn", "nesw", "ns"]
        self.westGlues = ["e", "ne", "se", "wne", "nes", "esw", "nesw", "we"]
        self.eastGlues  = ["w", "nw", "sw", "wne", "esw", "swn", "nesw", "we" ]
        self.crumbLabels = ["a", "b", "c", "d", "e", "f", "g", "h"]
        self.printLabels = ["N", "S", "E", "W"]

        for label in self.affLabels:
            affState = uc.State(label, white)
            self.system.add_State(affState)

            tailState = uc.State("t_" + label, red)
            self.system.add_State(tailState)

            for prin in self.printLabels:
                tailPState = uc.State(prin + "t_" + label, red)
                self.system.add_State(tailPState)
            
            messStates = uc.State("m_" + label, blue)
            self.system.add_State(messStates)

            # crumbs
            for crumb in self.crumbLabels:
                crumbState = uc.State(crumb + "_" + label, light_blue)
                self.system.add_State(crumbState)
                crumbPState = uc.State(crumb + "'_" + label, green)
                self.system.add_State(crumbPState)

            for prin in self.printLabels:
                printState = uc.State(prin + "_" + label, light_blue)
                self.system.add_Seed_State(printState)

        # Initial Tiles
        self.system.add_Initial_State(uc.State("n", white))
        self.system.add_Initial_State(uc.State("e", white))
        self.system.add_Initial_State(uc.State("s", white))
        self.system.add_Initial_State(uc.State("w", white))

        # add affinities
        for sLabel in self.southGlues:
            sStates = [sLabel, "t_" + sLabel, "m_" + sLabel]
            for crumb in self.crumbLabels:
                sStates.append(crumb + "_" + sLabel)
                sStates.append(crumb + "'_" + sLabel)

            for prin in self.printLabels:
                sStates.append(prin + "_" + sLabel)
            
            for nLabel in self.northGlues:
                nStates = [nLabel, "t_" + nLabel, "m_" + nLabel]
                for crumb in self.crumbLabels:
                    nStates.append(crumb + "_" + nLabel)
                    nStates.append(crumb + "'_" + nLabel)

                for prin in self.printLabels:
                    nStates.append(prin + "_" + nLabel)

                for sST in sStates:
                    for nST in nStates:
                        aff = uc.AffinityRule(sST, nST, "v")
                        self.system.add_affinity(aff)

        for eLabel in self.eastGlues:
            eStates = [eLabel, "t_" + eLabel, "m_" + eLabel]
            for crumb in self.crumbLabels:
                eStates.append(crumb + "_" + eLabel)
                eStates.append(crumb + "'_" + eLabel)

            for prin in self.printLabels:
                eStates.append(prin + "_" + eLabel)

            for wLabel in self.westGlues:
                wStates = [wLabel, "t_" + wLabel, "m_" + wLabel]
                for crumb in self.crumbLabels:
                    wStates.append(crumb + "_" + wLabel)
                    wStates.append(crumb + "'_" + wLabel)

                for prin in self.printLabels:
                    wStates.append(prin + "_" + wLabel)

                for eST in eStates:
                    for wST in wStates:
                        aff = uc.AffinityRule(eST, wST, "h")
                        self.system.add_affinity(aff)


        # Search Transitions
        # Printing states
        for label1 in self.affLabels:
            for label2 in self.affLabels:
                prinTR = uc.TransitionRule("")



        


 




    # def aff(self, label1, label2):

    #     # North
    #     nAffs = uc.AffinityRule(label1 + "n", label2 + "s")
    #     self.system.add_affinity(nAffs)

    #     nAffv = uc.AffinityRule(label1 + "n", label2 + "v")
    #     self.system.add_affinity(nAffv)

    #     nAffsw = uc.AffinityRule(label1 + "n", label2 + "sw")
    #     self.system.add_affinity(nAffsw)

    #     nAffse = uc.AffinityRule(label1 + "n", label2 + "se")
    #     self.system.add_affinity(nAffse)

    #     nAffsen = uc.AffinityRule(label1 + "n", label2 + "sen")
    #     self.system.add_affinity(nAffsen)

    #     nAffesw = uc.AffinityRule(label1 + "n", label2 + "ews")
    #     self.system.add_affinity(nAffesw)

    #     nAffnes= uc.AffinityRule(label1 + "n", label2 + "nes")
    #     self.system.add_affinity(nAffnes)

    def getSys(self):
        return self.system

if __name__ == "__main__":
    gen = fracGen()

    SaveFile.main(gen.getSys(), ["fractals.xml"])
    print("Generated File: saved")
