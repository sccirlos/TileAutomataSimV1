import LoadFile
from random import randrange

class ActiveTile:
    def __init__(self, base_tile):
        #Attributes Inherited from a Base Tile
        self.label = base_tile.returnLabel()
        self.x = base_tile.returnX()
        self.y = base_tile.returnY()
        self.color = base_tile.returnColor()
        self.relevantAffinities = base_tile.returnRelevantAffinities()
        self.relevantTranstitions = base_tile.returnRelevantTransitions()
        #New Attributes for Active Tiles for Positional Tracking
        self.left = None
        self.right = None
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
        print("\t-Label: "+self.label+"; X-Coordinate: "+self.x+"; Y-Coordinate: "+self.y+"; Color: "+self.color)


def PlacingFirstTile(CurrentAssemblyHistory, BaseTiles):
    elementNum = randrange(0, len(BaseTiles))
    tempActiveTile = ActiveTile(BaseTiles[elementNum]) #Create an instance of the 1st active tile
    CurrentAssemblyHistory.append(tempActiveTile)




def Main():
    CurrentAssemblyHistory = [] #This list will contain the order of the tiles placed for an assembly; this can be turned into/treated as a tree later on if wanted
    BaseTiles = LoadFile.TileSet #This is the list of basic tiles from the loading-seciton
    CompleteAssemblyHistory = [] #This list will contain the complete history of created assemblies; this is basically going to be a list of past Assemblies

    PlacingFirstTile(CurrentAssemblyHistory, BaseTiles)
    CompleteAssemblyHistory.append(CurrentAssemblyHistory)
    print("Current Assembly:")
    for element in CurrentAssemblyHistory:
        element.displayBasicInfo()




