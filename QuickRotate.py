import copy

from UniversalClasses import System, AffinityRule, TransitionRule
import SaveFile

# Major Note: Currently rotates a system by 90 degrees CW


def main(currentSystem):
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

    currentVAffinityList = currentSystem.returnVerticalAffinityList()
    currentHAffinityList = currentSystem.returnHorizontalAffinityList()
    currentVTransitionList = currentSystem.returnVerticalTransitionList()
    currentHTransitionList = currentSystem.returnHorizontalTransitionList()
