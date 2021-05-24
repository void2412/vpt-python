from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_mainWindow(object):
    def setupUI(self,mainWindow):
        #mainwindow
        mainWindow.setObjectName('mainWindow')
        mainWindow.resize(924,606)

        #central widget
        self.central=QtWidgets.QWidget(mainWindow)
        self.central.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setHeightForWidth(self.central.sizePolicy().hasHeightForWidth())
        self.central.setSizePolicy(sizePolicy)
        self.central.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.central.setSizeIncrement(QtCore.QSize(0,0))
        self.central.setObjectName('central_widget')
        self.gridlayout = QtWidgets.QGridLayout(self.central)
        self.gridlayout.setObjectName('gridLayout')
