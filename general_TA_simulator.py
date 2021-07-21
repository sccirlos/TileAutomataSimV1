from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog 

import TAFileWindow
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
        self.setWindowIcon(QtGui.QIcon('Verdant_Green.PNG'))

        self.buttonGroup.buttonClicked[int].connect(self.Click_FileSearch)
        
        self.pushButton_3.clicked.connect(self.Click_Calculations) #Button 3 executes the calculations. Afterwards the window updates to show results

        #the progress bar will have to be on a popup window that displays the messages in Data Processing.py

    def Click_Calculations(self): # Run Data App.py if everythings good
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
            self.threadpool = QtCore.QThreadPool()      
            
            self.l = LoadingWindow()
            self.l.show()
            worker = Worker()
            worker.signals.finished.connect(self.DisplayResults)
            worker.signals.progress.connect(self.l.LoadProgress)
            self.threadpool.start(worker)
            
            for x in range(10):
                self.l.LoadProgress(x*10)
                loop = QtCore.QEventLoop()
                QtCore.QTimer.singleShot(1700, loop.quit)
                loop.exec_()
                self.l.LoadProgress(x*10 + 5)
                self.l.label_2.setText(Config.load_messages[x])
            
    def DisplayResults(self):
        self.l.close()
        self.g = GraphMainWindow()
        self.g.show()

    def Click_FileSearch(self, id):
        for button in self.buttonGroup.buttons():
            if button is self.buttonGroup.button(id):
                file = QFileDialog.getOpenFileName(self,"Select Excel Document", "","CSV Files (*.csv)")
                if id == -2:
                    Config.spreadsheet1 = file[0]
                    self.lineEdit.setText(Config.spreadsheet1)
                elif id == -3:
                    Config.spreadsheet2 = file[0]
                    self.lineEdit_2.setText(Config.spreadsheet2)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Ui_MainWindow()
    w.show()
    sys.exit(app.exec_())