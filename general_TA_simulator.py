from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog 

import TAFileWindow

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
class Ui_MainWindow(QMainWindow, TAFileWindow.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.buttonGroup.buttonClicked[int].connect(self.Click_FileSearch)
        
        self.pushButton_5.clicked.connect(self.Click_Run_Simulation) #Button 5 executes the simulation. Afterwards the window updates to show results

    def Click_Run_Simulation(self): # Run application if everythings good
        err_flag = False
        self.error_label1.setText("")
        self.error_label2.setText("")

        if(Config.spreadsheet1 == ""):
            self.error_label1.setText("Please enter a spreadsheet")
            print("Please enter a spreadsheet")
            err_flag = True
        if(Config.spreadsheet2 == ""):
            self.error_label2.setText("Please enter a spreadsheet")
            print("Please enter a spreadsheet")
            err_flag = True
            
        if(err_flag == False):
            print("all good")
            #display results

    def Click_FileSearch(self, id):
        for button in self.buttonGroup.buttons():
            if button is self.buttonGroup.button(id):
                file = QFileDialog.getOpenFileName(self,"Select Excel Document", "","CSV Files (*.csv)")
                if id == -2:
                    self.lineEdit.setText(file[0])
                elif id == -3:
                    self.lineEdit_2.setText(file[0])



if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Ui_MainWindow()
    w.show()
    sys.exit(app.exec_())