from os import X_OK
import LoadFile
from random import randrange


class ActiveTile:  # Tiles based on the Base States
    ID = 0

    def __init__(self, base_tile, x, y):
        # Attributes Inherited from a Base Tile
        self.label = base_tile.returnLabel()
        self.color = base_tile.returnColor()
        self.relevantAffinities = base_tile.returnRelevantAffinities()
        self.relevantTranstitions = base_tile.returnRelevantTransitions()
        # New Attributes for Active Tiles for Positional Tracking
        self.left = None  # Left Neighbor (Tile)
        self.right = None  # Right Neighbor (Tile)
        self.x = x  # X-coordinate in the grid (Int)
        self.y = y  # Y-coordinate in the grid (Int)
        self.ID = ActiveTile.ID
        ActiveTile.ID += 1
    # Getters

    def returnCoordinates(self):
        return (str(self.x)+", "+str(self.y))

    def returnRelevantAffinities(self):
        return self.relevantAffinities

    def returnRelevantTransitions(self):
        return self.relevantTranstitions

    def returnID(self):
        return self.ID

    def returnLeft(self):
        return self.left

    def returnRight(self):
        return self.right

    def returnLabel(self):
        return self.label

    def returnX(self):
        return self.x

    def returnY(self):
        return self.y
    # Setters

    def setLabel(self, label):  # Will need to change this later because this only allows for a superficial transition (aka, just the label changes)
        self.label = label

    def setLeft(self, neighbor):
        self.left = neighbor

    def setRight(self, neighbor):
        self.right = neighbor

    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y

    def setColor(self, color):
        self.color = color

    def setRelevantAffinities(self, affinities):
        self.relevantAffinities = affinities

    def setRelevantTransitions(self, transitions):
        self.relevantTranstitions = transitions
    # Displayers

    def displayBasicInfo(self):
        print("\t-Label: "+self.label+"; X-Coordinate: "+str(self.x) +
              "; Y-Coordinate: "+str(self.y)+"; Color: "+self.color)


class CustomActiveTile:  # Tiles that aren't from the Base States
    def __init__(self, label, color, x, y):
        self.label = label
        self.color = color
        self.x = x
        self.y = y
        self.relevantAffinities = []
        self.relevantTransitions = []
        self.left = None
        self.right = None
        self.ID = ActiveTile.ID
        ActiveTile.ID += 1
    # Getters

    def returnCoordinates(self):
        return (str(self.x)+", "+str(self.y))

    def returnRelevantAffinities(self):
        return self.relevantAffinities

    def returnRelevantTransitions(self):
        return self.relevantTranstitions

    def returnID(self):
        return self.ID

    def returnLeft(self):
        return self.left

    def returnRight(self):
        return self.right

    def returnLabel(self):
        return self.label


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
    def __init__(self, originalLeft, originalRight, finalLeft, finalRight, ID, neighborID):
        self.originalLeft = originalLeft
        self.originalRight = originalRight
        self.finalLeft = finalLeft
        self.finalRight = finalRight
        self.ID = ID  # 'Origin' Tile's ID (Subjectively)
        self.neighborID = neighborID  # 'Origin' Tile's Neighbor's ID
        self.ruleType = "Transition"
    # Getters

    def returnOriginalLeft(self):
        return self.originalLeft

    def returnOriginalRight(self):
        return self.originalRight

    def returnFinalLeft(self):
        return self.finalLeft

    def returnFinalRight(self):
        return self.finalRight

    def returnID(self):
        return self.ID

    def returnNeighborID(self):
        return self.neighborID

    def returnRuleType(self):
        return self.ruleType


def PlacingFirstTile(AssemblyHistory, BaseStates):
    elementNum = randrange(0, len(BaseStates))
    # Create an instance of the 1st active tile
    tempActiveTile = ActiveTile(BaseStates[elementNum], 0, 0)
    AssemblyHistory.append(tempActiveTile)
    print("Current Assembly:")
    for element in AssemblyHistory:
        element.displayBasicInfo()


