import win32gui

import autoUtils
import enum
from time import sleep
from autoUtils import thread_with_trace,click
from gui import thuthapnl
import sys
from PyQt5.QtWidgets import *
from imgProcess import getImg,captureWindow,findImgPoint
class caytrong(enum.Enum):
    luamach = 'Lúa mạch (lv1)'
    luagao = 'Lúa gạo (lv1)'
    bap = 'Bắp (lv2)'
    khoailang = 'Khoai lang (lv2)'
    dauphong = 'Đậu phộng (lv3)'
    daunanh = 'Đậu nành (lv3)'
    caithao = 'Cải thảo (lv4)'
    cucai = 'Củ cải (lv4)'
    cacao = 'Cacao (lv5)'
    caoluong = 'Cao lương (lv5)'
    muop = 'Mướp (lv6)'
    bau = 'Bầu (lv6)'
    bongcai = 'Bông cải (lv7)'
    hoangkimqua = 'Hoàng kim quả (lv7)'


class trongcay(QMainWindow,thuthapnl.Ui_MainWindow):
    def __init__(self):
        super(trongcay, self).__init__()
        self.setupUi(self)
        self.buttons = [self.startBtn1,self.startBtn2,self.startBtn3,self.startBtn4,self.startBtn5]
        self.textboxs = [self.lineEdit1,self.lineEdit2,self.lineEdit3,self.lineEdit4,self.lineEdit5]
        self.dropdownboxs = [self.comboBox1,self.comboBox2,self.comboBox3,self.comboBox4,self.comboBox5]
        self.startStates = [False,False,False,False,False]
        self.checkBoxs = [self.checkBox1,self.checkBox2,self.checkBox3,self.checkBox4,self.checkBox5]
        self.autos = [None]*5
        self.delayLine.setText('3000')
        self.threads = [None]*5
        self.initBtn()
        self.initCombo()

    def initBtn(self):
        index = 0
        for button in self.buttons:
            button.clicked.connect(lambda ch,index = index: self.start(index))
            index = index + 1

    def initCombo(self):
        for item in self.dropdownboxs:
            for x in caytrong:
                item.addItem(x.value)

    def createAuto(self,index, title, caytrong, daingay, delay):
        auto = autoLogic(title,caytrong, daingay, delay)
        self.autos[index]=auto

    def getCayTrong(self,caytrongstr):
        for item in caytrong:
            if item.value == caytrongstr:
                return item

    def start(self,index):
        if (self.startStates[index] == False):
            self.startStates[index] = True
            self.dropdownboxs[index].setEnabled(False)
            self.textboxs[index].setEnabled(False)
            self.checkBoxs[index].setEnabled(False)
            self.buttons[index].setText('stop')
            title = self.textboxs[index].text()
            delay = int(self.delayLine.text()) * 0.001
            caytrongstr = self.dropdownboxs[index].currentText()
            caytrongVal = self.getCayTrong(caytrongstr)
            daingay = self.checkBoxs[index].isChecked()
            hwnd = autoUtils.getHandle(title)
            self.createAuto(index,hwnd,caytrongVal,daingay,delay)
            self.autos[index].start()
        else:
            self.startStates[index] = False
            self.textboxs[index].setEnabled(True)
            self.dropdownboxs[index].setEnabled(True)
            self.checkBoxs[index].setEnabled(True)
            self.buttons[index].setText('start')
            self.autos[index].stop()
            self.autos[index] = None

class trongcayState(enum.Enum):
    trongcay = 1
    chocaychin = 2
    thuhoach = 3

