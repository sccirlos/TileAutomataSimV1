# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TAMainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(853, 658)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(380, 530, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 851, 511))
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 853, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionLoad = QtWidgets.QAction(MainWindow)
        self.actionLoad.setObjectName("actionLoad")
        self.actionNext = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("C:/Users/rmich/Pictures/Saved Pictures/next.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNext.setIcon(icon)
        self.actionNext.setObjectName("actionNext")
        self.actionPrevious = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("C:/Users/rmich/Pictures/Saved Pictures/previous.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPrevious.setIcon(icon1)
        self.actionPrevious.setObjectName("actionPrevious")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionLoad)
        self.menuFile.addAction(self.actionSave)
        self.menubar.addAction(self.menuFile.menuAction())
        self.toolBar.addAction(self.actionPrevious)
        self.toolBar.addAction(self.actionNext)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Tile Automata Simulator"))
        self.pushButton.setText(_translate("MainWindow", "Begin"))
        self.label.setText(_translate("MainWindow", "TextLabel"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionLoad.setText(_translate("MainWindow", "Load"))
        self.actionNext.setText(_translate("MainWindow", "Next"))
        self.actionNext.setToolTip(_translate("MainWindow", "<html><head/><body><p>Goes to next stage of assembly</p></body></html>"))
        self.actionPrevious.setText(_translate("MainWindow", "Previous"))
        self.actionPrevious.setToolTip(_translate("MainWindow", "goes to previous stage of assembly"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionNew.setText(_translate("MainWindow", "New"))
