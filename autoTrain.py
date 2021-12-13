from gui import autotrain
import autoUtils
import imgProcess
import time
import sys
from PyQt5.QtWidgets import *

from autoUtils import thread_with_trace
import win32gui

class trainWindow(QMainWindow,autotrain.Ui_MainWindow):
    def __init__(self):
        super(trainWindow, self).__init__()
        self.setupUi(self)
        self.started = False
        self.chatRadioButton.setText('chat mật')
        self.boxRadioButton.setText('chat riêng')
        self.textBoxList = [self.lineEdit1,self.lineEdit2,self.lineEdit3,self.lineEdit4,self.lineEdit5]
        self.auto = autoTrain()
        self.delayLine.setText('1500')
        self.chatRadioButton.setChecked(True)
        self.startBtn.clicked.connect(self.startClicked)

    def startClicked(self):
        if self.started is False:
            self.started = True
            self.startBtn.setText('stop')
            self.initData()
            self.auto.start()
        else:
            self.started = False
            self.startBtn.setText('start')
            self.auto.stop()

    def initData(self):
        self.auto.hwnd.clear()
        self.auto.threads.clear()
        self.auto.title.clear()
        self.auto.delay = int(self.delayLine.text()) * 0.001
        for title in self.textBoxList:
            if (title.text().strip() != ""):
                self.auto.title.append(title.text())
        for title in self.auto.title:
            hwnd = autoUtils.getHandle(title)
            self.auto.hwnd.append(hwnd)

        if(self.boxRadioButton.isChecked() == True):
            self.auto.chatrieng = True
        if(self.chatRadioButton.isChecked() == True):
            self.auto.chatrieng = False

class autoTrain():
    def __init__(self):
        self.sanxuat = imgProcess.getImg('./img/sanxuat.png')
        self.thiensu = imgProcess.getImg('./img/ok.png')
        self.ketban = imgProcess.getImg('./img/khong.png')
        self.chatrieng = False
        self.threads = []
        self.title = []
        self.hwnd = []
        self.delay = 0.5

    def start(self):
        for hwnd in self.hwnd:
            self.createThread(hwnd)
        for thread in self.threads:
            thread.start()
    def stop(self):
        for thread in self.threads:
            thread.kill()

    def createThread(self,hwnd):
        th = thread_with_trace(target=self.doWork,args=(hwnd,))
        th.setDaemon(True)
        self.threads.append(th)

    def doWork(self, hwnd):
        p1 = (0, 0)
        p2 = (0, 0)
        if (self.chatrieng == False):
            p1 = (159, 593)
            p2 = (157, 606)
        else:
            p1 = (396, 459)
            p2 = (428, 458)
        while (True):
            (x, y, x1, y1) = win32gui.GetWindowRect(hwnd)
            w = x1 - x
            h = y1 - y
            if (w != 1066 or h != 724):
                autoUtils.ResizeWindow(hwnd)
            screen = imgProcess.captureWindow(hwnd)
            checkFight = imgProcess.findImgPoint (self.sanxuat, screen)
            checkTshp = imgProcess.findImgPoint (self.thiensu, screen)
            checkKetban = imgProcess.findImgPoint (self.ketban, screen)
            if checkTshp != (0, 0):
                autoUtils.click(hwnd, checkTshp)
                time.sleep(1)
            if checkKetban != (0, 0):
                autoUtils.click(hwnd, checkKetban)
                time.sleep(1)
            if checkFight != (0, 0):
                autoUtils.click(hwnd, p1)
                time.sleep(self.delay)
                autoUtils.click(hwnd, p2)
            time.sleep(self.delay)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = trainWindow()
    win.show()
    sys.exit(app.exec_())