class autoLogic():
    def __init__(self, hwnd, caytrong,daingay,delay):
        self.hwnd = hwnd
        self.caytrong = caytrong
        self.delay = delay
        self.state = trongcayState.trongcay
        self.daingay =  daingay
        self.khong = getImg('./img/khong.png')
        self.ok = getImg('./img/ok.png')
        self.roikhoi = getImg('./img/roikhoi.png')
        self.thread = None

    def start(self):
        th = thread_with_trace(target=self.doAuto, args=(self.hwnd,))
        th.setDaemon(True)
        self.thread = th
        self.thread.start()

    def stop(self):
        self.thread.kill()
        self.thread = None

    def doAuto(self, hwnd):
        while True:
            (x, y, x1, y1) = win32gui.GetWindowRect(hwnd)
            w = x1 - x
            h = y1 - y
            if w != 1066 or h != 724:
                autoUtils.ResizeWindow(hwnd)

            self.fixThiensu(hwnd)
            self.fixKetBan(hwnd)

            if self.state == trongcayState.trongcay:
                check = self.trongcay(hwnd)
                if check is True:
                    self.state = trongcayState.chocaychin

            if self.state == trongcayState.chocaychin:
                check = self.checkCayChin(hwnd)
                if check is True:
                    self.state = trongcayState.thuhoach

            if self.state == trongcayState.thuhoach:
                check = self.thuhoach(hwnd)
                if check is True:
                    self.state = trongcayState.trongcay
            sleep(self.delay)

    def fixThiensu(self,hwnd):
        empty = (0,0)
        screen = captureWindow(hwnd)
        point = findImgPoint(self.ok,screen)
        if point != empty:
            click(hwnd,point)
        sleep(0.5)

    def fixKetBan(self,hwnd):
        empty = (0, 0)
        screen = captureWindow(hwnd)
        point = findImgPoint(self.khong, screen)
        if point != empty:
            click(hwnd, point)
        sleep(0.5)

    def trongcay(self,hwnd):
        empty = (0,0)
        short_term_tree = (-42,-124)
        long_term_tree = (-42,-98)
        npc_code = (161,605)
        click(hwnd,npc_code)
        sleep(0.5)
        screen = captureWindow(hwnd)
        roikhoi = findImgPoint(self.roikhoi,screen)
        if roikhoi != empty:
            if self.daingay is True:
                click(hwnd,roikhoi + long_term_tree)
                sleep(0.5)
            else:
                click(hwnd,roikhoi+ short_term_tree)
                sleep(0.5)
            screen = captureWindow(hwnd)
            roikhoi = findImgPoint(self.roikhoi,screen)
            if roikhoi != empty:
                self.choncay(hwnd,roikhoi,self.caytrong)
                return True

        return False

    def choncay(self,hwnd,base,tree):
        last = base - (42,24)
        moveDown = base + (96,-27)
        moveUp = base + (96,-127)
        def getDown(num):
            for i in range(num):
                click(hwnd,moveDown)
                sleep(0.2)
            sleep(0.5)
            click(hwnd,last)

        for i in range(10):
            click(hwnd,moveUp)
            sleep(0.2)
        sleep(0.3)
        if tree == caytrong.luamach:
            click(hwnd,base-(42,124))
        if tree == caytrong.luagao:
            click(hwnd,base-(42,98))
        if tree == caytrong.bap:
            click(hwnd,base-(42,74))
        if tree == caytrong.khoailang:
            click(hwnd,base - (42,49))
        if tree == caytrong.dauphong:
            click(hwnd,last)
        if tree == caytrong.daunanh:
            getDown(1)
        if tree == caytrong.caithao:
            getDown(2)
        if tree == caytrong.cucai:
            getDown(3)
        if tree == caytrong.cacao:
            getDown(4)
        if tree == caytrong.caoluong:
            getDown(5)
        if tree == caytrong.muop:
            getDown(6)
        if tree == caytrong.bap:
            getDown(7)
        if tree == caytrong.bongcai:
            getDown(8)
        if tree == caytrong.hoangkimqua:
            getDown(9)
        sleep(0.5)



    def checkCayChin(self,hwnd):
        empty = (0, 0)
        needle=getImg('./img/trongcay/cayChin.png')
        screen = captureWindow(hwnd)
        point = findImgPoint(needle,screen)
        if point != empty:
            click(hwnd,point)
            sleep(0.5)
            return True
        return False

    def thuhoach(self,hwnd):
        empty = (0, 0)
        needle = getImg('./img/trongcay/crop.png')
        screen = captureWindow(hwnd)
        point = findImgPoint(needle, screen)
        if point != empty:
            click(hwnd,point)
            sleep(6)
            return True
        return False



if __name__ == '__main__':
    app = QApplication(sys.argv)
    trongcay = trongcay()
    trongcay.show()
    sys.exit(app.exec_())