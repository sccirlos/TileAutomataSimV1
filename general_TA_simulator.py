from os import stat
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QFileDialog, QWidget, QVBoxLayout
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor, QFont

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
import QuickReflect

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
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

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
        self.minimize_button.setIcon(QtGui.QIcon(
            'Icons/Programming-Minimize-Window-icon.png'))

        ### Close window ####
        self.close_button.clicked.connect(lambda: self.close())
        self.close_button.setIcon(QtGui.QIcon('Icons/X-icon.png'))

        ### Restore/Maximize window ####
        self.maximize_button.clicked.connect(
            lambda: self.restore_or_maximize_window())
        self.maximize_button.setIcon(QtGui.QIcon(
            'Icons/Programming-Maximize-Window-icon.png'))

        ### Window Size grip to resize window ###
        QtWidgets.QSizeGrip(self.sizeDrag_Button)
        self.sizeDrag_Button.setIcon(
            QtGui.QIcon('Icons/tabler-icon-resize.png'))

        # Left Menu toggle button
        self.Menu_button.clicked.connect(lambda: self.slideLeftMenu())
        self.Menu_button.setIcon(QtGui.QIcon('Icons/menu_icon.png'))

        # this is "Load" on the "File" menu
        self.Load_button.clicked.connect(self.Click_FileSearch)

        # "Save" from the "File" menu
        self.SaveAs_button.clicked.connect(self.Click_SaveFile)
        self.SaveAs_button.setIcon(QtGui.QIcon('Icons/save-icon.png'))

        self.First_button.clicked.connect(self.first_step)
        self.First_button.setIcon(QtGui.QIcon(
            'Icons/tabler-icon-player-skip-back.png'))

        self.Prev_button.clicked.connect(self.prev_step)
        self.Prev_button.setIcon(QtGui.QIcon(
            'Icons/tabler-icon-player-track-prev.png'))

        self.Play_button.clicked.connect(self.play_sequence)
        self.Play_button.setIcon(QtGui.QIcon(
            'Icons/tabler-icon-player-play.png'))

        self.Next_button.clicked.connect(self.next_step)
        self.Next_button.setIcon(QtGui.QIcon(
            'Icons/tabler-icon-player-track-next.png'))

        self.Last_button.clicked.connect(self.last_step)
        self.Last_button.setIcon(QtGui.QIcon(
            'Icons/tabler-icon-player-skip-forward.png'))

        # "Quick Rotate"
        self.Rotate_button.clicked.connect(self.Click_QuickRotate)

        # "Quick Combine"
        self.Combine_button.clicked.connect(self.Click_QuickCombine)

        # "Quick Reflect-X."
        self.X_reflect_button.clicked.connect(self.Click_XReflect)

        # "Quick Reflect-Y"
        self.Y_reflect_button.clicked.connect(self.Click_YReflect)

        self.SlowMode_button.clicked.connect(self.slowMode_toggle)

        # Available moves layout to place available moves
        self.movesLayout = QVBoxLayout(self.page_3)
        self.movesLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        # List of Move Widgets
        self.moveWidgets = []

        # Function to Move window on mouse drag event on the title bar
        def moveWindow(e):
            # Detect if the window is  normal size
            if self.isMaximized() == False:  # Not maximized
                # Move window only when window is normal size
                # if left mouse button is clicked (Only accept left mouse button clicks)
                if e.buttons() == Qt.LeftButton:
                    # Move window
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
        self.clickPosition = QtCore.QPoint(
            self.geometry().x(), self.geometry().y())

        self.textX = self.seedX + 10
        self.textY = self.seedY + 25

        self.tileSize = 40
        self.textSize = int(self.tileSize / 3)

        self.Engine = None
        self.SysLoaded = False
        self.play = True

        canvas = QtGui.QPixmap(self.geometry().width(),
                               self.geometry().height())
        canvas.fill(Qt.white)
        self.label.setPixmap(canvas)

        self.label_2.setText("")

    # Slide left menu function
    def slideLeftMenu(self):  # ANIMATION NEEDS TO BE WORKED ON SO ITS BEEN TURNED OFF
        # Get current left menu width
        width = self.slide_menu_container.width()

        # If minimized
        if width == 0:
            # Expand menu
            newWidth = 200
            canvas = QtGui.QPixmap(
                self.geometry().width() - 200, self.geometry().height() - 45)
            canvas.fill(Qt.white)

            self.slide_menu_container.setMaximumWidth(newWidth)
            #self.menu_animation(width, newWidth)
            self.label.setPixmap(canvas)
            # self.open_close_side_bar_btn.setIcon(QtGui.QIcon(u":/icons/icons/chevron-left.svg"))
        # If maximized
        else:
            # Restore menu
            newWidth = 0
            #self.setGeometry(self.x(), self.y(), self.geometry().width() - 100, self.geometry().height())
            #self.menu_animation(width, newWidth)
            self.slide_menu_container.setMaximumWidth(newWidth)

            canvas = QtGui.QPixmap(
                self.geometry().width(), self.geometry().height() - 45)
            canvas.fill(Qt.white)
            self.label.setPixmap(canvas)

            # self.open_close_side_bar_btn.setIcon(QtGui.QIcon(u":/icons/icons/align-left.svg"))

        if self.Engine != None:
            self.draw_assembly(self.Engine.getCurrentAssembly())

    def menu_animation(self, width, newWidth):
        # Animate the transition
        self.animation = QtCore.QPropertyAnimation(
            self.slide_menu_container, b"maximumWidth")  # Animate minimumWidht
        self.animation.setDuration(250)
        # Start value is the current menu width
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)  # end value is the new menu width
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()

    # Add mouse events to the window
    def mousePressEvent(self, event):
        # Get the current position of the mouse
        # print(event.globalPos())
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
            canvas = QtGui.QPixmap(
                self.geometry().width(), self.geometry().height() - 45)
        else:
            # prevents a bug that happens if menus open
            canvas = QtGui.QPixmap(
                self.geometry().width() - 200, self.geometry().height() - 45)

        canvas.fill(Qt.white)
        self.label.setPixmap(canvas)
        if self.Engine != None:
            self.seedX = self.geometry().width() / 2
            self.seedY = self.geometry().height() / 2
            self.textX = self.seedX + 10
            self.textY = self.seedY + 25
            self.draw_assembly(self.Engine.getCurrentAssembly())

    def keyPressEvent(self, event):
        #### Moving tiles across screen functions #####
        # up arrow key is pressed
        if event.key() == Qt.Key_W:
            self.seedY = self.seedY - 10
            self.textY = self.textY - 10
            if self.Engine != None:
                self.draw_assembly(self.Engine.getCurrentAssembly())

        # down arrow key is pressed
        elif event.key() == Qt.Key_S:
            self.seedY = self.seedY + 10
            self.textY = self.textY + 10
            if self.Engine != None:
                self.draw_assembly(self.Engine.getCurrentAssembly())

        # left arrow key is pressed
        elif event.key() == Qt.Key_A:
            self.seedX = self.seedX - 10
            self.textX = self.textX - 10
            if self.Engine != None:
                self.draw_assembly(self.Engine.getCurrentAssembly())

        # down arrow key is pressed
        elif event.key() == Qt.Key_D:
            self.seedX = self.seedX + 10
            self.textX = self.textX + 10
            if self.Engine != None:
                self.draw_assembly(self.Engine.getCurrentAssembly())

        # Hotkeys for the toolbar
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
            self.draw_assembly(self.Engine.getCurrentAssembly())

    def draw_move(self, move, forward):    
        painter = QPainter(self.label.pixmap())
        pen = QtGui.QPen()
        brush = QtGui.QBrush()
        font = QtGui.QFont()

        pen.setWidth(3)

        brush.setStyle(Qt.SolidPattern)

        font.setFamily("Times")
        font.setBold(True)
        font.setPixelSize(self.textSize)
        painter.setFont(font)

        pen.setColor(QtGui.QColor("black"))
        painter.setPen(pen)

        #adding attachment on screen
        if move['type'] == 'a' and forward == 1: #(type, x, y, state1)
            if self.onScreen_check(move['x'], move['y']) != 1:
                brush.setColor(QtGui.QColor("#" + move['state1'].returnColor()))
                self.draw_to_screen(move['x'], move['y'], move['state1'].get_label(), painter, brush)
        
        #showing transition on screen
        elif move['type'] == 't' and forward == 1: #(type, x, y, dir, state1, state2, state1Final, state2Final)
            self.transition_draw_function(move, move['state1Final'], move['state2Final'], painter, brush)

        #getting rid of attachment on screen
        elif move['type'] == 'a' and forward == 0: #(type, x, y, state1)
            brush.setColor(QtGui.QColor("white"))
            pen.setColor(QtGui.QColor("white"))
            painter.setPen(pen)

            if self.onScreen_check(move['x'], move['y']) != 1:
                self.draw_to_screen(move['x'], move['y'], "", painter, brush)

            assembly = self.Engine.getCurrentAssembly()
            pen.setColor(QtGui.QColor("black"))
            painter.setPen(pen)
   
            neighborN = assembly.coords.get("(" + str(move['x']) + "," + str(move['y'] + 1) + ")")
            neighborS = assembly.coords.get("(" + str(move['x']) + "," + str(move['y'] - 1) + ")")
            neighborE = assembly.coords.get("(" + str(move['x'] + 1) + "," + str(move['y']) + ")")
            neighborW = assembly.coords.get("(" + str(move['x'] - 1) + "," + str(move['y']) + ")")
            
            if neighborN != None:
                if self.onScreen_check(move['x'], move['y'] + 1) != 1:
                    brush.setColor(QtGui.QColor("#" + neighborN.get_color()))
                    self.draw_to_screen(move['x'], move['y'] + 1, neighborN.get_label(), painter, brush)
            if neighborS != None:
                if self.onScreen_check(move['x'], move['y'] - 1) != 1:
                    brush.setColor(QtGui.QColor("#" + neighborS.get_color()))
                    self.draw_to_screen(move['x'], move['y'] - 1, neighborS.get_label(), painter, brush)
            if neighborE != None:
                if self.onScreen_check(move['x'] + 1, move['y']) != 1:
                    brush.setColor(QtGui.QColor("#" + neighborE.get_color()))
                    self.draw_to_screen(move['x'] + 1, move['y'], neighborE.get_label(), painter, brush)
            if neighborW != None:
                if self.onScreen_check(move['x'] - 1, move['y']) != 1:
                    brush.setColor(QtGui.QColor("#" + neighborW.get_color()))
                    self.draw_to_screen(move['x'] - 1, move['y'], neighborW.get_label(), painter, brush)
        
        #reversing transition on screen
        elif move['type'] == 't' and forward == 0: #(type, x, y, dir, state1, state2, state1Final, state2Final)
            self.transition_draw_function(move, move['state1'], move['state2'], painter, brush)

        painter.end()

        self.Update_time_onScreen()
        self.Update_available_moves()
        self.update()

    def draw_assembly(self, assembly):
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
        painter.drawRect(0, 0, self.geometry().width(),
                         self.geometry().height())

        font.setFamily("Times")
        font.setBold(True)
        font.setPixelSize(self.textSize)
        painter.setFont(font)

        pen.setColor(QtGui.QColor("black"))
        painter.setPen(pen)
        for tile in assembly.tiles:
            if((tile.x * self.tileSize) + self.seedX > self.geometry().width() or (tile.x * self.tileSize) + self.seedX < -self.tileSize):
                continue #this if statement is so we don't draw tiles that aren't on screen width
            if((tile.y * -self.tileSize) + self.seedY > self.geometry().height() or (tile.y * -self.tileSize) + self.seedY < -self.tileSize):
                continue #this if statement is so we don't draw tiles that aren't on screen height

            brush.setColor(QtGui.QColor("#" + tile.get_color()))

            self.draw_to_screen(tile.x, tile.y, tile.state.label, painter, brush)

        painter.end()

        self.Update_time_onScreen()
        self.Update_available_moves()
        self.update()

    def Update_time_onScreen(self):
        if self.Engine.currentIndex != 0:
            self.label_2.setText("Time elapsed: \n" +
                                 str(round(self.time, 2)) + " time steps")
            self.label_3.setText("Current step time: \n" +
                                 str(round(self.Engine.timeTaken(), 2)) + " time steps")
        else:
            self.label_2.setText("Time elapsed: \n 0 time steps")
            self.label_3.setText("Current step time: \n 0 time steps")

    def Update_available_moves(self):
        # Remove old widgets from the layout
        for m in self.moveWidgets:
            self.movesLayout.removeWidget(m)
            m.deleteLater()
        self.moveWidgets = []

        # If no more moves, show it
        if len(self.Engine.validMoves) == 0:
            status = QLabel("No Available Moves")
            self.moveWidgets.append(status)
            self.movesLayout.addWidget(status)
        
        # If there are moves to pick, show them
        elif not len(self.Engine.validMoves) == 0:
            # Create moves and add to layout
            for m in self.Engine.validMoves:
                mGUI = Move(m, self, self.centralwidget)
                mGUI.setFixedHeight(34)
                self.moveWidgets.append(mGUI)
                self.movesLayout.addWidget(mGUI)

    def draw_to_screen(self, x, y, label, painter, brush):
        painter.setBrush(brush)

        painter.drawRect((x * self.tileSize) + self.seedX, (y * -self.tileSize) + self.seedY, self.tileSize, self.tileSize)
        if len(label) > 4:
            painter.drawText((x * self.tileSize) + self.textX, (y * -self.tileSize) + self.textY, label[0:3])
        else:
            painter.drawText((x * self.tileSize) + self.textX, (y * -self.tileSize) + self.textY, label)

    def transition_draw_function(self, move, state1, state2, painter, brush):
        horizontal = 0
        vertical = 0
        brush.setColor(QtGui.QColor("white"))
        if move['dir'] == 'h':
            horizontal = 1
        elif move['dir'] == 'v':
            vertical = -1
            
        if self.onScreen_check(move['x'], move['y']) != 1:
            self.draw_to_screen(move['x'], move['y'], "", painter, brush)
            brush.setColor(QtGui.QColor("#" + state1.returnColor()))
            self.draw_to_screen(move['x'], move['y'], state1.get_label(), painter, brush)

        if self.onScreen_check(move['x'] + horizontal, move['y'] + vertical) != 1:
            brush.setColor(QtGui.QColor("white"))
            self.draw_to_screen(move['x'] + horizontal, move['y'] + vertical, "", painter, brush)
            brush.setColor(QtGui.QColor("#" + state2.returnColor()))
            self.draw_to_screen(move['x'] + horizontal, move['y'] + vertical, state2.get_label(), painter, brush)
      
    #checks if a given tile is on screen by checking its coordinate, if not returns 1
    def onScreen_check(self, x, y):
        if((x * self.tileSize) + self.seedX > self.geometry().width() or (x * self.tileSize) + self.seedX < -self.tileSize):
            return 1
        if((y * -self.tileSize) + self.seedY > self.geometry().height() or (y * -self.tileSize) + self.seedY < -self.tileSize):
            return 1
        return 0

    def Click_Run_Simulation(self):  # Run application if everythings good
        err_flag = False

        if(err_flag == False):
            self.step = 0
            self.time = 0
            # Assembler_Proto.Main()
            self.draw_assembly(Assembler_Proto.CompleteAssemblyHistory[self.step])

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

            # the -150 is to account for the slide menu
            self.seedX = (self.geometry().width() - 150) / 2
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
            self.draw_assembly(self.Engine.getCurrentAssembly())

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
            self.draw_assembly(self.Engine.getCurrentAssembly())

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
            self.draw_assembly(self.Engine.getCurrentAssembly())

    def Click_XReflect(self):
        # Make a rotated system based off the current system, and instantly load the new system.
        if(self.SysLoaded == True):
            global currentSystem
            QuickReflect.reflect_across_x(currentSystem)
            currentSystem = QuickReflect.tempSystem
            self.time = 0
            self.Engine = Engine(currentSystem)
            self.draw_assembly(self.Engine.getCurrentAssembly())

    def Click_YReflect(self):
        # Make a rotated system based off the current system, and instantly load the new system.
        if(self.SysLoaded == True):
            global currentSystem
            QuickReflect.reflect_across_y(currentSystem)
            currentSystem = QuickReflect.tempSystem
            self.time = 0
            self.Engine = Engine(currentSystem)
            self.draw_assembly(self.Engine.getCurrentAssembly())

    # self.draw_assembly(LoadFile.) #starting assembly goes here
    def slowMode_toggle(self):
        if self.slowMode_Button.isChecked():
            self.delay = 1000
        else:
            self.delay = 0

    def do_move(self, move):
        if not self.play:
            # Shouldn't need all this code but copying from next_step() anyways
            self.stop_sequence()
            if self.SysLoaded == True:
                if self.Engine.step(move) != -1:
                    # Might need to go above
                    self.time = self.time + (self.Engine.timeTaken())
                    self.draw_assembly(self.Engine.getCurrentAssembly())

    def first_step(self):
        if self.SysLoaded == True:
            self.stop_sequence()
            self.Engine.first()
            self.time = 0
            self.draw_assembly(self.Engine.getCurrentAssembly())

    def prev_step(self):
        self.stop_sequence()
        if self.SysLoaded == True:
            if self.Engine.currentIndex > 0:
                self.draw_move(self.Engine.getCurrentMove(), 0)
                self.Engine.back()
                # Might need to go below
                self.time = self.time - (self.Engine.timeTaken())
                

    def next_step(self):
        self.stop_sequence()
        if self.SysLoaded == True:
            if self.Engine.step() != -1:
                # Might need to go above
                self.time = self.time + (self.Engine.timeTaken())
                self.draw_move(self.Engine.getCurrentMove(), 1)

    def last_step(self):
        self.stop_sequence()
        if self.SysLoaded == True:
            while (self.Engine.step() != -1):
                self.time = self.time + (self.Engine.timeTaken())

            self.draw_assembly(self.Engine.getCurrentAssembly())

    def play_sequence(self):
        if self.SysLoaded == True:
            if self.play == False:
                self.Play_button.setIcon(QtGui.QIcon(
                    'Icons/tabler-icon-player-pause.png'))
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

                    self.draw_move(self.Engine.getCurrentMove(), 1)
                    # if self.Engine.currentIndex != 0: #and self.Engine.currentIndex < self.Engine.lastIndex:

                # self.step = len(self.Engine.assemblyList) - 1 #this line is here to prevent a crash that happens if you click last after play finishes
                self.stop_sequence()
                self.Play_button.setIcon(QtGui.QIcon(
                    'Icons/tabler-icon-player-play.png'))

            if self.play == True:
                self.Play_button.setIcon(QtGui.QIcon(
                    'Icons/tabler-icon-player-play.png'))
                self.stop_sequence()

    def stop_sequence(self):
        self.play = False

