# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TAFileWindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(589, 445)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(280, 300, 93, 28))
        self.pushButton_5.setObjectName("pushButton_5")
        self.error_label1 = QtWidgets.QLabel(self.centralwidget)
        self.error_label1.setGeometry(QtCore.QRect(390, 70, 131, 16))
        self.error_label1.setText("")
        self.error_label1.setObjectName("error_label1")
        self.error_label2 = QtWidgets.QLabel(self.centralwidget)
        self.error_label2.setGeometry(QtCore.QRect(390, 120, 121, 16))
        self.error_label2.setText("")
        self.error_label2.setObjectName("error_label2")
        self.error_label3 = QtWidgets.QLabel(self.centralwidget)
        self.error_label3.setGeometry(QtCore.QRect(390, 180, 131, 16))
        self.error_label3.setText("")
        self.error_label3.setObjectName("error_label3")
        self.error_label4 = QtWidgets.QLabel(self.centralwidget)
        self.error_label4.setGeometry(QtCore.QRect(390, 240, 141, 16))
        self.error_label4.setText("")
        self.error_label4.setObjectName("error_label4")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(60, 40, 311, 220))
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 1, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setObjectName("pushButton")
        self.buttonGroup = QtWidgets.QButtonGroup(MainWindow)
        self.buttonGroup.setObjectName("buttonGroup")
        self.buttonGroup.addButton(self.pushButton)
        self.gridLayout.addWidget(self.pushButton, 1, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout.addWidget(self.lineEdit_2, 3, 0, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.widget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.buttonGroup.addButton(self.pushButton_2)
        self.gridLayout.addWidget(self.pushButton_2, 3, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 4, 0, 1, 1)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.gridLayout.addWidget(self.lineEdit_3, 5, 0, 1, 1)
        self.pushButton_3 = QtWidgets.QPushButton(self.widget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.buttonGroup.addButton(self.pushButton_3)
        self.gridLayout.addWidget(self.pushButton_3, 5, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 6, 0, 1, 1)
        self.lineEdit_4 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.gridLayout.addWidget(self.lineEdit_4, 7, 0, 1, 1)
        self.pushButton_4 = QtWidgets.QPushButton(self.widget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.buttonGroup.addButton(self.pushButton_4)
        self.gridLayout.addWidget(self.pushButton_4, 7, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 589, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Tile Automata Simulator"))
        self.pushButton_5.setText(_translate("MainWindow", "Begin"))
        self.label.setText(_translate("MainWindow", "Affinity rules"))
        self.pushButton.setText(_translate("MainWindow", "select file"))
        self.label_2.setText(_translate("MainWindow", "Transition rules"))
        self.pushButton_2.setText(_translate("MainWindow", "select file"))
        self.label_3.setText(_translate("MainWindow", "States"))
        self.pushButton_3.setText(_translate("MainWindow", "select file"))
        self.label_4.setText(_translate("MainWindow", "Starting configuration"))
        self.pushButton_4.setText(_translate("MainWindow", "select file"))
