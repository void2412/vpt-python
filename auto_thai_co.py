from gui import autoTemplate
import imgProcess
import sys

import time
from PyQt5.QtWidgets import *

from autoUtils import thread_with_trace
import win32gui
import autoUtils
import enum

class menu_thai_co(QMainWindow, autoTemplate.Ui_MainWindow):
    def __init__(self):
        super(menu_thai_co, self).__init__()
        self.setupUi(self)
        self.started = False
        self.auto = autoThaiCo()
        self.titleList = [self.lineEdit1, self.lineEdit2, self.lineEdit3, self.lineEdit4, self.lineEdit5]
        self.lineEdit3.setVisible(False)
        self.lineEdit4.setVisible(False)
        self.lineEdit5.setVisible(False)
        self.startBtn.clicked.connect(self.startBtnClicked)
        self.delayLine.setText('500')

    def closeEvent(self, event):
        if self.started == True:
            self.auto.stop()
        event.accept()


    def startBtnClicked(self):
        self.auto.titleList.clear()
        if not self.started:
            self.started = True
            self.startBtn.setText('stop')
            self.auto.delay = int(self.delayLine.text()) * 0.001
            for item in self.titleList:
                if item.text() != "":
                    self.auto.titleList.append(item.text())
            self.auto.state = state.boQ1
            self.auto.start()

        else:
            self.started = False
            self.startBtn.setText('start')
            self.auto.stop()



class state(enum.Enum):
    nhanQ1 = 1
    danhBoss1 = 2
    boQ1 = 3
    doiKeysangacc2 = 7
    nhanQ2 =4
    danhBoss2 = 5
    boQ2 = 6
    doiKeysangacc1 = 8