class Move(QWidget):
    def __init__(self, move, mw, parent):
        super().__init__(parent)
        self.move = move
        self.mw = mw
        self.initUI()
    
    def initUI(self):
        self.show()
    
    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.draw(event, qp)
        qp.end()
    
    def draw(self, event, qp):
        moveText = ""

        if self.move["type"] == "a":
            moveText = "Attach\n" +  self.move["state1"].get_label() + " at " + str(self.move["x"]) + " , " + str(self.move["y"])
        elif self.move["type"] == "t":
            # Add Transition Direction
            if self.move["dir"] == "v":
                moveText = "V "
            else:
                moveText = "H "
            moveText += "Transition\n" + self.move["state1"].get_label() + ", " + self.move["state2"].get_label() + " to " + self.move["state1Final"].get_label() + ", " + self.move["state2Final"].get_label()

        pen = QApplication.palette().text().color()
        qp.setPen(pen)
        qp.drawText(event.rect(), Qt.AlignCenter, moveText)
        qp.drawRect(event.rect())
    
    def mousePressEvent(self, event):
        self.mw.do_move(self.move)


if __name__ == "__main__":

    # App Stuff
    app = QApplication(sys.argv)
    w = Ui_MainWindow()
    w.show()

    sys.exit(app.exec_())
#
