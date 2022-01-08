from gui import autoKiemNL
import sys
from dataclasses import dataclass
import openpyxl
from PyQt5.QtWidgets import *
from mapData import *
import startvpt
from openpyxl import Workbook
from PyQt5.QtCore import *
import subprocess
import time
import wincap

class mainMenu(QMainWindow,autoKiemNL.Ui_mainWindow):
    def __init__(self):
        super(mainMenu, self).__init__()
        self.setupUi(self)
        x = self.tableWidget.horizontalHeader()
        x.setSectionResizeMode(2, QHeaderView.Stretch)
        x.resizeSection(4,300)
        x.resizeSection(3,150)


class cauca():
    def __init__(self):
        pass
        
    pass

class trongcay():
    pass

class haiduoc():
    pass



if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainMenu = mainMenu()
    mainMenu.show()
    sys.exit(app.exec_())