class autoThaiCo:
    def __init__(self):
        self.thaico = imgProcess.getImg('./img/thai_co/thai_co.png')
        self.thaico2 = imgProcess.getImg('./img/thai_co/thai_co2.png')
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
        self.thongtin = imgProcess.getImg('./img/thai_co/thongtin.png')
        self.thangnhomtruong = imgProcess.getImg('./img/thai_co/thangnhomtruong.png')
        self.nhiemvuopen = imgProcess.getImg('./img/thai_co/nhiemvuopen.png')
        self.titleList = []
        self.handleList = []
        self.auto_thread = None
        self.delay = 0
        self.state = state.boQ1
        self.init = True
        self.clickTC = True

        self.p_bo = ()
        self.p_qphu = ()
        self.p_qphuselected = ()
        self.p_nhiemvu = ()
        self.p_co = ()
        self.p_nhanQ = ()
        self.p_nhanQ2 = ()
        self.p_traQ = ()
        self.p_npc = ()
        self.p_roikhoi = ()
        self.p_quest = ()
        self.p_thaicomathan = ()

    def start(self):
        self.getHandle()
        th = thread_with_trace(target=self.doAuto, args=(self.handleList[0],self.handleList[1], self.delay))
        self.auto_thread = th
        self.auto_thread.start()


    def stop(self):
        self.auto_thread.kill()

    def getHandle(self):
        self.handleList.clear()
        for item in self.titleList:
            hwnd = autoUtils.getHandle(item)
            self.handleList.append(hwnd)

    def doAuto(self, hwnd1, hwnd2, delay):
        while True:
            (x, y, x1, y1) = win32gui.GetWindowRect(hwnd1)

            w = x1 - x
            h = y1 - y

            if w != 1066 or h != 724:
                autoUtils.ResizeWindow(hwnd1)
            (a,b,a1,b1) = win32gui.GetWindowRect(hwnd2)
            w1 = a1 - a
            h1 = b1 - b
            if w1 != 1066 or h1 != 724:
                autoUtils.ResizeWindow(hwnd2)


            if self.state == state.boQ1:
                self.fixThienSu(hwnd1)
                self.fixGiaiTru(hwnd1)
                check = self.boQ1(hwnd1)
                if check is True:
                    self.state = state.nhanQ1

            if self.state == state.nhanQ1:
                self.fixThienSu(hwnd1)
                self.fixGiaiTru(hwnd1)
                check = self.doNhanQ(hwnd1)
                if check is True:
                    self.state = state.danhBoss1

            if self.state == state.danhBoss1:
                self.fixThienSu(hwnd1)
                self.fixGiaiTru(hwnd1)
                check = self.danhboss(hwnd1)
                if check is True:
                    self.state = state.doiKeysangacc2

            if self.state == state.doiKeysangacc2:
                self.fixThienSu(hwnd1)
                self.fixGiaiTru(hwnd1)
                check = self.doiKey(hwnd1)
                if check is True:
                    self.state = state.boQ2

            if self.state == state.boQ2:
                self.fixThienSu(hwnd2)
                self.fixGiaiTru(hwnd2)
                check = self.boQ1(hwnd2)
                if check is True:
                    self.state = state.nhanQ2

            if self.state == state.nhanQ2:
                self.fixThienSu(hwnd2)
                self.fixGiaiTru(hwnd2)
                check = self.doNhanQ(hwnd2)
                if check is True:
                    self.state = state.danhBoss2

            if self.state == state.danhBoss2:
                self.fixThienSu(hwnd2)
                self.fixGiaiTru(hwnd2)
                check = self.danhboss(hwnd2)
                if check is True:
                    self.state = state.doiKeysangacc1

            if self.state == state.doiKeysangacc1:
                self.fixThienSu(hwnd2)
                self.fixGiaiTru(hwnd2)
                check = self.doiKey(hwnd2)
                if check is True:
                    self.state = state.boQ1



            time.sleep(delay)


    def fixThienSu(self,hwnd):
        random = (986,46)
        thiensu = imgProcess.getImg('./img/ok.png')
        autoUtils.click(hwnd,random)
        time.sleep(0.25)
        screen = imgProcess.captureWindow(hwnd)
        checkThiensu = imgProcess.findImgPoint(thiensu,screen)
        if checkThiensu != (0,0):
            autoUtils.click(hwnd,checkThiensu)
            time.sleep(0.5)



    def fixGiaiTru(self,hwnd):
        random = (986,46)
        giaitru = imgProcess.getImg('./img/nhantraQ/co.png')
        autoUtils.click(hwnd, random)
        time.sleep(0.25)
        screen = imgProcess.captureWindow(hwnd)
        checkGiaitru = imgProcess.findImgPoint(giaitru,screen)
        if checkGiaitru != (0,0):
            autoUtils.click(hwnd,checkGiaitru)
            time.sleep(0.5)

    def doiKey(self,hwndkey):
        res = False
        nhom = (850, 649)
        autoUtils.click(hwndkey, nhom)
        time.sleep(0.5)
        screen = imgProcess.captureWindow(hwndkey)
        thangnhom= imgProcess.findImgPoint(self.thangnhomtruong,screen)
        if thangnhom!=(0, 0):
            secondKey = (thangnhom[0] + 12, thangnhom[1] - 146)
            autoUtils.click(hwndkey, secondKey)
            time.sleep(0.5)
            autoUtils.click(hwndkey, thangnhom)
            time.sleep(0.5)
            res = True
        return res


    def danhboss(self,hwnd):
        checkFight = self.checkFight2(hwnd)
        if checkFight is True:
            return True
        else:
            self.clickThaiCo(hwnd)
            return False

    def doNhanQ(self,hwnd):
        res = False
        if self.clickTC is True:
            self.clickThaiCo(hwnd)
            time.sleep(0.5)
        screen = imgProcess.captureWindow(hwnd)
        self.p_roikhoi = imgProcess.findImgPoint(self.roikhoi, screen)
        if self.p_roikhoi != (0, 0):
            self.p_quest = OffsetPoint(self.p_roikhoi, -68, -124)
            autoUtils.click(hwnd, self.p_quest)
            time.sleep(0.5)
            self.p_roikhoi = (0, 0)
            self.p_quest = (0, 0)
            self.clickTC = False
        else:
            self.clickTC = True

        screen = imgProcess.captureWindow(hwnd)
        self.p_npc = imgProcess.findImgPoint(self.npc, screen, 0.7)
        if self.p_npc != (0, 0):
            self.p_nhanQ2 = imgProcess.findImgPoint(self.nhanQ2, screen)
            if self.p_nhanQ2 != (0, 0):
                autoUtils.click(hwnd, self.p_nhanQ2)
                self.p_nhanQ = (0, 0)
            self.clickTC = False

        screen = imgProcess.captureWindow(hwnd)
        self.p_nhanQ = imgProcess.findImgPoint(self.nhanQ, screen)
        if self.p_nhanQ != (0, 0):
            autoUtils.click(hwnd, self.p_nhanQ)
            self.p_nhanQ = (0, 0)
            res = True
            self.clickTC = True
        return res

    def checkNhiemVuBat(self,hwnd):
        screen = imgProcess.captureWindow(hwnd)
        p = imgProcess.findImgPoint(self.npc,screen,0.7)
        if p != (0, 0):
            return True
        else:
            return False

    def boQ1(self, hwnd):
        res = False
        check = self.checkNhiemVuBat(hwnd)
        nv = (982, 649)
        checkFight = self.checkFight(hwnd)
        if checkFight is False:
            if check is False:
                autoUtils.click(hwnd, nv)
                time.sleep(0.5)
            screen = imgProcess.captureWindow(hwnd)
            self.p_npc = imgProcess.findImgPoint(self.npc, screen, 0.7)
            if self.p_npc != (0, 0):
                self.p_thaicomathan = imgProcess.findImgPoint(self.thaicomathan, screen, 0.7)
                thaicoselected = imgProcess.findImgPoint(self.thaicoselected, screen, 0.7)
                if self.p_thaicomathan != (0, 0) or thaicoselected != (0, 0):
                    if self.p_thaicomathan != (0, 0):
                        autoUtils.click(hwnd, self.p_thaicomathan)
                    if thaicoselected != (0, 0):
                        autoUtils.click(hwnd, thaicoselected)
                    time.sleep(0.5)
                    self.boQ(hwnd)
                    res = True
                else:
                    self.p_qphu = imgProcess.findImgPoint(self.qphu, screen)
                    self.p_qphuselected = imgProcess.findImgPoint(self.qphuselected, screen)
                    if self.p_qphuselected != (0, 0):
                        autoUtils.click(hwnd, self.p_qphuselected)
                    else:
                        if self.p_qphu != (0, 0):
                            autoUtils.click(hwnd, self.p_qphu)
                        else:
                            autoUtils.click(hwnd, nv)
                            res = True
                    time.sleep(0.5)
                    screen = imgProcess.captureWindow(hwnd)
                    self.p_thaicomathan = imgProcess.findImgPoint(self.thaicomathan, screen, 0.7)
                    thaicoselected = imgProcess.findImgPoint(self.thaicoselected, screen, 0.7)
                    if self.p_thaicomathan != (0, 0) or thaicoselected != (0, 0):
                        if self.p_thaicomathan != (0, 0):
                            autoUtils.click(hwnd, self.p_thaicomathan)
                        if thaicoselected != (0, 0):
                            autoUtils.click(hwnd, thaicoselected)
                        time.sleep(0.5)
                        self.boQ(hwnd)
                        res = True

        return res

    def boQ(self,hwnd):
        screen = imgProcess.captureWindow(hwnd)
        thaicoselected = imgProcess.findImgPoint(self.thaicoselected, screen, 0.7)
        while thaicoselected != (0, 0):
            autoUtils.click(hwnd, thaicoselected)
            time.sleep(0.5)
            self.p_bo = imgProcess.findImgPoint(self.bo, screen)
            if self.p_bo != (0, 0):
                autoUtils.click(hwnd, self.p_bo)
                time.sleep(0.5)
            screen = imgProcess.captureWindow(hwnd)
            self.p_co = imgProcess.findImgPoint(self.co, screen)
            if self.p_co != (0, 0):
                autoUtils.click(hwnd, self.p_co)
                time.sleep(0.5)
            screen = imgProcess.captureWindow(hwnd)
            thaicoselected = imgProcess.findImgPoint(self.thaicoselected, screen, 0.7)
            time.sleep(0.5)
        screen = imgProcess.captureWindow(hwnd)
        p = imgProcess.findImgPoint(self.nhiemvuopen,screen)
        if p != (0, 0):
            tatnv =OffsetPoint(p, 218, -315)
            autoUtils.click(hwnd, tatnv)

    def clickThaiCo(self,hwnd):
        autoUtils.click(hwnd,(161,605))

    def checkFight(self, hwnd):
        screen = imgProcess.captureWindow(hwnd)
        p = imgProcess.findImgPoint(self.sanxuat, screen)
        if p != (0, 0):
            return False
        else:
            return True

    def checkFight2(self,hwnd):
        screen = imgProcess.captureWindow(hwnd)
        p = imgProcess.findImgPoint(self.thongtin, screen)
        if p != (0, 0):
            return True
        else:
            return False

if __name__ == '__main__':
    app = QApplication(sys.argv)
    q = menu_thai_co()
    q.show()
    sys.exit(app.exec_())
