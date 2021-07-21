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
        self.error_label3.setText("")
        self.error_label4.setText("")

        if(self.lineEdit.text() == ""):
            self.error_label1.setText("Please enter file 1")
            print("Please enter file 1")
            err_flag = True
        if(self.lineEdit_2.text() == ""):
            self.error_label2.setText("Please enter file 2")
            print("Please enter file 2")
            err_flag = True
        if(self.lineEdit_3.text() == ""):
            self.error_label3.setText("Please enter file 3")
            print("Please enter file 3")
            err_flag = True
        if(self.lineEdit_4.text() == ""):
            self.error_label4.setText("Please enter file 4")
            print("Please enter file 4")
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
                elif id == -4:
                    self.lineEdit_3.setText(file[0])
                elif id == -5:
                    self.lineEdit_4.setText(file[0])



if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Ui_MainWindow()
    w.show()
    sys.exit(app.exec_())