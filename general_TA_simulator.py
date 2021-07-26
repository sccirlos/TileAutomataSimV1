from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog 

import TAMainWindow
import LoadFile

import sys
#General Seeded TA Simulator 


#Takes in:
    #Seed State 
    #Set of States
    #Set of Transition Rules
    #Set of Affinities
# Creates
    # A list of events based on transition rules states and affinities
        # Add a tile or tiles
        # Transition a tile(s)
        # Make new assembly
        # Attach assemblies
    # An Assembly
#Outputs:
    # 
    #GUI showing step by step growth starting with seed state
    #Step button
    #Keep growing until their are no more rules that apply


# Step 1: Command Line with File Select 
#         
class Ui_MainWindow(QMainWindow, TAMainWindow.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.actionLoad.triggered.connect(self.Click_FileSearch) #this is "Load" on the "File" menu
        
        self.pushButton.clicked.connect(self.Click_Run_Simulation) #this button executes the simulation. Afterwards the window updates to show results

    def Click_Run_Simulation(self): # Run application if everythings good
        err_flag = False
        
            
        if(err_flag == False):
            print("all good")
            #display results

    def Click_FileSearch(self, id):
        file = QFileDialog.getOpenFileName(self,"Select XML Document", "","XML Files (*.xml)")
        LoadFile.readxml(file[0])       



if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Ui_MainWindow()
    w.show()
    sys.exit(app.exec_())