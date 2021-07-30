from PyQt5.QtWidgets import QFileDialog 
import xml.etree.ElementTree as ET
    
TileSet = [] #Collection of Available Tiles
AffinityRules = [] #Collection of Affinity Rules
TransitionRules = [] #Collection of Transition Rules
class Tile:
    def __init__(self, label,x, y, color):
        self.label = label #The tile's label
        self.x = x #The tile's starting x-position; Can be used as an int
        self.y = y #The tile's starting y-position; Can be used as an int
        self.color = color
        self.relevantAffinities = [] #Which elements from the AffinityRules list directly involve this tile?
        self.relevantTranstitions = [] #Which elements from the TransitionRules list directly involve this tile?
    def displayBasic(self): #Displays the basic information
        print("Label: "+self.label+"; Spawning X-Coordinate: "+self.x+"; Spawning Y-Coordinate: "+self.y+"; Color: "+self.color)
    def displayRelevantRules(self):
        print("Relevant rules for "+self.label+":") 
        print("\tAffinity Rules:") #Printing relevant affinity rules
        if(self.relevantAffinities == []): #If none are found...
            print("\t\t*None")
        else: #If any are found...
            for element in self.relevantAffinities:
                if(element.returnDir() == "left"):
                    print("\t\t*"+element.returnDestination()+" connects to the left of "+element.returnOrigin()+" -> ["+element.returnDestination()+","+element.returnOrigin()+"]")
                else:
                    print("\t\t*"+element.returnDestination()+" connects to the right of "+element.returnOrigin()+" ->["+element.returnOrigin()+","+element.returnDestination()+"]")
        print("\tTransition Rules:") #Printing relevant transition rules
        if(self.relevantTranstitions == []):#If none are found...
            print("\t\t*None")
        else: #If any are found...
            for element in self.relevantTranstitions:
                print("\t\t*["+element.returnOriginalLeft()+","+element.returnOriginalRight()+"] -> ["+element.returnFinalLeft()+","+element.returnFinalRight()+"]") 
    #Basic Getters
    def returnLabel(self):
        return self.label
    def returnX(self):
        return self.x
    def returnY(self):
        return self.y
    def returnColor(self):
        return self.color
    def returnRelevantAffinities(self):
        return self.relevantAffinities
    def returnRelevantTransitions(self):
        return self.relevantTranstitions
    #Rule Appenders
    def addAffinity(self, rule):
        self.relevantAffinities.append(rule)
    def addTransition(self, rule):
        self.relevantTranstitions.append(rule)


class AffinityRule:
    def __init__(self, origin, dir, destination):
        self.origin = origin #Which label will get a new neighbor?
        self.dir = dir #Which direction will the new neighbor be placed?
        self.destination = destination #Who's the new neighbor?
    def displayRule(self):
        if(self.dir == "left"):
            print(self.destination+" connects to the left of "+self.origin+" -> ["+self.destination+","+self.origin+"]")
        else:
            print(self.destination+" connects to the right of "+self.origin+" ->["+self.origin+","+self.destination+"]")
    def returnOrigin(self):
        return self.origin
    def returnDir(self):
        return self.dir
    def returnDestination(self):
        return self.destination

class TransitionRule:
    def __init__(self, originalLeft, originalRight, finalLeft, finalRight):
        self.originalLeft = originalLeft
        self.originalRight = originalRight
        self.finalLeft = finalLeft
        self.finalRight = finalRight
    def displayRule(self):
        print("["+self.originalLeft+","+self.originalRight+"] -> ["+self.finalLeft+","+self.finalRight+"]")
    def returnOriginalLeft(self):
        return self.originalLeft
    def returnOriginalRight(self):
        return self.originalRight
    def returnFinalLeft(self):
        return self.finalLeft
    def returnFinalRight(self):
        return self.finalRight
        
#I'm sure loading the files will grow to be complicated, so I made this file for anything relating to "Load"
def readxml(file):
    tree = ET.parse(file)
    treeroot = tree.getroot()

    #Main: Setting TileSet
    for tile_tag in treeroot.findall('TileTypes/Tile'):
        label = tile_tag.get('Label')
        xPosition = tile_tag.find('x').text
        yPosition = tile_tag.find('y').text
        color = tile_tag.find('color').text
        tempTile = Tile(label, xPosition, yPosition, color)
        TileSet.append(tempTile)
    print("Inital Tile Set:")
    for element in TileSet:
        element.displayBasic()

    #Main: Setting System Rules
    #Sub: Setting Affinity Rules
    for rule_tag in treeroot.findall('System/AffinityRules/Rule'):
        origin = rule_tag.get('Tile')
        for direction in rule_tag:
            dir = direction.tag
            destination = direction.text.replace("\"", "")
            tempRule = AffinityRule(origin, dir, destination)
            AffinityRules.append(tempRule)
    print("\nAffinity Rules:")
    for element in AffinityRules:
        element.displayRule()

    #Sub: Setting Transition Rules
    for rule_tag in treeroot.findall('System/TransitionRules/Rule'):
        originalLeft = rule_tag.get('Left')
        originalRight = rule_tag.get('Right')
        finalLeft = rule_tag.find('left').text.replace("\"", "")
        finalRight = rule_tag.find('right').text.replace("\"", "")
        tempRule = TransitionRule(originalLeft, originalRight, finalLeft, finalRight)
        TransitionRules.append(tempRule)
    print("\nTransition Rules:")
    for element in TransitionRules:
        element.displayRule()
    print("")

    #Main: Assigning Releveant Affinity and Transition Rules to Each Base Tile Type
    for element in TileSet: #For each tile in the base tile set...
        for rule in AffinityRules: #Check through the affinity rules...
            if(element.returnLabel() == rule.returnOrigin()): #And add any relevant affinity rules.
                element.addAffinity(rule)
        for rule in TransitionRules: #Then check through the transition rules...
            if(element.returnLabel() == rule.returnOriginalLeft() or element.returnLabel() == rule.returnOriginalRight()): #And add any relevant transition rules.
                element.addTransition(rule)
        element.displayRelevantRules()