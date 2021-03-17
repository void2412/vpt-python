from gui import autoTemplate
import AutoUtils
import imgProcess
import sys
import autoit
import time
from PyQt5.QtWidgets import *
from imgProcess import Point
from AutoUtils import thread_with_trace
import win32gui
import AutoUtils
import enum


class menu_thai_co(QMainWindow, autoTemplate.Ui_MainWindow):
    def __init__(self):
        super(menu_thai_co, self).__init__()
        self.setupUi(self)
        self.started = False
        self.auto = autoThaiCo()
        self.titleList = [self.lineEdit1, self.lineEdit2, self.lineEdit3, self.lineEdit4, self.lineEdit5]
        self.startBtn.clicked.connect(self.startBtnClicked)
        self.delayLine.setText('1000')

    def startBtnClicked(self):
        self.auto.titleList.clear()
        if not self.started:
            self.started = True
            self.startBtn.setText('stop')
            self.auto.delay = int(self.delayLine.text()) * 0.001
            for item in self.titleList:
                if item.text() != "":
                    self.auto.titleList.append(item.text())
            self.auto.start()

        else:
            self.started = False
            self.startBtn.setText('start')
            self.auto.stop()


class state(enum.Enum):
    nhanQ = 1
    danhBoss = 2
    boQ = 3


