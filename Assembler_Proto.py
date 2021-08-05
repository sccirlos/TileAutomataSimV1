from os import X_OK
import LoadFile
from random import randrange

class ActiveTile:
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
    #Getters
    def returnCoordinates(self):
        return (str(self.x)+", "+str(self.y))
    #Setters
    def setLeftNeighbor(self, neighbor):
        self.left = neighbor
    def setRightNeighbor(self, neighbor):
        self.right = neighbor
    def setX(self, num):
        self.x = num
    def setY(self, num):
        self.y = num
    #Displayers
    def displayBasicInfo(self):
        print("\t-Label: "+self.label+"; X-Coordinate: "+str(self.x)+"; Y-Coordinate: "+str(self.y)+"; Color: "+self.color)


def PlacingFirstTile(CurrentAssemblyHistory, BaseStates):
    elementNum = randrange(0, len(BaseStates))
    tempActiveTile = ActiveTile(BaseStates[elementNum], 0, 0) #Create an instance of the 1st active tile
    CurrentAssemblyHistory.append(tempActiveTile)




def Main():
    AssemblyHistory = [] #This will be the list of tiles where we placed a tile in chronological order; this will be essentially our complete history of created assemblies
    BaseStates = LoadFile.BaseStateSet #This is the list of basic tiles from the loading-seciton

    PlacingFirstTile(AssemblyHistory, BaseStates)
    print("Current Assembly:")
    for element in AssemblyHistory:
        element.displayBasicInfo()