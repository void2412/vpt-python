from gui import resetAuto
import autoUtils
import imgProcess
import time
import sys
from PyQt5.QtWidgets import *

from autoUtils import thread_with_trace

class autoQuang(QMainWindow, resetAuto.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('auto treo quang')
        self.textBoxList = [self.lineEdit1,self.lineEdit2,self.lineEdit3,self.lineEdit4,self.lineEdit5]
        self.startBtnList = [self.startBtn1, self.startBtn2, self.startBtn3, self.startBtn4, self.startBtn5]
        self.checkboxList = [self.checkBox, self.checkBox_2, self.checkBox_3, self.checkBox_4, self.checkBox_5]
        for checkbox in self.checkboxList:
            checkbox.setVisible(False)
        self.autoList = [treoQuang(),treoQuang(),treoQuang(),treoQuang(),treoQuang()]
        self.startStateList = [False,False,False,False,False]
        self.delayLine.setText('500')
        self.initBtn()

    def initBtn(self):
        i = 0
        for button in self.startBtnList:
            button.clicked.connect(lambda ch, index = i: self.start(index))
            i = i + 1

    def start(self, index):
        if (self.startStateList[index] == False):
            self.startStateList[index] = True
            self.startBtnList[index].setText('stop')
            title = self.textBoxList[index].text()
            delay = int(self.delayLine.text()) * 0.001
            hwnd = autoUtils.getHandle(title)
            self.autoList[index].hwnd = hwnd
            self.autoList[index].delay  = delay
            self.autoList[index].start()
        else:
            self.startStateList[index] = False
            self.startBtnList[index].setText('start')
            self.autoList[index].stop()
            self.autoList[index] = treoQuang()


class treoQuang():
    def __init__(self):
        self.sanxuat = imgProcess.getImg('./img/sanxuat.png')
        self.khong = imgProcess.getImg('./img/khong.png')
        self.thiensu = imgProcess.getImg('./img/ok.png')
        self.thread = None
        self.hwnd =None
        self.delay = 0.5
    def start(self):
        self.createThread(self.hwnd)
        self.thread.start()
    def stop(self):
        self.thread.kill()

    def createThread(self,hwnd):
        th = thread_with_trace(target=self.doWork,args=(hwnd,))
        th.setDaemon(True)
        self.thread = th

    def doWork(self,hwnd):
        bossQuang = (161,605)
        mp = (152, 49)
        while(True):
            screen = imgProcess.captureWindow(hwnd)
            checkFight = imgProcess.findImgPoint(self.sanxuat,screen)
            checkTshp = imgProcess.findImgPoint(self.thiensu,screen)
            checkKetban = imgProcess.findImgPoint(self.khong,screen)
            if checkTshp != (0, 0):
                autoUtils.click(hwnd, checkTshp)
                time.sleep(self.delay)
            if checkKetban != (0, 0):
                autoUtils.click(hwnd, checkKetban)
                time.sleep(self.delay)
            if checkFight != (0, 0):
                autoUtils.click(hwnd, mp)
                autoUtils.click(hwnd, bossQuang)

            time.sleep(self.delay)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = autoQuang()
    win.show()
    sys.exit(app.exec_())