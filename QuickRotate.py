import copy

from UniversalClasses import System, AffinityRule, TransitionRule
import SaveFile

# Major Note: Currently rotates a system by 90 degrees CW


def main(currentSystem, fileName):
    global tempSystem
    tempSystem = copy.deepcopy(currentSystem)

    # Reset tempSystem's dictionaries
    tempSystem.clearVerticalAffinityDict()
    tempSystem.clearHorizontalAffinityDict()
    tempSystem.clearVerticalTransitionDict()
    tempSystem.clearHorizontalTransitionDict()

    # Reset tempSystem's lists
    tempSystem.clearVerticalAffinityList()
    tempSystem.clearHorizontalAffinityList()
    tempSystem.clearVerticalTransitionList()
    tempSystem.clearHorizontalTransitionList()

    # Shallow copies of the currentSystem's lists
    currentVAffinityList = currentSystem.returnVerticalAffinityList()
    currentHAffinityList = currentSystem.returnHorizontalAffinityList()
    currentVTransitionList = currentSystem.returnVerticalTransitionList()
    currentHTransitionList = currentSystem.returnHorizontalTransitionList()

    # Shallow copies of the tempSystem's lists
    tempVAffinityList = tempSystem.returnVerticalAffinityList()
    tempHAffinityList = tempSystem.returnHorizontalAffinityList()
    tempVTransitionList = tempSystem.returnVerticalTransitionList()
    tempHTransitionList = tempSystem.returnHorizontalTransitionList()

    # If the current rule is a vertical affinity, swap label1's and label2's positions and change dir to horizontal.
    for rule in currentVAffinityList:
        label1 = rule.returnLabel1()
        label2 = rule.returnLabel2()
        strength = rule.returnStr()

        tempRule = AffinityRule(label2, label1, strength)
        tempHAffinityList.append(tempRule)

    # If the current rule is a horizontal affinity, don't touch label1 and label2, but change dir to horizontal.
    for rule in currentHAffinityList:
        label1 = rule.returnLabel1()
        label2 = rule.returnLabel2()
        strength = rule.returnStr()

        tempRule = AffinityRule(label1, label2, strength)
        tempVAffinityList.append(tempRule)

    # Apply the same principles we used in vertical affinities for vertical transitions.
    for rule in currentVTransitionList:
        label1 = rule.returnLabel1()
        label2 = rule.returnLabel2()
        label1Final = rule.returnLabel1Final()
        label2Final = rule.returnLabel2Final()

        tempRule = TransitionRule(label2, label1, label2Final, label1Final)
        tempHTransitionList.append(tempRule)

    # And the same thing for horizontal transitions.
    for rule in currentHTransitionList:
        label1 = rule.returnLabel1()
        label2 = rule.returnLabel2()
        label1Final = rule.returnLabel1Final()
        label2Final = rule.returnLabel2Final()

        tempRule = TransitionRule(label1, label2, label1Final, label2Final)
        tempVTransitionList.append(tempRule)

    # Translate tempSystem's lists into dictionaries
    tempSystem.translateListsToDicts()
    # Use SaveFile to save tempSystem as the rotated system of currentSystem
    SaveFile.main(tempSystem, fileName)
