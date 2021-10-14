from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QCheckBox, QMainWindow, QFileDialog, QTableWidgetItem
from PyQt5.QtGui import QPainter, QBrush, QPen


from PyQt5.QtCore import Qt
from random import randrange, seed

from assemblyEngine import Engine
from UniversalClasses import AffinityRule, System, Assembly, Tile, State, TransitionRule
import TAMainWindow
import LoadFile
import SaveFile
import Assembler_Proto
import QuickRotate
import QuickCombine
import EditorWindow16

import sys

# Global Variables
# Note: currentSystem is still global but had to be moved into the loading method
currentAssemblyHistory = []
# General Seeded TA Simulator


# Takes in:
# Seed State
# Set of States
# Set of Transition Rules
# Set of Affinities
# Creates
# A list of events based on transition rules states and affinities
# Add a tile or tiles
# Transition a tile(s)
# Make new assembly
# Attach assemblies
# An Assembly
# Outputs:
#
# GUI showing step by step growth starting with seed state
# Step button
# Keep growing until their are no more rules that apply

class Ui_MainWindow(QMainWindow, TAMainWindow.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        ###Remove Window title bar ####
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        ###Set main background to transparent####
        #self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        ###Shadow effect #####
        self.shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(50)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QtGui.QColor(0, 92, 157, 550))

        ####Apply shadow to central widget####
        self.centralwidget.setGraphicsEffect(self.shadow)

        ###Set window title and Icon####
        #self.setWindowIcon(QtGui.QIcon("path goes here"))
        self.setWindowTitle("TA Simulator")

        ### Minimize window ######
        self.minimize_button.clicked.connect(lambda: self.showMinimized())
        self.minimize_button.setIcon(QtGui.QIcon('Icons/Programming-Minimize-Window-icon.png'))

        ### Close window ####
        self.close_button.clicked.connect(lambda: self.close())
        self.close_button.setIcon(QtGui.QIcon('Icons/X-icon.png'))

        ### Restore/Maximize window ####
        self.maximize_button.clicked.connect(lambda: self.restore_or_maximize_window())
        self.maximize_button.setIcon(QtGui.QIcon('Icons/Programming-Maximize-Window-icon.png'))

        ### Window Size grip to resize window ###
        QtWidgets.QSizeGrip(self.sizeDrag_Button)
        self.sizeDrag_Button.setIcon(QtGui.QIcon('Icons/tabler-icon-resize.png'))

        #Left Menu toggle button
        self.Menu_button.clicked.connect(lambda: self.slideLeftMenu())
        self.Menu_button.setIcon(QtGui.QIcon('Icons/menu_icon.png'))

        # this is "Load" on the "File" menu
        self.Load_button.clicked.connect(self.Click_FileSearch)

        # "Save" from the "File" menu
        self.SaveAs_button.clicked.connect(self.Click_SaveFile)
        self.SaveAs_button.setIcon(QtGui.QIcon('Icons/save-icon.png'))

        self.First_button.clicked.connect(self.first_step)
        self.First_button.setIcon(QtGui.QIcon('Icons/tabler-icon-player-skip-back.png'))

        self.Prev_button.clicked.connect(self.prev_step)
        self.Prev_button.setIcon(QtGui.QIcon('Icons/tabler-icon-player-track-prev.png'))

        self.Play_button.clicked.connect(self.play_sequence)
        self.Play_button.setIcon(QtGui.QIcon('Icons/tabler-icon-player-play.png'))

        self.Next_button.clicked.connect(self.next_step)
        self.Next_button.setIcon(QtGui.QIcon('Icons/tabler-icon-player-track-next.png'))

        self.Last_button.clicked.connect(self.last_step)
        self.Last_button.setIcon(QtGui.QIcon('Icons/tabler-icon-player-skip-forward.png'))

         # "Quick Rotate"
        self.Rotate_button.clicked.connect(self.Click_QuickRotate)

        # "Quick Combine"
        self.Combine_button.clicked.connect(self.Click_QuickCombine)

        self.SlowMode_button.clicked.connect(self.slowMode_toggle)

        # 'Edit' from the Tools menu
        #self.actionEdit.triggered.connect(self.Click_EditFile)
        self.Edit_button.clicked.connect(self.Click_EditFile)

        # Function to Move window on mouse drag event on the title bar
        def moveWindow(e):
            # Detect if the window is  normal size
            if self.isMaximized() == False: #Not maximized
                # Move window only when window is normal size 
                #if left mouse button is clicked (Only accept left mouse button clicks)
                if e.buttons() == Qt.LeftButton:  
                    #Move window 
                    self.move(self.pos() + e.globalPos() - self.clickPosition)
                    self.clickPosition = e.globalPos()
                    e.accept()

        # Add click event/Mouse move event/drag event to the top header to move the window
        self.header.mouseMoveEvent = moveWindow
        self.slide_menu.mouseMoveEvent = moveWindow

        self.time = 0
        self.delay = 0
        self.seedX = self.geometry().width() / 2 
        self.seedY = self.geometry().height() / 2 
        self.clickPosition = QtCore.QPoint(self.geometry().x(), self.geometry().y())

        self.textX = self.seedX + 10
        self.textY = self.seedY + 25

        self.tileSize = 40
        self.textSize = int(self.tileSize / 3)

        self.Engine = None
        self.SysLoaded = False
        self.play = True

        canvas = QtGui.QPixmap(self.geometry().width(), self.geometry().height())
        canvas.fill(Qt.white)
        self.label.setPixmap(canvas)

        self.label_2.setText("")

        
    # Slide left menu function
    def slideLeftMenu(self):                    #ANIMATION NEEDS TO BE WORKED ON SO ITS BEEN TURNED OFF
        # Get current left menu width
        width = self.slide_menu_container.width()

        # If minimized
        if width == 0:
            # Expand menu
            newWidth = 200
            canvas = QtGui.QPixmap(self.geometry().width() - 200, self.geometry().height() - 45) 
            canvas.fill(Qt.white)
            
            self.slide_menu_container.setMaximumWidth(newWidth)
            #self.menu_animation(width, newWidth)
            self.label.setPixmap(canvas)
            #self.open_close_side_bar_btn.setIcon(QtGui.QIcon(u":/icons/icons/chevron-left.svg"))
        # If maximized
        else:
            # Restore menu
            newWidth = 0
            #self.setGeometry(self.x(), self.y(), self.geometry().width() - 100, self.geometry().height())
            #self.menu_animation(width, newWidth)
            self.slide_menu_container.setMaximumWidth(newWidth)

            canvas = QtGui.QPixmap(self.geometry().width(), self.geometry().height() - 45) 
            canvas.fill(Qt.white)
            self.label.setPixmap(canvas)
            
            #self.open_close_side_bar_btn.setIcon(QtGui.QIcon(u":/icons/icons/align-left.svg"))
        
        if self.Engine != None:
            self.draw_tiles(self.Engine.getCurrentAssembly())

    def menu_animation(self, width, newWidth):
        # Animate the transition
        self.animation = QtCore.QPropertyAnimation(self.slide_menu_container, b"maximumWidth")#Animate minimumWidht
        self.animation.setDuration(250)
        self.animation.setStartValue(width)#Start value is the current menu width
        self.animation.setEndValue(newWidth)#end value is the new menu width
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()

    # Add mouse events to the window
    def mousePressEvent(self, event):
        # Get the current position of the mouse
        #print(event.globalPos())
        super().mousePressEvent(event)
        self.clickPosition = event.globalPos()
        # We will use this value to move the window

    def restore_or_maximize_window(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def resizeEvent(self, event):
        # If left menu is closed
        if self.slide_menu_container.width() == 0:
            canvas = QtGui.QPixmap(self.geometry().width(), self.geometry().height() - 45)
        else:
            canvas = QtGui.QPixmap(self.geometry().width() - 200, self.geometry().height() - 45) #prevents a bug that happens if menus open

        canvas.fill(Qt.white)
        self.label.setPixmap(canvas)
        if self.Engine != None:
            self.draw_tiles(self.Engine.getCurrentAssembly())

    def keyPressEvent(self, event):
        #### Moving tiles across screen functions #####
        # up arrow key is pressed
        if event.key() == Qt.Key_W:
            self.seedY = self.seedY - 10
            self.textY = self.textY - 10

        # down arrow key is pressed
        elif event.key() == Qt.Key_S:
            self.seedY = self.seedY + 10
            self.textY = self.textY + 10

        # left arrow key is pressed
        elif event.key() == Qt.Key_A:
            self.seedX = self.seedX - 10
            self.textX = self.textX - 10

        # down arrow key is pressed
        elif event.key() == Qt.Key_D:
            self.seedX = self.seedX + 10
            self.textX = self.textX + 10

        elif event.key() == Qt.Key_H:
            self.first_step()

        elif event.key() == Qt.Key_J:
            self.prev_step()

        elif event.key() == Qt.Key_K:
            self.play_sequence()

        elif event.key() == Qt.Key_L:
            self.next_step()

        elif event.key() == Qt.Key_Semicolon:
            self.last_step()

        if self.Engine != None:
            self.draw_tiles(self.Engine.getCurrentAssembly())

    def wheelEvent(self, event):
        #### Zoom in functions for the scroll wheel ####
        if event.angleDelta().y() == 120:
            self.tileSize = self.tileSize + 10
            self.textX = self.textX + 3
            self.textY = self.textY + 5
        else:
            if self.tileSize > 10:
                self.tileSize = self.tileSize - 10
                self.textX = self.textX - 3
                self.textY = self.textY - 5
        self.textSize = int(self.tileSize / 3)

        if self.Engine != None:
            self.draw_tiles(self.Engine.getCurrentAssembly())

    def draw_tiles(self, assembly):
        painter = QPainter(self.label.pixmap())
        pen = QtGui.QPen()
        brush = QtGui.QBrush()
        font = QtGui.QFont()

        pen.setWidth(3)

        brush.setStyle(Qt.SolidPattern)

        pen.setColor(QtGui.QColor("white"))
        brush.setColor(QtGui.QColor("white"))
        painter.setPen(pen)
        painter.setBrush(brush)
        # this block is drawing a big white rectangle across the screen to "clear" it
        painter.drawRect(0, 0, self.geometry().width(), self.geometry().height())

        font.setFamily("Times")
        font.setBold(True)
        font.setPixelSize(self.textSize)
        painter.setFont(font)
        for tile in assembly.tiles:
            # print(tile[0].color)
            pen.setColor(QtGui.QColor("black"))
            brush.setColor(QtGui.QColor("#" + tile.get_color()))

            painter.setPen(pen)
            painter.setBrush(brush)
            painter.drawRect((tile.x * self.tileSize) + self.seedX, (tile.y * -self.tileSize) + self.seedY, self.tileSize, self.tileSize)
            if len(tile.state.label) > 4:
                painter.drawText((tile.x * self.tileSize) + self.textX, (tile.y * -self.tileSize) + self.textY, tile.state.label[0:3])
            else:
                painter.drawText((tile.x * self.tileSize) + self.textX, (tile.y * -self.tileSize) + self.textY, tile.state.label)

        painter.end()

        if self.Engine.currentIndex != 0:
            self.label_2.setText("Time elapsed: \n" +
                                 str(round(self.time, 2)) + " time steps")
            self.label_3.setText("Current step time: \n" +
                                 str(round(self.Engine.timeTaken(), 2)) + " time steps")
        else:
            self.label_2.setText("Time elapsed: \n 0 time steps")
            self.label_3.setText("Current step time: \n 0 time steps")

        # print(self.Engine.currentIndex)
        self.update()

    def Click_Run_Simulation(self):  # Run application if everythings good
        err_flag = False

        if(err_flag == False):
            self.step = 0
            self.time = 0
            # Assembler_Proto.Main()
            self.draw_tiles(Assembler_Proto.CompleteAssemblyHistory[self.step])

    def Click_FileSearch(self, id):
        self.stop_sequence()
        self.SysLoaded = False
        file = QFileDialog.getOpenFileName(
            self, "Select XML Document", "", "XML Files (*.xml)")
        if file[0] != '':
            # Simulator must clear all of LoadFile's global variables when the user attempts to load something.
            LoadFile.HorizontalAffinityRules.clear()
            LoadFile.VerticalAffinityRules.clear()
            LoadFile.HorizontalTransitionRules.clear()
            LoadFile.VerticalTransitionRules.clear()
            LoadFile.SeedStateSet.clear()
            LoadFile.InitialStateSet.clear()
            LoadFile.CompleteStateSet.clear()

            LoadFile.readxml(file[0])

            # Creating global variables
            global temp
            global states
            global inital_states
            global seed_assembly
            global seed_states
            global vertical_affinities
            global horizontal_affinities
            global vertical_transitions
            global horizontal_transitions

            # Creating a System object from data read.
            temp = LoadFile.Temp
            states = LoadFile.CompleteStateSet
            inital_states = LoadFile.InitialStateSet
            seed_states = LoadFile.SeedStateSet
            vertical_affinities = LoadFile.VerticalAffinityRules
            horizontal_affinities = LoadFile.HorizontalAffinityRules
            vertical_transitions = LoadFile.VerticalTransitionRules
            horizontal_transitions = LoadFile.HorizontalTransitionRules

            self.SysLoaded = True

            # Establish the current system we're working with
            global currentSystem
            currentSystem = System(temp, states, inital_states, seed_states, vertical_affinities,
                                   horizontal_affinities, vertical_transitions, horizontal_transitions)
            print("\nSystem Dictionaries:")
            print("Vertical Affinities:")
            currentSystem.displayVerticalAffinityDict()
            print("Horizontal Affinities:")
            currentSystem.displayHorizontalAffinityDict()
            print("Vertical Transitions:")
            currentSystem.displayVerticalTransitionDict()
            print("Horizontal Transitions:")
            currentSystem.displayHorizontalTransitionDict()

            self.seedX = (self.geometry().width() - 150)/ 2 #the -150 is to account for the slide menu
            self.seedY = self.geometry().height() / 2 
            self.textX = self.seedX + 10
            self.textY = self.seedY + 25

            self.tileSize = 40
            self.textSize = int(self.tileSize / 3)

            self.time = 0
            self.Engine = Engine(currentSystem)
            #a = Assembly()
            #t = Tile(currentSystem.returnSeedStates(), 0, 0)
            # a.tiles.append(t)
            # currentAssemblyHistory.append(a)
            # Assembler_Proto.Main()
            self.draw_tiles(self.Engine.getCurrentAssembly())

    def Click_SaveFile(self):
        # Creating a System object from data read.
        if(self.SysLoaded == True):
            fileName = QFileDialog.getSaveFileName(
                self, "QFileDialog.getSaveFileName()", "", "XML Files (*.xml)")

            if(fileName[0] != ''):
                SaveFile.main(currentSystem, fileName)

    def Click_QuickRotate(self):
        # Make a rotated system based off the current system, and instantly load the new system.
        if(self.SysLoaded == True):
            global currentSystem
            QuickRotate.main(currentSystem)
            currentSystem = QuickRotate.tempSystem
            self.time = 0
            self.Engine = Engine(currentSystem)
            self.draw_tiles(self.Engine.getCurrentAssembly())

    def Click_QuickCombine(self):
        if(self.SysLoaded == True):
            global currentSystem
            file = QFileDialog.getOpenFileName(
                self, "Select XML Document", "", "XML Files (*.xml)")
            if file[0] != '':
                QuickCombine.main(currentSystem, file[0])
            currentSystem.clearVerticalTransitionDict()
            currentSystem.clearHorizontalTransitionDict()
            currentSystem.clearVerticalAffinityDict()
            currentSystem.clearHorizontalAffinityDict()
            currentSystem.translateListsToDicts()
            self.time = 0
            self.Engine = Engine(currentSystem)
            self.draw_tiles(self.Engine.getCurrentAssembly())

    # self.draw_tiles(LoadFile.) #starting assembly goes here
    def slowMode_toggle(self):
        if self.slowMode_Button.isChecked():
            self.delay = 1000
        else:
            self.delay = 0

    def first_step(self):
        if self.SysLoaded == True:
            self.stop_sequence()
            self.Engine.first()
            self.time = 0
            self.draw_tiles(self.Engine.getCurrentAssembly())

    def prev_step(self):
        self.stop_sequence()
        if self.SysLoaded == True:
            if self.Engine.currentIndex > 0:
                self.Engine.back()
                # Might need to go below
                self.time = self.time - (self.Engine.timeTaken())
                self.draw_tiles(self.Engine.getCurrentAssembly())

    def next_step(self):
        self.stop_sequence()
        if self.SysLoaded == True:
            if self.Engine.step() != -1:
                # Might need to go above
                self.time = self.time + (self.Engine.timeTaken())
                self.draw_tiles(self.Engine.getCurrentAssembly())

    def last_step(self):
        self.stop_sequence()
        if self.SysLoaded == True:
            while (self.Engine.step() != -1):
                self.time = self.time + (self.Engine.timeTaken())

            self.draw_tiles(self.Engine.getCurrentAssembly())

    def play_sequence(self):
        if self.SysLoaded == True:
            if self.play == False:
                self.Play_button.setIcon(QtGui.QIcon('Icons/tabler-icon-player-pause.png'))
                self.play = True
                while((self.Engine.step() != -1) and self.play == True):
                    print(self.Engine.currentIndex)
                    self.time = self.time + (self.Engine.timeTaken())

                    loop = QtCore.QEventLoop()
                    if self.Engine.currentIndex != 0:
                        QtCore.QTimer.singleShot(
                            int(self.delay * self.Engine.timeTaken()), loop.quit)
                    else:
                        QtCore.QTimer.singleShot(self.delay, loop.quit)
                    loop.exec_()

                    self.draw_tiles(self.Engine.getCurrentAssembly())
                    # if self.Engine.currentIndex != 0: #and self.Engine.currentIndex < self.Engine.lastIndex:

                # self.step = len(self.Engine.assemblyList) - 1 #this line is here to prevent a crash that happens if you click last after play finishes
                self.stop_sequence()
                self.Play_button.setIcon(QtGui.QIcon('Icons/tabler-icon-player-play.png'))

            if self.play == True:   
                self.Play_button.setIcon(QtGui.QIcon('Icons/tabler-icon-player-play.png'))
                self.stop_sequence()

    def stop_sequence(self):
        self.play = False


    # opens editor window 
    def Click_EditFile(self):
         # if system loaded, open editorwindow
        if self.SysLoaded == True:
            self.e = Ui_EditorWindow(self.Engine)
            self.e.show()
        else: 
            print("Please load a file to edit.")
# add self, engine - then fill the table 
# engine has the system 


# do i need another function per page??
class Ui_EditorWindow(QMainWindow, EditorWindow16.Ui_EditorWindow):
    def __init__(self, engine):
        super().__init__()
        self.setupUi(self)
        self.Engine = engine
        self.system = engine.system
         # set row count state table
        self.newStateIndex = len(self.system.states)
        self.tableWidget.setRowCount(len(self.system.states))
        print(len(self.system.states))
         # set row count affinity table
        self.newAffinityIndex = (len(self.system.vertical_affinities_list)) + (len(self.system.horizontal_affinities_list))
        self.tableWidget_2.setRowCount(len(self.system.vertical_affinities_list) + len(self.system.horizontal_affinities_list))
        print(len(self.system.vertical_affinities_list) + len(self.system.horizontal_affinities_list))
         # set row count transition table
        self.newTransitionIndex = (len(self.system.vertical_transitions_list)) + (len(self.system.horizontal_transitions_list))
        self.tableWidget_3.setRowCount(len(self.system.vertical_transitions_list) + len(self.system.horizontal_transitions_list))
        print(len(self.system.vertical_transitions_list) + len(self.system.horizontal_transitions_list))


         # connect the color change
        self.tableWidget.cellChanged.connect(self.cellchanged)

         # filling in table 2 with vertical affinities
        r = 0
        for af in self.system.vertical_affinities_list:
            label1 = QTableWidgetItem()
            label1.setText(af.returnLabel1()) 
            label1.setTextAlignment(Qt.AlignCenter)
            label2 = QTableWidgetItem()
            label2.setText(af.returnLabel2())
            label2.setTextAlignment(Qt.AlignCenter)
            self.tableWidget_2.setItem(r, 0, label1)
            self.tableWidget_2.setItem(r, 1, label2)
           
            direc = QTableWidgetItem()
            direc.setText(af.returnDir())
            direc.setTextAlignment(Qt.AlignCenter)
            self.tableWidget_2.setItem(r, 2, direc)
            glue = QTableWidgetItem()
            glue.setText(af.returnStr())
            glue.setTextAlignment(Qt.AlignCenter)
            self.tableWidget_2.setItem(r, 3, glue)
            r += 1

        # filling in table 2 with horizontal affinities
        for afH in self.system.horizontal_affinities_list:
            label1HR = QTableWidgetItem()
            label1HR.setText(afH.returnLabel1())
            label1HR.setTextAlignment(Qt.AlignCenter)
            self.tableWidget_2.setItem(r, 0, label1HR)
            label2HR = QTableWidgetItem()
            label2HR.setText(afH.returnLabel2())
            label2HR.setTextAlignment(Qt.AlignCenter)
            self.tableWidget_2.setItem(r, 1, label2HR)
            direcHR = QTableWidgetItem()
            direcHR.setText(afH.returnDir())
            direcHR.setTextAlignment(Qt.AlignCenter)
            self.tableWidget_2.setItem(r, 2, direcHR)
            glueHR = QTableWidgetItem()
            glueHR.setText(afH.returnStr())
            glueHR.setTextAlignment(Qt.AlignCenter)
            self.tableWidget_2.setItem(r, 3, glueHR)
            r += 1


        # filling in table 3 with vertical transitions
        r = 0
        for trV in self.system.vertical_transitions_list:
            stateVT1 = QTableWidgetItem()
            stateVT1.setText(trV.returnLabel1())
            stateVT1.setTextAlignment(Qt.AlignCenter)
            self.tableWidget_3.setItem(r, 0, stateVT1)
            stateVT2 = QTableWidgetItem()
            stateVT2.setText(trV.returnLabel2())
            stateVT2.setTextAlignment(Qt.AlignCenter)
            self.tableWidget_3.setItem(r, 1, stateVT2)
            finalVT1 = QTableWidgetItem()
            finalVT1.setText(trV.returnLabel1Final())
            finalVT1.setTextAlignment(Qt.AlignCenter)
            self.tableWidget_3.setItem(r, 3, finalVT1)
            finalVT2 = QTableWidgetItem()
            finalVT2.setText(trV.returnLabel2Final())
            finalVT2.setTextAlignment(Qt.AlignCenter)
            self.tableWidget_3.setItem(r, 4, finalVT2)
            direcVT = QTableWidgetItem()
            direcVT.setText(trV.returnDir())
            direcVT.setTextAlignment(Qt.AlignCenter)
            self.tableWidget_3.setItem(r, 5, direcVT)
            r += 1

        # filling in table 3 with horizontal transitions
        for trH in self.system.horizontal_transitions_list:
            stateHT1 = QTableWidgetItem()
            stateHT1.setText(trH.returnLabel1())
            stateHT1.setTextAlignment(Qt.AlignCenter)
            self.tableWidget_3.setItem(r, 0, stateHT1)
            stateHT2 = QTableWidgetItem()
            stateHT2.setText(trH.returnLabel2())
            stateHT2.setTextAlignment(Qt.AlignCenter)
            self.tableWidget_3.setItem(r, 1, stateHT2)
            finalHT1 = QTableWidgetItem()
            finalHT1.setText(trH.returnLabel1Final())
            finalHT1.setTextAlignment(Qt.AlignCenter)
            self.tableWidget_3.setItem(r, 3, finalHT1)
            finalHT2 = QTableWidgetItem()
            finalHT2.setText(trH.returnLabel2Final())
            finalHT2.setTextAlignment(Qt.AlignCenter)
            self.tableWidget_3.setItem(r, 4, finalHT2)
            direcHT = QTableWidgetItem()
            direcHT.setText(trH.returnDir())
            direcHT.setTextAlignment(Qt.AlignCenter)
            self.tableWidget_3.setItem(r, 5, direcHT)
            r += 1


        # filling in table 1 with states
        r = 0
        for s in self.system.states:
            color_cell = QTableWidgetItem()
            color_cell.setText(s.get_color())
            color_cell.setTextAlignment(Qt.AlignCenter)
            color_cell.setForeground(QtGui.QColor("#" + s.get_color()))
            color_cell.setBackground(QtGui.QColor("#" + s.get_color()))
            self.tableWidget.setItem(r, 0, color_cell)

            label_cell = QTableWidgetItem()
            label_cell.setText(s.get_label())
            label_cell.setTextAlignment(Qt.AlignCenter)
            self.tableWidget.setItem(r, 1, label_cell)

            seedWidget = QtWidgets.QWidget()
            seedCheckbox = QCheckBox()
            seedChkLayout = QtWidgets.QHBoxLayout(seedWidget)
            seedChkLayout.addWidget(seedCheckbox)
            seedChkLayout.setAlignment(Qt.AlignCenter)
            seedChkLayout.setContentsMargins(0,0,0,0)
            self.tableWidget.setCellWidget(r, 2, seedWidget)
            for sstate in self.system.seed_states:
                if sstate.get_label() == s.get_label():
                    seedCheckbox.setChecked(True)
            
            initialWidget = QtWidgets.QWidget()
            initialCheckbox = QCheckBox()
            initialChkLayout = QtWidgets.QHBoxLayout(initialWidget)
            initialChkLayout.addWidget(initialCheckbox)
            initialChkLayout.setAlignment(Qt.AlignCenter)
            initialChkLayout.setContentsMargins(0,0,0,0)
            self.tableWidget.setCellWidget(r, 3, initialWidget)
            for istate in self.system.initial_states:
                if istate.get_label() == s.get_label():
                    initialCheckbox.setChecked(True)
            
            r += 1

    
     # action for 'apply' the changes made to the side edit window to the view states side 
        self.pushButton.clicked.connect(self.Click_EditApply)
         # action for 'save' the changes made to the side edit window to the XML file
        self.pushButton_2.clicked.connect(self.Click_EditSaveAs)
        self.pushButton_3.clicked.connect(self.Click_AddRowStates)
        self.pushButton_4.clicked.connect(self.Click_AddRowAff)
        self.pushButton_5.clicked.connect(self.Click_AddRowTrans)


    # for 'add state'
    def cellchanged(self, row, col):
        # only do anything is we are in the color column (0)
        if col == 0:
            print("in color column")

            color_cell = self.tableWidget.item(row, col)
            color = color_cell.text()
            color_cell.setForeground(QtGui.QColor("#" + color))
            color_cell.setBackground(QtGui.QColor("#" + color))

    # would have to change widget geometry here as well? 
    # Yes
    def Click_AddRowStates(self):
        print("Add Row in States clicked")
        newrow = self.tableWidget.rowCount()
        self.tableWidget.setRowCount(newrow + 1)

        color_cell = QTableWidgetItem()
        color_cell.setTextAlignment(Qt.AlignCenter)
        self.tableWidget.setItem(newrow, 0, color_cell)

        label_cell = QTableWidgetItem()
        label_cell.setTextAlignment(Qt.AlignCenter)
        self.tableWidget.setItem(newrow, 1, label_cell)

        seedWidget = QtWidgets.QWidget()
        seedCheckbox = QCheckBox()
        seedChkLayout = QtWidgets.QHBoxLayout(seedWidget)
        seedChkLayout.addWidget(seedCheckbox)
        seedChkLayout.setAlignment(Qt.AlignCenter)
        seedChkLayout.setContentsMargins(0,0,0,0)
        self.tableWidget.setCellWidget(newrow, 2, seedWidget)

        initialWidget = QtWidgets.QWidget()
        initialCheckbox = QCheckBox()
        initialChkLayout = QtWidgets.QHBoxLayout(initialWidget)
        initialChkLayout.addWidget(initialCheckbox)
        initialChkLayout.setAlignment(Qt.AlignCenter)
        initialChkLayout.setContentsMargins(0,0,0,0)       
        self.tableWidget.setCellWidget(newrow, 3, initialWidget)
        
     # To add new row entered by user as a rule
    def Click_AddRowAff(self):
        print("Add Row in Affinities clicked")
        newrow = self.tableWidget_2.rowCount()
        self.tableWidget_2.setRowCount(newrow + 1)

        label1 = QTableWidgetItem()
        label1.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_2.setItem(newrow, 0, label1)

        label2 = QTableWidgetItem()
        label2.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_2.setItem(newrow, 1, label2)

        direc = QTableWidgetItem()  
        direc.setTextAlignment(Qt.AlignCenter)      
        self.tableWidget_2.setItem(newrow, 2, direc)

        glue = QTableWidgetItem()
        glue.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_2.setItem(newrow, 3, glue)


    def Click_AddRowTrans(self):
        print("Add Row in Transitions clicked")
        newrow = self.tableWidget_3.rowCount()
        self.tableWidget_3.setRowCount(newrow + 1)

        tLabel1 = QTableWidgetItem()
        tLabel1.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_3.setItem(newrow, 0, tLabel1)

        tLabel2 = QTableWidgetItem()
        tLabel2.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_3.setItem(newrow, 1, tLabel2)

        tFinal1 = QTableWidgetItem()
        tFinal1.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_3.setItem(newrow, 3, tFinal1)

        tFinal2 = QTableWidgetItem()
        tFinal2.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_3.setItem(newrow, 4, tFinal2)

        tDirec = QTableWidgetItem()
        tDirec.setTextAlignment(Qt.AlignCenter)
        self.tableWidget_3.setItem(newrow, 5, tDirec)


    def Click_EditApply(self):
        print("Apply button clicked")

        # go through new rows, create states, add states to system
        for row in range(self.newStateIndex, self.tableWidget.rowCount()):
            color_cell = self.tableWidget.item(row, 0)
            label_cell = self.tableWidget.item(row, 1)
            initialCheckbox = self.tableWidget.cellWidget(row, 3)

            color = color_cell.text()
            label = label_cell.text()
            ## Qwidget object has no attribute isChecked!! 
            # crash on "Apply as" click
            initial = initialCheckbox.isChecked()

            s = State(label, color)

            self.system.add_State(s)

            if initial:
                self.system.add_Initial_State(s)

        for row in range(self.newAffinityIndex, self.tableWidget_2.rowCount()):
            label1 = self.tableWidget_2.item(row, 0)
            label2 = self.tableWidget_2.item(row, 1)
            
            direc = self.tableWidget_2.item(row, 2)
            glue = self.tableWidget_2.item(row,3)

            lab1 = label1.text()
            lab2 = label2.text()
            dire = direc.text()
            glu = glue.text()

            afRule = AffinityRule(lab1, lab2, dire, glu)

            self.system.add_affinity(afRule)

        for row in range(self.newTransitionIndex, self.tableWidget_3.rowCount()):
            tLabel1 = self.tableWidget_3.item(row, 0)
            tLabel2 = self.tableWidget_3.item(row, 1)
            tFinal1 = self.tableWidget_3.item(row, 3)
            tFinal2 = self.tableWidget_3.item(row, 4)
            tDirec = self.tableWidget_3.item(row, 5)

            tLab1 = tLabel1.text()
            tLab2 = tLabel2.text()
            tFin1 = tFinal1.text()
            tFin2 = tFinal2.text()
            tDir = tDirec.text()

            trRule = TransitionRule(tLab1, tLab2, tFin1, tFin2, tDir)

            self.system.add_transition(trRule)


     # working on this currently
    def Click_EditSaveAs(self):
        print("Save As button clicked")
    

if __name__ == "__main__":
     # App Stuff
        app = QApplication(sys.argv)
        w = Ui_MainWindow()
        w.show()
        sys.exit(app.exec_())
        #
