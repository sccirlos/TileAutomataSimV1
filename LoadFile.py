from PyQt5.QtWidgets import QFileDialog 
import xml.etree.ElementTree as ET


def readxml(file):
    tree = ET.parse(file)
    treeroot = tree.getroot()
    
    for item in treeroot.iter():
        print(item) #item.atrib