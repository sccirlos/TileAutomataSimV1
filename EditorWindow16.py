# -*- coding: utf-8 -*-

 # Form implementation generated from reading ui file 'EditorWindow.ui'
 #
 # Created by: PyQt5 UI code generator 5.15.4 & Sonya Cirlos :) 
 #
 # WARNING: Any manual changes made to this file will be lost when pyuic5 is
 # run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import general_TA_simulator 

class Ui_EditorWindow(object):
     def setupUi(self, EditorWindow):
         EditorWindow.setObjectName("EditorWindow")
         EditorWindow.resize(813, 586)
         font = QtGui.QFont()
         font.setFamily("Verdana")
         EditorWindow.setFont(font)
         EditorWindow.setToolTipDuration(-2)
         EditorWindow.setStyleSheet("")
         self.centralwidget = QtWidgets.QWidget(EditorWindow)
         self.centralwidget.setStyleSheet("")
         self.centralwidget.setObjectName("centralwidget")
         self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
         self.verticalLayout.setObjectName("verticalLayout")
         self.editFrame = QtWidgets.QFrame(self.centralwidget)
         sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
         sizePolicy.setHorizontalStretch(0)
         sizePolicy.setVerticalStretch(0)
         sizePolicy.setHeightForWidth(self.editFrame.sizePolicy().hasHeightForWidth())
         self.editFrame.setSizePolicy(sizePolicy)
         self.editFrame.setMaximumSize(QtCore.QSize(16777215, 500))
         self.editFrame.setFrameShape(QtWidgets.QFrame.NoFrame)
         self.editFrame.setFrameShadow(QtWidgets.QFrame.Raised)
         self.editFrame.setObjectName("editFrame")
         self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.editFrame)
         self.verticalLayout_2.setObjectName("verticalLayout_2")
         self.toolBox = QtWidgets.QToolBox(self.editFrame)
         self.toolBox.setObjectName("toolBox")

         ### Page 1 of editor; System Temperature
         self.page = QtWidgets.QWidget()
         self.page.setGeometry(QtCore.QRect(0, 0, 765, 340))
         self.page.setMinimumSize(QtCore.QSize(0, 340))
         self.page.setObjectName("page")
         self.label = QtWidgets.QLabel(self.page)
         self.label.setGeometry(QtCore.QRect(30, 30, 60, 16))
         self.label.setObjectName("label")
         self.comboBox = QtWidgets.QComboBox(self.page)
         self.comboBox.setGeometry(QtCore.QRect(90, 20, 91, 32))
         self.comboBox.setObjectName("comboBox")
         self.toolBox.addItem(self.page, "")

         ### Page 2 of editor; Add State
         self.page_2 = QtWidgets.QWidget()
         self.page_2.setGeometry(QtCore.QRect(0, 0, 765, 340))
         self.page_2.setObjectName("page_2")
          # table for states
         self.tableWidget = QtWidgets.QTableWidget(self.page_2)
         self.tableWidget.setGeometry(QtCore.QRect(0, 70, 771, 200))
         self.tableWidget.setObjectName("tableWidget")
         self.tableWidget.setColumnCount(4)
         columns = ['Color', 'Label', 'Seed', 'Initial']
         self.tableWidget.setColumnWidth(0, 100)
         self.tableWidget.setColumnWidth(1, 100)
         self.tableWidget.setColumnWidth(2, 100)
         self.tableWidget.setColumnWidth(3, 100)
         self.tableWidget.setHorizontalHeaderLabels(columns)
         self.tableWidget.setRowCount(2)
         self.tableWidget.setRowHeight(0, 40)
         self.tableWidget.setRowHeight(1, 40)
    
          # add row for state table
          # after clicking add row; scroll down table to see it and edit boxes
         self.pushButton_3 = QtWidgets.QPushButton(self.page_2)
         self.pushButton_3.setGeometry(QtCore.QRect(10, 10, 113, 32))
         self.pushButton_3.setObjectName("pushButton_3")
         self.toolBox.addItem(self.page_2, "")


         ### Page 3; Affinity Rules
         self.page_3 = QtWidgets.QWidget()
         self.page_3.setGeometry(QtCore.QRect(0, 0, 765, 340))
         self.page_3.setObjectName("page_3")
       
         self.tableWidget_2 = QtWidgets.QTableWidget(self.page_3)
         self.tableWidget_2.setGeometry(QtCore.QRect(0, 50, 771, 261))
         self.tableWidget_2.setObjectName("tableWidget_2")
        
         self.tableWidget_2.setColumnCount(4)
         columns = ['State 1', 'State 2', 'Direction', 'Glue Strength']
         self.tableWidget_2.setColumnWidth(0, 100)
         self.tableWidget_2.setColumnWidth(1, 100)
         self.tableWidget_2.setColumnWidth(2, 125)
         self.tableWidget_2.setColumnWidth(3, 100)
         self.tableWidget_2.setHorizontalHeaderLabels(columns)
         self.tableWidget_2.setRowCount(2)
         self.tableWidget_2.setRowHeight(0, 40)
         self.tableWidget_2.setRowHeight(1, 40)
          # Add row button for affinity rules
         self.pushButton_4 = QtWidgets.QPushButton(self.page_3)
         self.pushButton_4.setGeometry(QtCore.QRect(20, 0, 113, 32))
         self.pushButton_4.setObjectName("pushButton_4")
         self.toolBox.addItem(self.page_3, "")

        ### Page 4; Transition Rules
         self.page_4 = QtWidgets.QWidget()
         self.page_4.setGeometry(QtCore.QRect(0, 0, 765, 340))
         self.page_4.setObjectName("page_4")
        
         self.tableWidget_3 = QtWidgets.QTableWidget(self.page_4)
         self.tableWidget_3.setGeometry(QtCore.QRect(0, 50, 771, 261))
         self.tableWidget_3.setObjectName("tableWidget_3")
         self.tableWidget_3.setColumnCount(6)
         columns = ['State 1', 'State 2', '-->', 'State 1 Final', 'State 2 Final', 'Direction']
         self.tableWidget_3.setColumnWidth(0, 100)
         self.tableWidget_3.setColumnWidth(1, 100)
         self.tableWidget_3.setColumnWidth(2, 90)
         self.tableWidget_3.setColumnWidth(3, 120)
         self.tableWidget_3.setColumnWidth(4, 120)
         self.tableWidget_3.setColumnWidth(5, 100)
         self.tableWidget_3.setHorizontalHeaderLabels(columns)
         self.tableWidget_3.setRowCount(2)
         self.tableWidget_3.setRowHeight(0, 40)
         self.tableWidget_3.setRowHeight(1, 40)
          # Add row button for transition rules
         self.pushButton_5 = QtWidgets.QPushButton(self.page_4)
         self.pushButton_5.setGeometry(QtCore.QRect(10, 0, 113, 32))
         self.pushButton_5.setObjectName("pushButton_5")
         self.toolBox.addItem(self.page_4, "")
         

         self.verticalLayout_2.addWidget(self.toolBox)
         self.verticalLayout.addWidget(self.editFrame)
         self.frame_2 = QtWidgets.QFrame(self.centralwidget)
         self.frame_2.setFrameShape(QtWidgets.QFrame.NoFrame)
         self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
         self.frame_2.setObjectName("frame_2")
         self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_2)
         self.horizontalLayout.setObjectName("horizontalLayout")
         self.pushButton = QtWidgets.QPushButton(self.frame_2)
         sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
         sizePolicy.setHorizontalStretch(0)
         sizePolicy.setVerticalStretch(0)
         sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
         self.pushButton.setSizePolicy(sizePolicy)
         self.pushButton.setObjectName("pushButton")
         self.horizontalLayout.addWidget(self.pushButton)
         self.pushButton_2 = QtWidgets.QPushButton(self.frame_2)
         sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
         sizePolicy.setHorizontalStretch(0)
         sizePolicy.setVerticalStretch(0)
         sizePolicy.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
         self.pushButton_2.setSizePolicy(sizePolicy)
         self.pushButton_2.setObjectName("pushButton_2")
         self.horizontalLayout.addWidget(self.pushButton_2)
         self.verticalLayout.addWidget(self.frame_2, 0, QtCore.Qt.AlignRight|QtCore.Qt.AlignBottom)
         EditorWindow.setCentralWidget(self.centralwidget)

         self.retranslateUi(EditorWindow)
         self.toolBox.setCurrentIndex(1)
         QtCore.QMetaObject.connectSlotsByName(EditorWindow)

     def retranslateUi(self, EditorWindow):
         _translate = QtCore.QCoreApplication.translate
         EditorWindow.setWindowTitle(_translate("EditorWindow", "Editor "))
         self.label.setText(_translate("EditorWindow", "Temp:"))
         self.toolBox.setItemText(self.toolBox.indexOf(self.page), _translate("EditorWindow", "System Temperature"))
         self.toolBox.setItemText(self.toolBox.indexOf(self.page_2), _translate("EditorWindow", "Add State"))
         self.toolBox.setItemText(self.toolBox.indexOf(self.page_3), _translate("EditorWindow", "Add Affinity Rule"))
         self.toolBox.setItemText(self.toolBox.indexOf(self.page_4), _translate("EditorWindow", "Add Transition Rule"))
         self.pushButton.setText(_translate("EditorWindow", "Apply"))
         self.pushButton_2.setText(_translate("EditorWindow", "Save as"))
         self.pushButton_3.setText(_translate("EditorWindow", "Add Row"))
         self.pushButton_4.setText(_translate("EditorWindow", "Add Row"))
         self.pushButton_5.setText(_translate("EditorWindow", "Add Row"))


if __name__ == "__main__":
     import sys
     app = QtWidgets.QApplication(sys.argv)
     EditorWindow = QtWidgets.QMainWindow()
     ui = Ui_EditorWindow()
     ui.setupUi(EditorWindow)
     EditorWindow.show()
     sys.exit(app.exec_())