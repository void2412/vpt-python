# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'autoTemplate.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(273, 210)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(180, 10, 81, 41))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.delayLine = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.delayLine.setObjectName("delayLine")
        self.verticalLayout_2.addWidget(self.delayLine)
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 158, 152))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.lineEdit1 = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit1.setObjectName("lineEdit1")
        self.verticalLayout.addWidget(self.lineEdit1)
        self.lineEdit2 = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit2.setObjectName("lineEdit2")
        self.verticalLayout.addWidget(self.lineEdit2)
        self.lineEdit3 = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit3.setObjectName("lineEdit3")
        self.verticalLayout.addWidget(self.lineEdit3)
        self.lineEdit4 = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit4.setObjectName("lineEdit4")
        self.verticalLayout.addWidget(self.lineEdit4)
        self.lineEdit5 = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit5.setObjectName("lineEdit5")
        self.verticalLayout.addWidget(self.lineEdit5)
        self.startBtn = QtWidgets.QPushButton(self.centralwidget)
        self.startBtn.setGeometry(QtCore.QRect(180, 120, 75, 23))
        self.startBtn.setObjectName("startBtn")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 273, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "auto"))
        self.label_2.setText(_translate("MainWindow", "delay(ms)"))
        self.label.setText(_translate("MainWindow", "window title"))
        self.startBtn.setText(_translate("MainWindow", "start"))
