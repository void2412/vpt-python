from gui import autoTM as g

import imgProcess
import sys
import time
from time import sleep
from PyQt5.QtWidgets import *
from imgProcess import *
from autoUtils import *
import win32gui
import enum

class menu_TM(QMainWindow, g.Ui_MainWindow):
    def __init__(self):
        super(menu_TM, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('auto trừ ma')
        self.textBoxList = [self.lineEdit1,self.lineEdit2,self.lineEdit3,self.lineEdit4,self.lineEdit5]
        self.startBtnList = [self.startBtn1,self.startBtn2,self.startBtn3,self.startBtn4,self.startBtn5]
        self.startStateList = [False for _ in range(5)]
        self.autoPool = [None for _ in range(5)]
        self.initBtn()
    def initBtn(self):
        index = 0
        for button in self.startBtnList:
            button.clicked.connect(lambda ch, index = index: self.start(index))
            index += 1

    
    def start(self, index):
        if self.startStateList[index] == False:
            self.startStateList[index] =True
            self.startBtnList[index].setText('stop')
            title = self.textBoxList[index].text().strip()
            self.createAutoObj(index, title)
            self.autoPool[index].start()

        else:
            self.startStateList[index] = False
            self.startBtnList[index].setText('start')
            self.autoPool[index].stop()
            self.autoPool[index] = None


    def createAutoObj(self, index, title):
        auto = auto_TM(title)
        self.autoPool[index] = auto
        pass



class state (enum.Enum):
    traQ = 1
    timDanh = 2
    reset = 3


def checkImg(hwnd, needle, tolerance = 0.9):
    screen = captureWindow(hwnd)
    point = findImgPoint(needle, screen, tolerance)

    if point != Point(0, 0):
        return True
    
    return False

class auto_TM():
    def __init__(self, title):
        self.hwnd = getHandle(title)
        self.thread = None
        self.state = state.timDanh
        self.cuthu = getImg('./img/truma/cuthu.png')
        self.cuma = getImg('./img/truma/cuma.png')
        self.phima = getImg('./img/truma/phima.png')
        self.menu1 = getImg('./img/truma/nhiemvu1.png')
        self.menu2 = getImg('./img/truma/nhiemvu2.png')
        self.xongQ1 = getImg('./img/truma/xongQ.png')
        self.xongQ2 = getImg('./img/truma/xongQ2.png')
        self.loadmap = getImg('./img/truma/loadmap.png')
        self.city = getImg('./img/truma/city.png')
        self.ttl = getImg('./img/truma/ttl.png')
        self.roikhoi = getImg('./img/roikhoi.png')
        self.xong = getImg('./img/nhantraQ/xong.png')
        self.inFight = getImg('./img/truma/inFight.png')
        self.trian = getImg('./img/truma/trian.png')
        self.truma = getImg('./img/truma/truma.png')
        self.phuchoi = getImg('./img/truma/phuchoi.png')
        self.busy = getImg('./img/truma/busy.png')
        self.sanxuat = imgProcess.getImg('./img/sanxuat.png')
        self.currentBoss = None
        x = 156
        self.phimaLoc = [
            Point(x,337),
            Point(x,351),
            Point(x,367),
            Point(x,382),
            Point(x,397)
        ]

        self.cumaLoc = [
            Point(x,412),
            Point(x,425),
            Point(x,442),
            Point(x,455),
            Point(x,469)
        ]

        self.cuthuLoc = [
            Point(x, 486),
            Point(x, 502),
            Point(x, 516),
            Point(x, 532),
            Point(x, 547)
        ]

        self.traQLoc = Point(x, 562)
        self.ttlLoc = Point(x, 576)
        self.cityLoc = Point(x,592)
        self.nhiemvuLoc = Point(979, 648)

        self.checkCurrentBoss()
    
    def fixThienSu(self,hwnd):
        randomPoint = Point(986,46)
        thiensu = getImg('./img/ok.png')
        click(hwnd,randomPoint)
        sleep(0.25)
        screen = captureWindow(hwnd)
        checkThiensu = findImgPoint(thiensu,screen)
        if checkThiensu != Point(0,0):
            click(hwnd,checkThiensu)
            sleep(0.5)
    
    def fixGiaiTru(self,hwnd):
        randomPoint = Point(986,46)
        giaitru = getImg('./img/nhantraQ/co.png')
        click(hwnd, randomPoint)
        sleep(0.25)
        screen = captureWindow(hwnd)
        checkGiaitru = findImgPoint(giaitru,screen)
        if checkGiaitru != Point(0,0):
            click(hwnd,checkGiaitru)
            sleep(0.5)

    def checkCurrentBoss(self):

        check1 = checkImg(self.hwnd, self.phima, 0.8)
        check2 = checkImg(self.hwnd, self.cuma, 0.8)
        check3 = checkImg(self.hwnd, self.cuthu, 0.8)
        check4 = checkImg(self.hwnd, self.xongQ1, 0.8)
        check5 = checkImg(self.hwnd, self.xongQ2, 0.8)

        if check1 is True:
            self.currentBoss = 'phi ma'
            self.state = state.timDanh
        if check2 is True:
            self.currentBoss = 'cu ma'
            self.state = state.timDanh
        if check3 is True:
            self.currentBoss = 'cu thu'
            self.state = state.timDanh
        if check4 is True or check5 is True:
            self.state = state.traQ

        if check1 is False and check2 is False and check3 is False and check4 is False and check5 is False:
            self.state = state.reset

        
    def clickBoss(self):
        if self.currentBoss == 'phi ma':
            for i in range(5):
                click(self.hwnd, self.phimaLoc[i])
                sleep(0.5)
                
                if checkImg(self.hwnd, self.city) is False:
                    sleep(0.5)
                    busy = False
                    backmiddle = False
                    screen = captureWindow(self.hwnd)
                    roikhoiLoc = findImgPoint(self.roikhoi, screen)
                    while roikhoiLoc == Point(0,0):
                        sleep(1)
                        click(self.hwnd, self.phimaLoc[i])
                        sleep(1)
                        busy = checkImg(self.hwnd, self.busy)
                        backmiddle = checkImg(self.hwnd, self.city)
                        if busy is True or backmiddle is True:
                            break
                        
                        screen = captureWindow(self.hwnd)
                        roikhoiLoc = findImgPoint(self.roikhoi, screen)
                        
                    if busy is True or backmiddle is True:
                        continue
                    fightLoc = OffsetPoint(roikhoiLoc, 0, -125)
                    click(self.hwnd, fightLoc)
                    sleep(1)
                    break
                else:
                    continue
        
        if self.currentBoss == 'cu ma':
            for i in range(5):
                click(self.hwnd, self.cumaLoc[i])
                sleep(0.5)
                if checkImg(self.hwnd, self.ttl) is False:
                    sleep(0.5)
                    busy = False
                    backmiddle = False
                    screen = captureWindow(self.hwnd)
                    roikhoiLoc = findImgPoint(self.roikhoi, screen)
                    while roikhoiLoc == Point(0,0):
                        sleep(1)
                        click(self.hwnd, self.cumaLoc[i])
                        sleep(1)
                        busy = checkImg(self.hwnd, self.busy)
                        backmiddle = checkImg(self.hwnd, self.ttl)
                        if busy is True or backmiddle is True:
                            break
                        
                        screen = captureWindow(self.hwnd)
                        roikhoiLoc = findImgPoint(self.roikhoi, screen)
                    if busy is True or backmiddle is True:
                        continue
                    fightLoc = OffsetPoint(roikhoiLoc, 0, -125)
                    click(self.hwnd, fightLoc)
                    sleep(1)
                    break
                else:
                    continue
            pass

        if self.currentBoss == 'cu thu':
            for i in range(5):
                click(self.hwnd, self.cuthuLoc[i])
                sleep(0.5)
                if checkImg(self.hwnd, self.ttl) is False:
                    sleep(0.5)
                    busy = False
                    backmiddle = False
                    screen = captureWindow(self.hwnd)
                    roikhoiLoc = findImgPoint(self.roikhoi, screen)
                    while roikhoiLoc == Point(0,0):
                        sleep(1)
                        click(self.hwnd, self.cuthuLoc[i])
                        sleep(1)
                        busy = checkImg(self.hwnd, self.busy)
                        backmiddle = checkImg(self.hwnd, self.ttl)
                        if busy is True or backmiddle is True:
                            break
                        screen = captureWindow(self.hwnd)
                        roikhoiLoc = findImgPoint(self.roikhoi, screen)

                    if busy is True or backmiddle is True:
                        continue
                    fightLoc = OffsetPoint(roikhoiLoc, 0, -125)
                    click(self.hwnd, fightLoc)
                    sleep(1)
                    break
                else:
                    continue
            pass

    def worker(self):
       
        while True:
            #resize to default window size
            (x, y, x1, y1) = win32gui.GetWindowRect(self.hwnd)

            w = x1 - x
            h = y1 - y

            if w != 1066 or h != 724:
                autoUtils.ResizeWindow(self.hwnd)

            self.fixThienSu(self.hwnd)
            self.fixGiaiTru(self.hwnd)

            if self.state == state.traQ:
                #initial click to change map
                click(self.hwnd, self.traQLoc)
                sleep(1)
                #waiting to load map
                start = time.time()
                while checkImg(self.hwnd, self.loadmap) is True:
                    sleep(2)
                    Next = time.time()
                    if (Next - start) > 60:
                        print('error load map')
                        return
                #click until menu popup
                while checkImg(self.hwnd, self.roikhoi) is False:
                    click(self.hwnd, self.traQLoc)
                    sleep(1)
                #click traQ
                screen = captureWindow(self.hwnd)
                roikhoiLoc = findImgPoint(self.roikhoi, screen)
                QLoc = OffsetPoint(roikhoiLoc, 0, -125)
                click(self.hwnd, QLoc)
                sleep(0.5)
                click(self.hwnd, QLoc)
                sleep(0.5)
                screen = captureWindow(self.hwnd)
                xongLoc = findImgPoint(self.xong, screen)
                click(self.hwnd,xongLoc)
                sleep(0.5)

                #check Boss Type or Quest Finish and set corresponding state/boss
                self.currentBoss = 'reset'
                self.checkCurrentBoss()
                if self.currentBoss == 'reset':
                    self.state = state.reset
                else:
                    self.state = state.timDanh

                sleep(0.5)
                pass

            if self.state == state.timDanh:
                if self.currentBoss == 'phi ma':
                    # click to change map
                    click(self.hwnd, self.cityLoc)
                    sleep(1)
                    #waiting to load map
                    start = time.time()
                    while checkImg(self.hwnd, self.loadmap) is True:
                        sleep(2)
                        Next = time.time()
                        if (Next - start) > 60:
                            print('error load map')
                            return

                    #click Boss phi ma
                    sleep(2)
                    while checkImg(self.hwnd, self.city) is True:
                        self.clickBoss()
                    
                    

                if self.currentBoss == 'cu ma':
                    #click change mapData
                    click(self.hwnd, self.ttlLoc)
                    sleep(1)
                    #waiting to load map
                    start = time.time()
                    while checkImg(self.hwnd, self.loadmap) is True:
                        sleep(2)
                        Next = time.time()
                        if (Next - start) > 60:
                            print('error load map')
                            return

                    #click Boss cu ma
                    sleep(2)
                    while checkImg(self.hwnd, self.ttl) is True:
                        self.clickBoss()
                    

                if self.currentBoss == 'cu thu':
                    #click change mapData
                    click(self.hwnd, self.ttlLoc)
                    sleep(1)
                    #waiting to load map
                    start = time.time()
                    while checkImg(self.hwnd, self.loadmap) is True:
                        sleep(2)
                        Next = time.time()
                        if (Next - start) > 60:
                            print('error load map')
                            return

                    #click Boss cu thu
                    sleep(2)
                    while checkImg(self.hwnd, self.ttl) is True:
                        self.clickBoss()

                
                #wait for get in Fight
                stuckWait = False
                start = time.time()
                while checkImg(self.hwnd, self.inFight) is False:
                    sleep(1)
                    stop = time.time()
                    if (stop - start) > 30:
                        if checkImg(self.hwnd, self.xongQ1) is True:
                            break
                        if checkImg(self.hwnd, self.xongQ2) is True:
                            break
                        #ve dht
                        click(self.hwnd, self.traQLoc)
                        #load map
                        start = time.time()
                        while checkImg(self.hwnd, self.loadmap) is True:
                            sleep(2)
                            Next = time.time()
                            if (Next - start) > 60:
                                print('error load map')
                                return
                        stuckWait = True

                #wait for fight Finish
                
                while checkImg(self.hwnd, self.inFight) is True:
                    sleep(1)
                    
                    
                #Restore Hp/Mp
                sleep(1)
                click(self.hwnd, Point(130, 26))
                click(self.hwnd, Point(130, 26))
                sleep(1)
                click(self.hwnd,Point(117, 85))
                click(self.hwnd,Point(117, 85))
                
                #set state
                if stuckWait == False:
                    self.state = state.traQ
                else:
                    self.checkCurrentBoss()
                sleep(0.5)


            if self.state == state.reset:
                click(self.hwnd, self.nhiemvuLoc)
                sleep(0.5)
                screen = captureWindow(self.hwnd)
                cothenhanPoint = findImgPoint(self.menu1, screen)
                if cothenhanPoint == Point(0,0):
                    cothenhanPoint = findImgPoint(self.menu2, screen)
                
                lienhoanPoint = OffsetPoint(cothenhanPoint, 75, 0)
                exitPoint = OffsetPoint(cothenhanPoint, 347, -35)
                click(self.hwnd, lienhoanPoint)
                sleep(0.5)
                screen = captureWindow(self.hwnd)
                trianLoc = findImgPoint(self.trian, screen, 0.7)
                trumaLoc = findImgPoint(self.truma, screen, 0.7)
                click(self.hwnd, trianLoc)
                sleep(0.5)
                click(self.hwnd, trumaLoc)
                sleep(0.5)
                screen = captureWindow(self.hwnd)
                phuchoiLoc = findImgPoint(self.phuchoi, screen)
                click(self.hwnd, phuchoiLoc)
                sleep(0.5)
                click(self.hwnd, exitPoint)
                self.state = state.timDanh
                sleep(0.5)
                self.checkCurrentBoss()
                pass


    def start(self):
        th = thread_with_trace(target = self.worker)
        th.setDaemon(True)
        self.thread = th
        self.thread.start()
        pass

    def stop(self):
        self.thread.kill()
        self.thread = None

        pass




if __name__ == "__main__":
    app = QApplication(sys.argv)
    tm = menu_TM()
    tm.show()
    sys.exit(app.exec_())