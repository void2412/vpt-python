import time
import imgProcess
from gui import nhantraQ
import sys
from PyQt5.QtWidgets import *

from autoUtils import thread_with_trace
import win32gui
import autoUtils

class nhantraQ(QMainWindow, nhantraQ.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.started = False
        self.auto = autoTraQ()
        self.titleList=[self.lineEdit1,self.lineEdit2,self.lineEdit3,self.lineEdit4,self.lineEdit5]
        self.startBtn.clicked.connect(self.startBtnClicked)
        self.delayLine.setText('500')


    def startBtnClicked(self):
        self.auto.titleList.clear()
        if not self.started:
            self.started = True
            self.startBtn.setText('stop')
            self.auto.delay = int(self.delayLine.text()) * 0.001
            for item in self.titleList:
                if (item.text() != ""):
                    self.auto.titleList.append(item.text())
            self.auto.start()

        else:
            self.started = False
            self.startBtn.setText('start')
            self.auto.stop()



class autoTraQ():
    def __init__(self):
        self.canve = imgProcess.getImg('./img/nhantraQ/canvedht.png')
        self.nhiemvu = imgProcess.getImg('./img/nhantraQ/nhiemvu.png')
        self.co = imgProcess.getImg('./img/nhantraQ/co.png')
        self.trilieu = imgProcess.getImg('./img/nhantraQ/trilieu.png')
        self.tonle = imgProcess.getImg('./img/nhantraQ/tonle.png')
        self.roikhoi = imgProcess.getImg('./img/nhantraQ/roikhoi.png')
        self.nhanQ = imgProcess.getImg('./img/nhantraQ/nhan.png')
        self.nhanQ2 = imgProcess.getImg('./img/nhantraQ/nhan2.png')
        self.traQ = imgProcess.getImg('./img/nhantraQ/xong.png')
        self.npc = imgProcess.getImg('./img/nhantraQ/npc nhiem vu.PNG')
        self.titleList = []
        self.handleList=[]
        self.auto_threads = []
        self.delay = 0

        self.p_roikhoi=(0, 0)
        self.p_nhanQ=(0, 0)
        self.p_nhanQ2 = (0, 0)
        self.p_traQ=(0, 0)
        self.p_quest = (0, 0)
        self.p_tonle = (0, 0)
        self.p_nhiemvu = (0, 0)
        self.p_canve = (0, 0)
        self.p_npc = (0, 0)

    def start(self):
        self.getHandle()
        for item in self.handleList:
            th = thread_with_trace(target=self.doAuto,args=(item,self.delay))
            th.setDaemon(True)
            self.auto_threads.append(th)
        for item in self.auto_threads:
            item.start()
            time.sleep(0.3)
        pass

    def stop(self):
        for item in self.auto_threads:
            item.kill()
        self.auto_threads.clear()
        pass

    def getHandle(self):
        self.handleList.clear()
        for item in self.titleList:
            hwnd = autoUtils.getHandle(item)
            self.handleList.append(hwnd)

    def doAuto(self,hwnd,delay):
        randomLoc = (967, 47)
        while (True):

            (x,y,x1,y1) = win32gui.GetWindowRect(hwnd)
            w = x1-x
            h = y1-y
            if(w != 1066 or h!= 724):
                autoUtils.ResizeWindow(hwnd)
            screen = imgProcess.captureWindow(hwnd)

            self.p_roikhoi = imgProcess.findImgPoint(self.roikhoi,screen)
            if (self.p_roikhoi != (0, 0)):

                self.p_tonle = imgProcess.findImgPoint(self.tonle,screen, 0.6)
                if(self.p_tonle != (0, 0)):
                    self.p_quest = imgProcess.Offset(self.p_roikhoi, -44, -73)
                    autoUtils.click(hwnd, self.p_quest)

                self.p_canve = imgProcess.findImgPoint(self.canve,screen)
                self.p_nhiemvu = imgProcess.findImgPoint(self.nhiemvu,screen,0.6)
                if(self.p_nhiemvu != (0, 0) or self.p_canve != (0, 0)):
                    self.p_quest = imgProcess.Offset(self.p_roikhoi, -68, -124)
                    autoUtils.click(hwnd, self.p_quest)

                self.p_roikhoi = (0, 0)
                self.p_tonle = (0, 0)
                self.p_quest = (0, 0)

            self.p_npc = imgProcess.findImgPoint(self.npc,screen,0.7)
            if(self.p_npc != (0, 0)):
                self.p_nhanQ2 = imgProcess.findImgPoint(self.nhanQ2,screen)
                if (self.p_nhanQ2 != (0, 0)):
                    autoUtils.click(hwnd, self.p_nhanQ2)
                    time.sleep(0.2)
                    autoUtils.click(hwnd, randomLoc)
                    self.p_nhanQ = (0, 0)
                else:
                    self.p_nhanQ = imgProcess.findImgPoint(self.nhanQ, screen)
                    if(self.p_nhanQ != (0, 0)):
                        autoUtils.click(hwnd, self.p_nhanQ)
                        time.sleep(0.2)
                        autoUtils.click(hwnd, randomLoc)
                        self.p_nhanQ = (0, 0)

            self.p_traQ = imgProcess.findImgPoint(self.traQ, screen)
            if(self.p_traQ != (0, 0)):
                autoUtils.click(hwnd, self.p_traQ)
                time.sleep(0.2)
                autoUtils.click(hwnd, randomLoc)
                self.p_traQ = (0, 0)

            time.sleep(delay)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    q = nhantraQ()
    q.show()
    sys.exit(app.exec_())