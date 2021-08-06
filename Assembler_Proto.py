from os import X_OK
import LoadFile
from random import randrange

class ActiveTile:
    ID = 0
    def __init__(self, base_tile, x, y):
        #Attributes Inherited from a Base Tile
        self.label = base_tile.returnLabel()
        self.color = base_tile.returnColor()
        self.relevantAffinities = base_tile.returnRelevantAffinities()
        self.relevantTranstitions = base_tile.returnRelevantTransitions()
        #New Attributes for Active Tiles for Positional Tracking
        self.left = None #Left Neighbor
        self.right = None #Right Neighbor
        self.x = x #X-coordinate in the grid
        self.y = y #Y-coordinate in the grid
        self.ID = ActiveTile.ID
        ActiveTile.ID += 1
    #Getters
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
    #Setters
    def setLabel(self, label): #Will need to change this later because this only allows for a superficial transition (aka, just the label changes)
        self.label = label
    def setLeft(self, neighbor):
        self.left = neighbor
    def setRight(self, neighbor):
        self.right = neighbor
    #Displayers
    def displayBasicInfo(self):
        print("\t-Label: "+self.label+"; X-Coordinate: "+str(self.x)+"; Y-Coordinate: "+str(self.y)+"; Color: "+self.color)
class AvailableAffinity:
    def __init__(self, origin, dir, destination, ID):
        self.origin = origin
        self.dir = dir
        self.destination = destination
        self.ID = ID #Active Tile's ID; AKA, which tile from the assembly will this rule be executed on
        self.ruleType = "Affinity"
    #Getters
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
    def __init__(self, originalLeft, originalRight, finalLeft, finalRight, ID):
        self.originalLeft = originalLeft
        self.originalRight = originalRight
        self.finalLeft = finalLeft
        self.finalRight = finalRight
        self.ID = ID
        self.ruleType = "Transition"
    #Getters
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
    def returnRuleType(self):
        return self.ruleType
    



def PlacingFirstTile(AssemblyHistory, BaseStates):
    elementNum = randrange(0, len(BaseStates))
    tempActiveTile = ActiveTile(BaseStates[elementNum], 0, 0) #Create an instance of the 1st active tile
    AssemblyHistory.append(tempActiveTile)
    print("Current Assembly:")
    for element in AssemblyHistory:
        element.displayBasicInfo()

def PlacingSecondTile(AssemblyHistory, BaseStates):
    #Main: Find out what are our available moves.
    AvailableMoves = []
    #Checking each tile individually...
    for tile in AssemblyHistory:
        tileID = tile.returnID()
        tileLabel = tile.returnLabel()
        tileLeftNeighbor = tile.returnLeft()
        tileRightNeighbor = tile.returnRight()
        tileAffinities = tile.returnRelevantAffinities()
        tileTransitions = tile.returnRelevantTransitions()
        #Check through the current tile's affinity rules...
        for rule in tileAffinities:
            ruleOrigin = rule.returnOrigin()
            ruleDir = rule.returnDir()
            ruleDestination = rule.returnDestination()
            
            if(tileLeftNeighbor != None and tileRightNeighbor != None): #If the tile's left and right sides are occupied, skip the entire affinity check
                break
            else:
                #If we have a leftward affinity, and the left side is open...
                if(ruleDir == 'left' and tileLeftNeighbor == None):
                    #Pick the rule and attach it to AvailableMoves[]
                    tempMove = AvailableAffinity(ruleOrigin, ruleDir, ruleDestination, tileID)
                    AvailableMoves.append(tempMove)
                #Same thing if we have a rightward affinity and the right side is open...
                if(ruleDir == 'right' and tileRightNeighbor == None):
                    tempMove = AvailableAffinity(ruleOrigin, ruleDir, ruleDestination, tileID)
                    AvailableMoves.append(tempMove)
        #Then check the current tile's transition rules...
        for rule in tileTransitions:
            ruleOriginalLeft = rule.returnOriginalLeft()
            ruleOriginalRight = rule.returnOriginalRight()
            ruleFinalLeft = rule.returnFinalLeft()
            ruleFinalRight = rule.returnFinalRight()

            if(tileLeftNeighbor == None and tileRightNeighbor == None):#If the tile has no neighbors, then there's no way to make a transition, so skip the entire transition check
                break
            else:
                tileLeftNeighborLabel = tileLeftNeighbor.returnLabel()
                tileRightNeighborLabel = tileRightNeighbor.returnLabel()
                #If the current tile is the 'left' tile, then we must check the 'right'. If everything is correct, add the transition rule to AvailableMoves[].
                if(tileLabel == ruleOriginalLeft and tileRightNeighborLabel == ruleOriginalRight):
                    tempMove = AvailableTransition(ruleOriginalLeft, ruleOriginalRight, ruleFinalLeft, ruleFinalRight, tileID)
                    AvailableMoves.append(tempMove)
                #Same thing as before: if the current tile is the 'right' tile, then we must check the 'left'...
                if(tileLabel == ruleOriginalRight and tileLeftNeighborLabel == ruleOriginalLeft):
                    tempMove = AvailableTransition(ruleOriginalLeft, ruleOriginalRight, ruleFinalLeft, ruleFinalRight, tileID)
                    AvailableMoves.append(tempMove)
    
    #Main: Execute a Random Available Move
    


def Main():
    AssemblyHistory = [] #This will be the list of tiles where we placed a tile in chronological order; this will be essentially our complete history of created assemblies
    BaseStates = LoadFile.BaseStateSet #This is the list of basic tiles from the loading-seciton

    PlacingFirstTile(AssemblyHistory, BaseStates)
    PlacingSecondTile(AssemblyHistory, BaseStates)
