# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'thuthapnl.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(506, 263)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(10, 0, 491, 231))
        self.widget.setObjectName("widget")
        self.lineEdit1 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit1.setGeometry(QtCore.QRect(10, 30, 156, 23))
        self.lineEdit1.setMinimumSize(QtCore.QSize(0, 23))
        self.lineEdit1.setObjectName("lineEdit1")
        self.lineEdit2 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit2.setGeometry(QtCore.QRect(10, 60, 156, 23))
        self.lineEdit2.setMinimumSize(QtCore.QSize(0, 23))
        self.lineEdit2.setObjectName("lineEdit2")
        self.lineEdit3 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit3.setGeometry(QtCore.QRect(10, 90, 156, 23))
        self.lineEdit3.setMinimumSize(QtCore.QSize(0, 23))
        self.lineEdit3.setObjectName("lineEdit3")
        self.lineEdit4 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit4.setGeometry(QtCore.QRect(10, 120, 156, 23))
        self.lineEdit4.setMinimumSize(QtCore.QSize(0, 23))
        self.lineEdit4.setObjectName("lineEdit4")
        self.lineEdit5 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit5.setGeometry(QtCore.QRect(10, 150, 156, 23))
        self.lineEdit5.setMinimumSize(QtCore.QSize(0, 23))
        self.lineEdit5.setObjectName("lineEdit5")
        self.startBtn1 = QtWidgets.QPushButton(self.widget)
        self.startBtn1.setGeometry(QtCore.QRect(400, 30, 75, 23))
        self.startBtn1.setObjectName("startBtn1")
        self.startBtn2 = QtWidgets.QPushButton(self.widget)
        self.startBtn2.setGeometry(QtCore.QRect(400, 60, 75, 23))
        self.startBtn2.setObjectName("startBtn2")
        self.startBtn3 = QtWidgets.QPushButton(self.widget)
        self.startBtn3.setGeometry(QtCore.QRect(400, 90, 75, 23))
        self.startBtn3.setObjectName("startBtn3")
        self.startBtn4 = QtWidgets.QPushButton(self.widget)
        self.startBtn4.setGeometry(QtCore.QRect(400, 120, 75, 23))
        self.startBtn4.setObjectName("startBtn4")
        self.startBtn5 = QtWidgets.QPushButton(self.widget)
        self.startBtn5.setGeometry(QtCore.QRect(400, 150, 75, 23))
        self.startBtn5.setObjectName("startBtn5")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(20, 0, 156, 20))
        self.label.setObjectName("label")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.widget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(300, 180, 81, 41))
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
        self.comboBox1 = QtWidgets.QComboBox(self.widget)
        self.comboBox1.setGeometry(QtCore.QRect(170, 30, 131, 22))
        self.comboBox1.setObjectName("comboBox1")
        self.comboBox2 = QtWidgets.QComboBox(self.widget)
        self.comboBox2.setGeometry(QtCore.QRect(170, 60, 131, 22))
        self.comboBox2.setObjectName("comboBox2")
        self.comboBox3 = QtWidgets.QComboBox(self.widget)
        self.comboBox3.setGeometry(QtCore.QRect(170, 90, 131, 22))
        self.comboBox3.setObjectName("comboBox3")
        self.comboBox4 = QtWidgets.QComboBox(self.widget)
        self.comboBox4.setGeometry(QtCore.QRect(170, 120, 131, 22))
        self.comboBox4.setObjectName("comboBox4")
        self.comboBox5 = QtWidgets.QComboBox(self.widget)
        self.comboBox5.setGeometry(QtCore.QRect(170, 150, 131, 22))
        self.comboBox5.setObjectName("comboBox5")
        self.checkBox1 = QtWidgets.QCheckBox(self.widget)
        self.checkBox1.setGeometry(QtCore.QRect(310, 30, 91, 17))
        self.checkBox1.setObjectName("checkBox1")
        self.checkBox2 = QtWidgets.QCheckBox(self.widget)
        self.checkBox2.setGeometry(QtCore.QRect(310, 60, 91, 17))
        self.checkBox2.setObjectName("checkBox2")
        self.checkBox3 = QtWidgets.QCheckBox(self.widget)
        self.checkBox3.setGeometry(QtCore.QRect(310, 90, 91, 17))
        self.checkBox3.setObjectName("checkBox3")
        self.checkBox4 = QtWidgets.QCheckBox(self.widget)
        self.checkBox4.setGeometry(QtCore.QRect(310, 120, 91, 17))
        self.checkBox4.setObjectName("checkBox4")
        self.checkBox5 = QtWidgets.QCheckBox(self.widget)
        self.checkBox5.setGeometry(QtCore.QRect(310, 150, 91, 17))
        self.checkBox5.setObjectName("checkBox5")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 506, 21))
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
        self.startBtn1.setText(_translate("MainWindow", "start"))
        self.startBtn2.setText(_translate("MainWindow", "start"))
        self.startBtn3.setText(_translate("MainWindow", "start"))
        self.startBtn4.setText(_translate("MainWindow", "start"))
        self.startBtn5.setText(_translate("MainWindow", "start"))
        self.label.setText(_translate("MainWindow", "window title"))
        self.label_2.setText(_translate("MainWindow", "delay(ms)"))
        self.checkBox1.setText(_translate("MainWindow", "cây dài ngày"))
        self.checkBox2.setText(_translate("MainWindow", "cây dài ngày"))
        self.checkBox3.setText(_translate("MainWindow", "cây dài ngày"))
        self.checkBox4.setText(_translate("MainWindow", "cây dài ngày"))
        self.checkBox5.setText(_translate("MainWindow", "cây dài ngày"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