class autoThaiCo:
    def __init__(self):
        self.thaico = imgProcess.getImg('./img/thai_co/thai_co.png')
        self.thaicomathan = imgProcess.getImg('./img/thai_co/thaicomathan.png')
        self.thaicoselected = imgProcess.getImg('./img/thai_co/thaicomathanselected.png')
        self.qphuselected = imgProcess.getImg('./img/thai_co/qphuselected.png')
        self.sanxuat = imgProcess.getImg('./img/thai_co/bay.png')
        self.nhiemvu = imgProcess.getImg('./img/nhantraQ/nhiemvu.png')
        self.co = imgProcess.getImg('./img/nhantraQ/co.png')
        self.nhanQ = imgProcess.getImg('./img/nhantraQ/nhan.png')
        self.nhanQ2 = imgProcess.getImg('./img/nhantraQ/nhan2.png')
        self.traQ = imgProcess.getImg('./img/nhantraQ/xong.png')
        self.npc = imgProcess.getImg('./img/nhantraQ/npc nhiem vu.PNG')
        self.roikhoi = imgProcess.getImg('./img/nhantraQ/roikhoi.png')
        self.qphu = imgProcess.getImg('./img/thai_co/qphu.png')
        self.bo = imgProcess.getImg('./img/thai_co/bo.png')
        self.thaicoQ = imgProcess.getImg('./img/thai_co/thaicoQ.png')
        self.titleList = []
        self.handleList = []
        self.auto_threads = []
        self.delay = 0
        self.state = state.nhanQ

        self.p_bo = Point()
        self.p_qphu = Point()
        self.p_qphuselected = Point()
        self.p_nhiemvu = Point()
        self.p_co = Point()
        self.p_nhanQ = Point()
        self.p_nhanQ2 = Point()
        self.p_traQ = Point()
        self.p_npc = Point()
        self.p_roikhoi = Point()
        self.p_quest = Point()
        self.p_thaicomathan = Point()

    def start(self):
        self.getHandle()
        for item in self.handleList:
            th = thread_with_trace(target=self.doAuto, args=(item, self.delay))
            self.auto_threads.append(th)
        for item in self.auto_threads:
            item.start()
            time.sleep(0.3)

    def stop(self):
        for item in self.auto_threads:
            item.kill()
        self.auto_threads.clear()

    def getHandle(self):
        self.handleList.clear()
        for item in self.titleList:
            hwnd = autoit.win_get_handle(item)
            self.handleList.append(hwnd)

    def doAuto(self, hwnd, delay):
        randomLoc = Point(967, 47)
        nv = Point(982, 649)
        while True:
            (x, y, x1, y1) = win32gui.GetWindowRect(hwnd)
            w = x1 - x
            h = y1 - y
            if w != 106 or h != 724:
                AutoUtils.ResizeWindow(hwnd)

            if self.state == state.nhanQ:
                screen = imgProcess.CaptureWindow(hwnd)
                self.p_roikhoi = imgProcess.findImgPointandFixCoord(self.roikhoi, screen)
                if self.p_roikhoi != Point(0, 0):
                    screen = imgProcess.CaptureWindow(hwnd)
                    self.p_nhiemvu = imgProcess.findImgPointandFixCoord(self.nhiemvu, screen, 0.6)
                    if self.p_nhiemvu != Point(0, 0):
                        self.p_quest = imgProcess.OffsetPoint(self.p_roikhoi, -68, -124)
                        AutoUtils.click(hwnd, self.p_quest)
                    self.p_roikhoi = Point(0, 0)
                    self.p_quest = Point(0, 0)

                self.p_npc = imgProcess.findImgPointandFixCoord(self.npc, screen, 0.7)
                if self.p_npc != Point(0, 0):
                    self.p_nhanQ2 = imgProcess.findImgPointandFixCoord(self.nhanQ2, screen)
                    if self.p_nhanQ2 != Point(0, 0):
                        AutoUtils.click(hwnd, self.p_nhanQ2)
                        time.sleep(0.2)
                        AutoUtils.click(hwnd, randomLoc)
                        self.p_nhanQ = Point(0, 0)

                self.p_nhanQ = imgProcess.findImgPointandFixCoord(self.nhanQ, screen)
                if self.p_nhanQ != Point(0, 0):
                    AutoUtils.click(hwnd, self.p_nhanQ)
                    time.sleep(0.2)
                    AutoUtils.click(hwnd, randomLoc)
                    self.p_nhanQ = Point(0, 0)
                    self.state = state.danhBoss
            if self.state == state.boQ:
                check = self.checkFight(hwnd)
                xongQCheck = self.checkXongQ(hwnd)
                if check is False and xongQCheck is True:
                    AutoUtils.click(hwnd, nv)
                    time.sleep(0.5)
                    screen = imgProcess.CaptureWindow(hwnd)
                    self.p_npc = imgProcess.findImgPoint(self.npc, screen, 0.7)
                    if self.p_npc != Point(0, 0):
                        self.p_thaicomathan = imgProcess.findImgPointandFixCoord(self.thaicomathan, screen, 0.7)
                        thaicoselected = imgProcess.findImgPointandFixCoord(self.thaicoselected, screen, 0.7)
                        if self.p_thaicomathan != Point(0, 0) or thaicoselected != Point(0, 0):
                            if self.p_thaicomathan != Point(0, 0):
                                AutoUtils.click(hwnd, self.p_thaicomathan)
                            if thaicoselected != Point(0, 0):
                                AutoUtils.click(hwnd, thaicoselected)
                            time.sleep(0.5)
                            self.boQ(hwnd)
                        else:
                            self.p_qphu = imgProcess.findImgPointandFixCoord(self.qphu, screen, 0.7)
                            self.p_qphuselected = imgProcess.findImgPointandFixCoord(self.qphuselected, screen)
                            if self.p_qphuselected != Point(0, 0):
                                AutoUtils.click(hwnd, self.p_qphuselected)
                            else:
                                if self.p_qphu != Point(0, 0):
                                    AutoUtils.click(hwnd, self.p_qphu)
                            time.sleep(0.5)
                            screen = imgProcess.CaptureWindow(hwnd)
                            self.p_thaicomathan = imgProcess.findImgPointandFixCoord(self.thaicomathan, screen, 0.7)
                            thaicoselected = imgProcess.findImgPointandFixCoord(self.thaicoselected, screen, 0.7)
                            if self.p_thaicomathan != Point(0, 0) or thaicoselected != Point(0, 0):
                                if self.p_thaicomathan != Point(0, 0):
                                    AutoUtils.click(hwnd, self.p_thaicomathan)
                                if thaicoselected != Point(0, 0):
                                    AutoUtils.click(hwnd, thaicoselected)
                                time.sleep(0.5)
                            self.boQ(hwnd)
            time.sleep(delay)

    def boQ(self, hwnd):
        randomLoc = Point(967, 47)
        screen = imgProcess.CaptureWindow(hwnd)

        thaicoselected = imgProcess.findImgPointandFixCoord(self.thaicoselected, screen, 0.7)
        while thaicoselected != Point(0, 0):
            AutoUtils.click(hwnd, thaicoselected)
            time.sleep(0.5)
            self.p_bo = imgProcess.findImgPointandFixCoord(self.bo, screen)
            if self.p_bo != Point(0,0):
                AutoUtils.click(hwnd, self.p_bo)
            time.sleep(0.5)
            screen = imgProcess.CaptureWindow(hwnd)
            self.p_co = imgProcess.findImgPointandFixCoord(self.co, screen)
            if self.p_co != Point(0, 0):
                AutoUtils.click(hwnd, self.p_co)
                time.sleep(0.5)
                AutoUtils.click(hwnd, randomLoc)
                time.sleep(0.5)
            screen = imgProcess.CaptureWindow(hwnd)
            thaicoselected = imgProcess.findImgPointandFixCoord(self.thaicoselected, screen, 0.7)
            time.sleep(0.5)
        tatnv = Point(self.p_bo.x + 379, self.p_bo.y - 337)
        AutoUtils.click(hwnd, tatnv)

    def checkXongQ(self, hwnd):
        screen = imgProcess.CaptureWindow(hwnd)
        p = imgProcess.findImgPointandFixCoord(self.thaico, screen, 0.999)
        if p != Point(0, 0):
            AutoUtils.click(hwnd, p)
            time.sleep(2)
            screen = imgProcess.CaptureWindow(hwnd)
            p1 = imgProcess.findImgPoint(self.roikhoi, screen)
            if p1 != Point(0, 0):
                return False
            else:
                return True

    def checkFight(self, hwnd):
        screen = imgProcess.CaptureWindow(hwnd)
        p = imgProcess.findImgPoint(self.sanxuat, screen)
        if p != Point(0, 0):
            return False
        else:
            return True


if __name__ == '__main__':
    app = QApplication(sys.argv)
    q = menu_thai_co()
    q.show()
    sys.exit(app.exec_())
