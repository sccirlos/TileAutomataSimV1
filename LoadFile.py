from PyQt5.QtWidgets import QFileDialog 
import xml.etree.ElementTree as ET

#I'm sure loading the files will grow to be complicated, so I made this file for anything relating to "Load"
def readxml(file):
    tree = ET.parse(file)
    treeroot = tree.getroot()
    
    for item in treeroot.iter():
        print(item) #item.atrib