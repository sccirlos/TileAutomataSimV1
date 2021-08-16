from os import X_OK
from random import randrange
import copy
import LoadFile

AssemblyHistory = []  # This will be the list of tiles where we placed a tile in chronological order; this will be essentially our complete history of created assemblies
AvailableMoves = []  # Records possible rules to execute in a move; it's placed here so that the main window can access it easier
TimeTaken = [] #Records the length of AvailableMoves at each step
CompleteAssemblyHistory = []  # Records all past assemblies.


class ActiveTile:  # Tiles based on the Base States
    ID = 0

    def __init__(self, x, y, base_state=None):
        # Attributes Inherited from a Base Tile
        if(base_state == None):
            self.label = "?"
            self.color = "ff0000"
            self.relevantAffinities = []
            self.relevantTransitions = []
        else:
            self.label = base_state.returnLabel()
            self.color = base_state.returnColor()
            self.relevantAffinities = base_state.returnRelevantAffinities()
            self.relevantTransitions = base_state.returnRelevantTransitions()
        # New Attributes for Active Tiles for Positional Tracking
        self.left = None  # Left Neighbor (Tile)
        self.right = None  # Right Neighbor (Tile)
        self.up = None  # Neighbor from above (Tile)
        self. down = None  # Neighbor from below (Tile)
        self.x = x  # X-coordinate in the grid (Int)
        self.y = y  # Y-coordinate in the grid (Int)
        self.ID = ActiveTile.ID
        ActiveTile.ID += 1

    # Getters
    def returnCoordinates(self):
        return ("("+str(self.x)+", "+str(self.y)+")")

    def returnRelevantAffinities(self):
        return self.relevantAffinities

    def returnRelevantTransitions(self):
        return self.relevantTransitions

    def returnID(self):
        return self.ID

    def returnLeft(self):
        return self.left

    def returnRight(self):
        return self.right

    def returnUp(self):
        return self.up

    def returnDown(self):
        return self.down

    def returnLabel(self):
        return self.label

    def returnX(self):
        return self.x

    def returnY(self):
        return self.y

    # Setters
    def setLabel(self, label):
        self.label = label

    def setLeft(self, neighbor):
        self.left = neighbor

    def setRight(self, neighbor):
        self.right = neighbor

    def setUp(self, neighbor):
        self.up = neighbor

    def setDown(self, neighbor):
        self.down = neighbor

    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y

    def setColor(self, color):
        self.color = color

    def setRelevantAffinities(self, affinities):
        self.relevantAffinities = affinities

    def setRelevantTransitions(self, transitions):
        self.relevantTransitions = transitions

    # Displayers
    def displayBasicInfo(self):
        print("\t-Label: "+self.label+"; Coordinates: (" +
              str(self.x)+", "+str(self.y)+") ; Color: "+self.color)


class AvailableAffinity:
    def __init__(self, origin, dir, destination, ID):
        self.origin = origin
        self.dir = dir
        self.destination = destination
        self.ID = ID  # Active/Origin Tile's ID; AKA, which tile from the assembly will this rule be executed on
        self.ruleType = "Affinity"
    # Getters

    def returnOrigin(self):
        return self.origin

    def returnDir(self):
        return self.dir

    def returnDestination(self):
        return self.destination

    def returnID(self):
        return self.ID

    def returnRuleType(self):
        return self.ruleType


class AvailableTransition:
    def __init__(self, origin, neighbor, bondDir, finalOrigin, finalNeighbor, ID):
        self.origin = origin
        self.neighbor = neighbor
        self.bondDir = bondDir
        self.finalOrigin = finalOrigin
        self.finalNeighbor = finalNeighbor
        self.ID = ID
        self.ruleType = "Transition"

    # Getters
    def returnOrigin(self):
        return self.origin

    def returnNeighbor(self):
        return self.neighbor

    def returnDir(self):
        return self.bondDir

    def returnFinalOrigin(self):
        return self.finalOrigin

    def returnFinalNeighbor(self):
        return self.finalNeighbor

    def returnID(self):
        return self.ID

    def returnRuleType(self):
        return self.ruleType


