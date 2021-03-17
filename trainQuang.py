from gui import autoquang
import AutoUtils
import imgProcess
import autoit
import time
import sys
from PyQt5.QtWidgets import *
from imgProcess import Point
from AutoUtils import thread_with_trace

class autoQuang(QMainWindow, autoquang.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.textBoxList = [self.lineEdit1,self.lineEdit2,self.lineEdit3,self.lineEdit4,self.lineEdit5]
        self.auto = treoQuang()
        self.started = False
        self.delayLine.setText('500')
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
            hwnd = autoit.win_get_handle(title)
            self.auto.hwnd.append(hwnd)

class treoQuang():
    def __init__(self):
        self.sanxuat = imgProcess.getImg('./img/sanxuat.png')
        self.khong = imgProcess.getImg('./img/khong.png')
        self.thiensu = imgProcess.getImg('./img/ok.png')
        self.threads = []
        self.title = []
        self.hwnd =[]
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
        self.threads.append(th)

    def doWork(self,hwnd):
        bossQuang = Point(397, 459)
        mp = Point(152,49)
        while(True):
            screen = imgProcess.CaptureWindow(hwnd)
            checkFight = imgProcess.findImgPoint(self.sanxuat,screen)
            checkTshp = imgProcess.findImgPointandFixCoord(self.thiensu,screen)
            checkKetban = imgProcess.findImgPointandFixCoord(self.khong,screen)
            if checkTshp != Point(0,0):
                AutoUtils.click(hwnd,checkTshp)
                time.sleep(self.delay)
            if checkKetban != Point(0,0):
                AutoUtils.click(hwnd,checkKetban)
                time.sleep(self.delay)
            if checkFight != Point(0,0):
                AutoUtils.click(hwnd,mp)
                AutoUtils.click(hwnd, bossQuang)

            time.sleep(self.delay)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = autoQuang()
    win.show()
    sys.exit(app.exec_())