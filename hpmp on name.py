from gui import hpmp
import AutoUtils
import imgProcess
import autoit
import time
import sys
from PyQt5.QtWidgets import *
from imgProcess import Point
from AutoUtils import thread_with_trace

class hpmp(QMainWindow,hpmp.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.delayLine.setText('1000')
        self.textBoxList = [self.lineEdit1,self.lineEdit2,self.lineEdit3,self.lineEdit4,self.lineEdit5]
        self.hpmpnguoi.setChecked(True)
        self.hpmppet.setChecked(True)
        self.startBtn.clicked.connect(self.startClicked)
        self.started = False
        self.auto = autoHpmp()
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
        self.auto.hwnds.clear()
        self.auto.threads.clear()
        self.auto.titles.clear()
        self.auto.delay = int(self.delayLine.text()) * 0.001
        self.auto.hoipet = self.hpmppet.isChecked()
        self.auto.hoinguoi = self.hpmpnguoi.isChecked()
        for title in self.textBoxList:
            if (title.text().strip() != ""):
                self.auto.titles.append(title.text())
        for title in self.auto.titles:
            hwnd = autoit.win_get_handle(title)
            self.auto.hwnds.append(hwnd)

class autoHpmp():
    def __init__(self):
        self.titles =[]
        self.hwnds = []
        self.threads= []
        self.sanxuat = imgProcess.getImg('./img/sanxuat.png')
        self.khong = imgProcess.getImg('./img/khong.png')
        self.thiensu = imgProcess.getImg('./img/ok.png')
        self.delay = 0.5
        self.hoinguoi = False
        self.hoipet = False
    def start(self):
        for hwnd in self.hwnds:
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
        nguoi = Point(130,26)
        pet = Point(115,86)
        while (True):
            screen = imgProcess.CaptureWindow(hwnd)
            checkFight = imgProcess.findImgPoint(self.sanxuat, screen)
            checkTshp = imgProcess.findImgPointandFixCoord(self.thiensu, screen)
            checkKetban = imgProcess.findImgPointandFixCoord(self.khong, screen)
            if checkTshp != Point(0,0):
                AutoUtils.click(hwnd,checkTshp)
                time.sleep(self.delay)
            if checkKetban != Point(0,0):
                AutoUtils.click(hwnd,checkKetban)
                time.sleep(self.delay)
            if checkFight != Point(0,0):
                if(self.hoinguoi == True):
                    AutoUtils.click(hwnd,nguoi)
                    time.sleep(self.delay)
                if (self.hoipet == True):
                    AutoUtils.click(hwnd,pet)
                    time.sleep(self.delay)
            time.sleep(self.delay)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = hpmp()
    win.show()
    sys.exit(app.exec_())