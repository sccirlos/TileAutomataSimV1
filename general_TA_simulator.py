from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtGui import QPainter, QBrush, QPen


from PyQt5.QtCore import Qt
from random import randrange

from assemblyEngine import Engine
from UniversalClasses import System, Assembly, Tile
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


    def Click_EditFile(self):
         # if file loaded 
          # open editorwindow
         self.e = Ui_EditorWindow()
         self.e.show()

class Ui_EditorWindow(QMainWindow, EditorWindow16.Ui_EditorWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

         # action for 'apply' the changes made to the side edit window to the view states side 

         # action for 'save' the changes made to the side edit window to the XML file
        self.pushButton_2.clicked.connect(self.Click_EditSaveAs)

    def Click_EditSaveAs(self):
        print("Save As button clicked")

     # functions - accessing dictionaries for states, rules


if __name__ == "__main__":

     # App Stuff
        app = QApplication(sys.argv)
        w = Ui_MainWindow()
        w.show()

        sys.exit(app.exec_())
        #