def PlacingSecondTile(AssemblyHistory, BaseStates):

    while(True):
        # Main: Find out what are our available moves.
        AvailableMoves = []
        # Checking each tile individually...
        for tile in AssemblyHistory:
            tileID = tile.returnID()
            tileLabel = tile.returnLabel()
            tileLeftNeighbor = tile.returnLeft()
            tileRightNeighbor = tile.returnRight()
            tileAffinities = tile.returnRelevantAffinities()
            tileTransitions = tile.returnRelevantTransitions()
            # Check through the current tile's affinity rules...
            for rule in tileAffinities:
                ruleOrigin = rule.returnOrigin()
                ruleDir = rule.returnDir()
                ruleDestination = rule.returnDestination()

                # If the tile's left and right sides are occupied, skip the entire affinity check
                if(tileLeftNeighbor != None and tileRightNeighbor != None):
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
            # Then check the current tile's transition rules...
            for rule in tileTransitions:
                ruleOriginalLeft = rule.returnOriginalLeft()
                ruleOriginalRight = rule.returnOriginalRight()
                ruleFinalLeft = rule.returnFinalLeft()
                ruleFinalRight = rule.returnFinalRight()
                # If the tile has no neighbors, then there's no way to make a transition, so skip the entire transition check
                if(tileLeftNeighbor == None and tileRightNeighbor == None):
                    break
                else:
                    # Note: This part doesn't account for a missing neighbor
                    tileLeftNeighborLabel = tileLeftNeighbor.returnLabel()
                    tileLeftNeighborID = tileLeftNeighbor.returnID()
                    tileRightNeighborLabel = tileRightNeighbor.returnLabel()
                    tileRightNeighborID = tileRightNeighbor.returnID()

                    # If the current tile is the 'left' tile, then we must check the 'right'. If everything is correct, add the transition rule to AvailableMoves[].
                    if(tileLabel == ruleOriginalLeft and tileRightNeighborLabel == ruleOriginalRight):
                        tempMove = AvailableTransition(
                            ruleOriginalLeft, ruleOriginalRight, ruleFinalLeft, ruleFinalRight, tileID, tileRightNeighborID)
                        AvailableMoves.append(tempMove)
                    # Same thing as before: if the current tile is the 'right' tile, then we must check the 'left'...
                    if(tileLabel == ruleOriginalRight and tileLeftNeighborLabel == ruleOriginalLeft):
                        tempMove = AvailableTransition(
                            ruleOriginalLeft, ruleOriginalRight, ruleFinalLeft, ruleFinalRight, tileID, tileLeftNeighborID)
                        AvailableMoves.append(tempMove)
        # Main: The exit for the move-search is if there is no available moves at this point. If we can't find any moves, then we must be in the terminal assembly.
        if(AvailableMoves == []):
            break
        else:
            # Main: Execute a Random Available Move
            elementNum = randrange(0, len(AvailableMoves))  # Pick a number
            # Pick the corresponding available move from that number
            activeMove = AvailableMoves[elementNum]
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
                destinationTile = ActiveTile(BaseStates[0], 0, 0)

                if(moveDir == "left"):
                    for base_tile in BaseStates:
                        baseLabel = base_tile.returnLabel()

                        # Note: Add an exception branch if the new label isn't from the BaseStates
                        if(baseLabel == moveDestinationLabel):
                            baseColor = base_tile.returnColor()
                            baseAffinities = base_tile.returnRelevantAffinities()
                            baseTransitions = base_tile.returnRelevantTransitions()

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
                else:  # If moveDir == "right"
                    for base_tile in BaseStates:
                        baseLabel = base_tile.returnLabel()

                        # Note: Add an exception branch if the new label isn't from the BaseStates
                        if(baseLabel == moveDestinationLabel):
                            baseColor = base_tile.returnColor()
                            baseAffinities = base_tile.returnRelevantAffinities()
                            baseTransitions = base_tile.returnRelevantTransitions()

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
                # Append the new tile to the assembly
                AssemblyHistory.append(destinationTile)
            # Note: An else-statement for Transition Rules would go here, but the execution of transition rules are causing a lot of urt.
        print("New Assembly:")
        # Main: Print resulting assembly
        for element in AssemblyHistory:
            element.displayBasicInfo()


def Main():
    AssemblyHistory = []  # This will be the list of tiles where we placed a tile in chronological order; this will be essentially our complete history of created assemblies
    # This is the list of basic tiles from the loading-seciton
    BaseStates = LoadFile.BaseStateSet

    PlacingFirstTile(AssemblyHistory, BaseStates)
    PlacingSecondTile(AssemblyHistory, BaseStates)