def PlacingFirstTile(AssemblyHistory, BaseStates):
    elementNum = randrange(0, len(BaseStates))
    # Create an instance of the 1st active tile
    tempActiveTile = ActiveTile(0, 0, BaseStates[0])
    AssemblyHistory.append(tempActiveTile)
    print("Initial Assembly:")
    for element in AssemblyHistory:
        element.displayBasicInfo()
    # Make a shallow copy of the current list of tiles (the assembly)
    tempHistory = copy.deepcopy(AssemblyHistory)
    # Attach the shallow copy to CompleteAssemblyHistory
    CompleteAssemblyHistory.append(tempHistory)


def PlacingSecondTile(AssemblyHistory, CompleteStatesSet):

    while(True):
        # Main: Find out what are our available moves.

        # Reset AvailableMoves when the simulator searches for a new move.
        TimeTaken.append(len(AvailableMoves))
        AvailableMoves.clear()

        # Checking each tile individually...
        for tile in AssemblyHistory:
            tileID = tile.returnID()
            tileLeftNeighbor = tile.returnLeft()
            tileRightNeighbor = tile.returnRight()
            tileUpNeighbor = tile.returnUp()
            tileDownNeighbor = tile.returnDown()
            tileAffinities = tile.returnRelevantAffinities()
            tileTransitions = tile.returnRelevantTransitions()
            # Check through the current tile's affinity rules...
            for rule in tileAffinities:
                ruleOrigin = rule.returnOrigin()
                ruleDir = rule.returnDir()
                ruleDestination = rule.returnDestination()

                # If all sides of a tile are occupied, skip the entire affinity check
                if(tileLeftNeighbor != None and tileRightNeighbor != None and tileUpNeighbor != None and tileDownNeighbor != None):
                    break
                else:
                    # If we have a leftward affinity, and the left side is open...
                    if(ruleDir == 'left' and tileLeftNeighbor == None):
                        # Pick the rule and attach it to AvailableMoves[]
                        tempMove = AvailableAffinity(
                            ruleOrigin, ruleDir, ruleDestination, tileID)
                        AvailableMoves.append(tempMove)
                    # Same thing if we have a rightward affinity and the right side is open...
                    if(ruleDir == 'right' and tileRightNeighbor == None):
                        tempMove = AvailableAffinity(
                            ruleOrigin, ruleDir, ruleDestination, tileID)
                        AvailableMoves.append(tempMove)
                    # Same thing if we have an upward affinity and we have open space above us...
                    if(ruleDir == 'up' and tileUpNeighbor == None):
                        tempMove = AvailableAffinity(
                            ruleOrigin, ruleDir, ruleDestination, tileID)
                        AvailableMoves.append(tempMove)
                    # Lastly, same thing with downward affinity...
                    if(ruleDir == 'down' and tileDownNeighbor == None):
                        tempMove = AvailableAffinity(
                            ruleOrigin, ruleDir, ruleDestination, tileID)
                        AvailableMoves.append(tempMove)

            # Then check the current tile's transition rules...
            for rule in tileTransitions:
                ruleOrigin = rule.returnOrigin()  # It's the origin's label
                ruleDir = rule.returnDir()
                ruleNeighbor = rule.returnNeighbor()  # It's the neighbor's label
                ruleFinalOrigin = rule.returnFinalOrigin()  # Label
                ruleFinalNeighbor = rule.returnFinalNeighbor()  # Label

                # If all sides of a tile are empty, skip the entire transition check.
                if(tileLeftNeighbor == None and tileRightNeighbor == None and tileUpNeighbor == None and tileDownNeighbor == None):
                    break
                else:
                    # Initiate labels as None for exception-handling
                    tileLeftNeighborLabel = None
                    tileRightNeighborLabel = None
                    tileUpNeighborLabel = None
                    tileDownNeighborLabel = None
                    # Gather labels if the neighbor exists
                    if(tileLeftNeighbor != None):
                        tileLeftNeighborLabel = tileLeftNeighbor.returnLabel()
                    if(tileRightNeighbor != None):
                        tileRightNeighborLabel = tileRightNeighbor.returnLabel()
                    if(tileUpNeighbor != None):
                        tileUpNeighborLabel = tileUpNeighbor.returnLabel()
                    if(tileDownNeighbor != None):
                        tileDownNeighborLabel = tileDownNeighbor.returnLabel()

                    # Check neighbors associated with a bond direction
                    # If the direction is left and the neighbor's label matches the rule's neighbor label...
                    if(ruleDir == "left" and tileLeftNeighborLabel == ruleNeighbor):
                        # Add this rule to AvailableMoves
                        tempMove = AvailableTransition(
                            ruleOrigin, ruleNeighbor, ruleDir, ruleFinalOrigin, ruleFinalNeighbor, tileID)
                        AvailableMoves.append(tempMove)
                    if(ruleDir == "right" and tileRightNeighborLabel == ruleNeighbor):
                        tempMove = AvailableTransition(
                            ruleOrigin, ruleNeighbor, ruleDir, ruleFinalOrigin, ruleFinalNeighbor, tileID)
                        AvailableMoves.append(tempMove)
                    if(ruleDir == "up" and tileUpNeighborLabel == ruleNeighbor):
                        tempMove = AvailableTransition(
                            ruleOrigin, ruleNeighbor, ruleDir, ruleFinalOrigin, ruleFinalNeighbor, tileID)
                        AvailableMoves.append(tempMove)
                    if(ruleDir == "down" and tileDownNeighborLabel == ruleNeighbor):
                        tempMove = AvailableTransition(
                            ruleOrigin, ruleNeighbor, ruleDir, ruleFinalOrigin, ruleFinalNeighbor, tileID)
                        AvailableMoves.append(tempMove)

        # Main: The exit for the move-search is if there is no available moves at this point. If we can't find any moves, then we must be in the terminal assembly.
        if(AvailableMoves == []):
            print("TERMINAL ASSEMBLY REACHED!")
            break
        else:
            # Main: Execute a Random Available Move
            elementNum = randrange(0, len(AvailableMoves))  # Pick a number
            # Pick the corresponding available move from that number
            activeMove = AvailableMoves[0]
            # Determine what kind of rule we're executing.
            moveType = activeMove.returnRuleType()
            # If it's an affinity rule:
            if(moveType == "Affinity"):
                # Gather Move's Data
                originID = activeMove.returnID()
                # The entire origin tile
                originTile = AssemblyHistory[originID]
                originX = originTile.returnX()
                originY = originTile.returnY()
                moveDir = activeMove.returnDir()
                moveDestinationLabel = activeMove.returnDestination()
                # Dummy Data to Prevent Future Errors
                # Since there's no base state, the None value from the constructor kicks in.
                destinationTile = ActiveTile(0, 0)

                if(moveDir == "left"):
                    for state in CompleteStatesSet:
                        baseLabel = state.returnLabel()

                        # Note: Add an exception branch if the new label isn't from the BaseStates
                        if(baseLabel == moveDestinationLabel):
                            baseColor = state.returnColor()
                            baseAffinities = state.returnRelevantAffinities()
                            baseTransitions = state.returnRelevantTransitions()

                            destinationTile.setLabel(baseLabel)
                            destinationTile.setColor(baseColor)
                            destinationTile.setRelevantAffinities(
                                baseAffinities)
                            destinationTile.setRelevantTransitions(
                                baseTransitions)
                    # Establish the new tile's coordinates
                    destinationTile.setX(originX - 1)
                    destinationTile.setY(originY)
                    # Update both tiles' neighbor-statuses
                    originTile.setLeft(destinationTile)
                    destinationTile.setRight(originTile)
                elif(moveDir == "right"):  # If moveDir == "right"
                    for state in CompleteStatesSet:
                        baseLabel = state.returnLabel()

                        # Note: Add an exception branch if the new label isn't from the BaseStates
                        if(baseLabel == moveDestinationLabel):
                            baseColor = state.returnColor()
                            baseAffinities = state.returnRelevantAffinities()
                            baseTransitions = state.returnRelevantTransitions()

                            destinationTile.setLabel(baseLabel)
                            destinationTile.setColor(baseColor)
                            destinationTile.setRelevantAffinities(
                                baseAffinities)
                            destinationTile.setRelevantTransitions(
                                baseTransitions)
                    # Establish the new tile's coordinates
                    destinationTile.setX(originX + 1)
                    destinationTile.setY(originY)
                    # Update both tiles' neighbor-statuses
                    originTile.setRight(destinationTile)
                    destinationTile.setLeft(originTile)
                elif(moveDir == "up"):
                    for state in CompleteStatesSet:
                        baseLabel = state.returnLabel()

                        # Note: Add an exception branch if the new label isn't from the BaseStates
                        if(baseLabel == moveDestinationLabel):
                            baseColor = state.returnColor()
                            baseAffinities = state.returnRelevantAffinities()
                            baseTransitions = state.returnRelevantTransitions()

                            destinationTile.setLabel(baseLabel)
                            destinationTile.setColor(baseColor)
                            destinationTile.setRelevantAffinities(
                                baseAffinities)
                            destinationTile.setRelevantTransitions(
                                baseTransitions)
                    # Establish the new tile's coordinates
                    destinationTile.setX(originX)
                    destinationTile.setY(originY + 1)
                    # Update both tiles' neighbor-statuses
                    originTile.setUp(destinationTile)
                    destinationTile.setDown(originTile)
                elif(moveDir == "down"):
                    for state in CompleteStatesSet:
                        baseLabel = state.returnLabel()

                        # Note: Add an exception branch if the new label isn't from the BaseStates
                        if(baseLabel == moveDestinationLabel):
                            baseColor = state.returnColor()
                            baseAffinities = state.returnRelevantAffinities()
                            baseTransitions = state.returnRelevantTransitions()

                            destinationTile.setLabel(baseLabel)
                            destinationTile.setColor(baseColor)
                            destinationTile.setRelevantAffinities(
                                baseAffinities)
                            destinationTile.setRelevantTransitions(
                                baseTransitions)
                    # Establish the new tile's coordinates
                    destinationTile.setX(originX)
                    destinationTile.setY(originY - 1)
                    # Update both tiles' neighbor-statuses
                    originTile.setDown(destinationTile)
                    destinationTile.setUp(originTile)
                # UPDATE: Further update the new tile if it initiates with neighbors
                destinationTempX = destinationTile.returnX()  # New tile's X-value
                destinationTempY = destinationTile.returnY()  # New tile's y-value

                # The expected value X-value of the left neighbor.
                leftNeighborCheck = destinationTempX - 1
                # Repeat the logic for the rest of the possible spots...
                rightNeighborCheck = destinationTempX + 1
                upNeighborCheck = destinationTempY + 1
                downNeighborCheck = destinationTempY - 1
                # Searching through the tiles in AssemblyHistory before we place the new tile...
                for tile in AssemblyHistory:
                    tileX = tile.returnX()  # X-value of the current tile in AH
                    tileY = tile.returnY()  # Y-value of the current tile in AH

                    # Found a left neighbor:
                    # Proof: Difference between left neighbor's coordinates and the new tile's coordinates: (-1,0)
                    if(tileX == leftNeighborCheck and tileY == destinationTempY):
                        destinationTile.setLeft(tile)
                    # Repeat logic for the rest...
                    if(tileX == rightNeighborCheck and tileY == destinationTempY):
                        destinationTile.setRight(tile)
                    if(tileX == destinationTempX and tileY == upNeighborCheck):
                        destinationTile.setUp(tile)
                    if(tileX == destinationTempX and tileY == downNeighborCheck):
                        destinationTile.setDown(tile)
                # Append the new tile to the assembly
                AssemblyHistory.append(destinationTile)
            # If it's a transition rule:
            else:
                # Gather Move's Data
                originID = activeMove.returnID()
                originTile = AssemblyHistory[originID]  # Actual origin tile
                bondDir = activeMove.returnDir()
                neighborTile = None  # Actual neighbor tile

                # Origin's final label based on the rule
                finalOrigin = activeMove.returnFinalOrigin()
                # Neighbor's final label based on the rule
                finalNeighbor = activeMove.returnFinalNeighbor()

                # Establish who's the neighbor.
                # If it's a transition based from a leftward bond...
                if(bondDir == "left"):
                    neighborTile = originTile.returnLeft()
                elif(bondDir == "right"):
                    neighborTile = originTile.returnRight()
                elif(bondDir == "up"):
                    neighborTile = originTile.returnUp()
                elif(bondDir == "down"):
                    neighborTile = originTile.returnDown()

                # Start replacing the origin and neighbor with another state
                for state in CompleteStatesSet:
                    baseLabel = state.returnLabel()
                    baseColor = state.returnColor()
                    baseAffinities = state.returnRelevantAffinities()
                    baseTransitions = state.returnRelevantTransitions()

                    if(baseLabel == finalOrigin):
                        originTile.setLabel(baseLabel)
                        originTile.setColor(baseColor)
                        originTile.setRelevantAffinities(baseAffinities)
                        originTile.setRelevantTransitions(baseTransitions)
                    if(baseLabel == finalNeighbor):
                        neighborTile.setLabel(baseLabel)
                        neighborTile.setColor(baseColor)
                        neighborTile.setRelevantAffinities(baseAffinities)
                        neighborTile.setRelevantTransitions(baseTransitions)
                # UPDATE: Further update the new tile if it initiates with neighbors
                originX = originTile.returnX()  # X-value of the origin tile
                originY = originTile.returnY()  # Y-value of the origin tile
                neighborX = neighborTile.returnX()  # X-value of the neighbor tile
                neighborY = neighborTile.returnY()  # Y-value of the neighbor tile
                # Searching through the tiles in AssemblyHistory before we place the new tile...

                # The expected X and Y values for the origin's neighbors
                leftOriginCheck = originX - 1
                rightOriginCheck = originX + 1
                upOriginCheck = originY + 1
                downOriginCheck = originY - 1

                # The expected X and Y values for the neighbor's neighbors
                leftNeighborCheck = neighborX - 1
                rightNeighborCheck = neighborX + 1
                upNeighborCheck = neighborY + 1
                downNeighborCheck = neighborY - 1
                for tile in AssemblyHistory:
                    tileX = tile.returnX()  # X-value of the current tile in AH
                    tileY = tile.returnY()  # Y-value of the current tile in AH

                    # Found a left neighbor for the neighbor tile:
                    # Proof: Difference between left neighbor's coordinates and the new tile's coordinates: (-1,0)
                    if(tileX == leftOriginCheck and tileY == originY):
                        originTile.setLeft(tile)
                    # Repeat logic for the rest...
                    if(tileX == rightOriginCheck and tileY == originY):
                        originTile.setRight(tile)
                    if(tileX == originX and tileY == upOriginCheck):
                        originTile.setUp(tile)
                    if(tileX == originX and tileY == downOriginCheck):
                        originTile.setDown(tile)

                    # Found a left neighbor for the neighbor tile:
                    # Proof: Difference between left neighbor's coordinates and the new tile's coordinates: (-1,0)
                    if(tileX == leftNeighborCheck and tileY == neighborY):
                        neighborTile.setLeft(tile)
                    # Repeat logic for the rest...
                    if(tileX == rightNeighborCheck and tileY == neighborY):
                        neighborTile.setRight(tile)
                    if(tileX == neighborX and tileY == upNeighborCheck):
                        neighborTile.setUp(tile)
                    if(tileX == neighborX and tileY == downNeighborCheck):
                        neighborTile.setDown(tile)

        print("New Assembly:")
        # Main: Print resulting assembly
        for element in AssemblyHistory:
            element.displayBasicInfo()
        # Make a deep copy of the current list of tiles (the assembly)
        tempHistory = copy.deepcopy(AssemblyHistory)
        # Attach the deep copy to CompleteAssemblyHistory
        CompleteAssemblyHistory.append(tempHistory)

# This Display feature is only to make it clear how we can access past assembly.


def DisplayCompleteAssemblyHistory(CompleteAssemblyHistory):
    print("Complete Assembly History: ")
    i = 0
    for assembly in CompleteAssemblyHistory:
        print("\n Assembly #"+str(i)+":")
        for element in assembly:
            element.displayBasicInfo()
        i += 1
    # Reset i in case the user wants to assembly a different system
    i = 0


def Main():
    # Resets conflicting information if the user loads a different system
    AssemblyHistory.clear()
    CompleteAssemblyHistory.clear()

    ActiveTile.ID = 0  # Resets the ID counter for ActiveTiles
    # This is the list of base states from the loading-seciton
    BaseStates = LoadFile.BaseStateSet
    # List of transition states from the loading-section
    TransitionStates = LoadFile.TransitionStateSet
    # Collection of Base States and Transition States
    CompleteStatesSet = BaseStates + TransitionStates

    PlacingFirstTile(AssemblyHistory, BaseStates)
    PlacingSecondTile(AssemblyHistory, CompleteStatesSet)
    # Displays all past assemblies
    DisplayCompleteAssemblyHistory(CompleteAssemblyHistory)

    # Resets the terminal assembly to allow the user to create another assembly instantly.
