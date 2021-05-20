import autoUtils
import  win32gui
import time
import sys
from PyQt5.QtWidgets import *
from gui import tacticalmove

class tacticalMove(QMainWindow,tacticalmove.Ui_MainWindow):
    def __init__(self):
        super(tacticalMove, self).__init__()
        self.setupUi(self)
        self.titleList=[self.lineEdit1,self.lineEdit2,self.lineEdit3,self.lineEdit4,self.lineEdit5]
        self.startBtn.clicked.connect(self.startBtnClicked)
        self.setWindowTitle('tacticalMove')

    def startBtnClicked(self):
        for i in range(5):
            if(self.titleList[i].text() != ""):
                (x,y) = self.getPos(i)
                hwnd = autoUtils.getHandle(self.titleList[i].text().strip())
                win32gui.MoveWindow(hwnd,x,y,1066,724,True)

    def getPos(self,index):
        if index == 0:
            return (5,1)
        if index == 1:
            return (1496,3)
        if index == 2:
            return (752,384)
        if index == 3:
            return (5,719)
        if index == 4:
            return (1496,723)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    q = tacticalMove()
    q.show()
    sys.exit(app.exec_())