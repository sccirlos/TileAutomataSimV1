# These classes are used for Loading and Saving Files and Communicating with general_TA_simulator.

class State:
    def __init__(self, label, color):
        self.label = label
        self.color = color

    # Getters
    def returnLabel(self):
        return self.label

    def returnColor(self):
        return self.color


# Not in use right now.
class SeedAssemblyTile:
    def __init__(self, label, x, y):
        self.label = label
        self.x = x
        self.y = y


class AffinityRule:
    def __init__(self, label1, label2, dir, strength):
        self.label1 = label1  # Left/Upper label
        self.label2 = label2  # Right/Bottom label
        self.dir = dir  # Horizontal or Vertical
        self.strength = strength  # Bond Strength (as a string)

    # Getters
    def returnLabel1(self):
        return self.label1

    def returnLabel2(self):
        return self.label2

    def returnDir(self):
        return self.dir

    def returnStr(self):
        return self.strength


class TransitionRule:
    def __init__(self, label1, label2, label1Final, label2Final, dir):
        self.label1 = label1
        self.label2 = label2
        self.label1Final = label1Final
        self.label2Final = label2Final
        self.dir = dir

    # Getters
    def returnLabel1(self):
        return self.label1

    def returnLabel2(self):
        return self.label2

    def returnLabel1Final(self):
        return self.label1Final

    def returnLabel2Final(self):
        return self.label2Final

    def returnDir(self):
        return self.dir
