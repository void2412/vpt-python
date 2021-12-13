from gui import autoTemplate
from autoUtils import *
from imgProcess import *
import time
from PyQt5.QtWidgets import *
from imgProcess import Point
from autoUtils import thread_with_trace
import win32gui
import autoUtils


class autoKsMenu(QMainWindow,autoTemplate.Ui_MainWindow):
    def __init__(self):
        super(autoKsMenu, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('auto Ks shop tranh mua')
        self.started = False
        self.titleList = [self.lineEdit1, self.lineEdit2, self.lineEdit3, self.lineEdit4, self.lineEdit5]
        self.delayLine.setText('100')
        self.auto = autoKs()
        self.startBtn.clicked.connect(self.startBtnClicked)


    def startBtnClicked(self):
        self.auto.handleList.clear()
        if not self.started:
            self.started = True
            self.startBtn.setText('stop')
            self.auto.delay = int(self.delayLine.text()) * 0.001
            for item in self.titleList:
                if item.text() != "":
                    hwnd = getHandle(item.text())
                    self.auto.handleList.append(hwnd)
            self.auto.start()

        else:
            self.started = False
            self.startBtn.setText('start')
            self.auto.stop()

class autoKs():
    def __init__(self):
        self.handleList = []
        self.khong = getImg('./img/khong.png')
        self.datvao = getImg('./img/datvao.png')
        self.dotim = getImg('./img/dotim.png')
        self.autoThreads = []
        self.delay = 100

    def start(self):
        self.autoThreads.clear()
        for handle in self.handleList:
            th = thread_with_trace(target=self.doAuto, args=(handle,self.delay))
            self.autoThreads.append(th)
        for thread in self.autoThreads:
            thread.start()
    def stop(self):
        for thread in self.autoThreads:
            thread.kill()
    def doAuto(self,hwnd,delay):
        while True:
            (x, y, x1, y1) = win32gui.GetWindowRect(hwnd)

            w = x1 - x
            h = y1 - y

            if w != 1066 or h != 724:
                autoUtils.ResizeWindow(hwnd)
            coPoint = (-69,0)
            xacnhanPoint = (-67,0)
            muaPoint = (138,0)
            empty = (0,0)
            screen = captureWindow(hwnd)
            checkKhong = findImgPoint(self.khong,screen)
            checkxacnhan = findImgPoint(self.datvao, screen)
            if checkxacnhan != (0,0) or checkKhong != (0,0):
                if checkKhong != (0,0):
                    clickPoint = checkKhong + coPoint
                    autoUtils.click(hwnd,clickPoint)
                    time.sleep(delay)


                if checkxacnhan != (0,0):
                    clickPoint = checkxacnhan + xacnhanPoint
                    autoUtils.click(hwnd,clickPoint)
                    time.sleep(delay)
            else:
                checkmua = findImgPoint(self.dotim,screen)
                if checkmua != (0,0):
                    clickPoint = checkmua + muaPoint
                    autoUtils.click(hwnd,clickPoint)
                    time.sleep(delay)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    menu = autoKsMenu()
    menu.show()
    sys.exit(app.exec_())