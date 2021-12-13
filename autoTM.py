from gui import autoTM as g
import pynput
from pynput import keyboard
import imgProcess
import sys
import time
from time import sleep
from PyQt5.QtWidgets import *
from imgProcess import *
from autoUtils import *
import win32gui
import enum
from threading import Lock
from pynput.mouse import Controller
from wincap import *

listener = None
tempLocphima =[]
tempLoccuma = []
tempLoccuthu =[]
tempLocnpc =[]
wincapThread = [None for _ in range(5)]
mouse = Controller()
class menu_TM(QMainWindow, g.Ui_MainWindow):
    def __init__(self):
        super(menu_TM, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('auto trừ ma')
        self.getCodeList = [self.getCodeBtn1, self.getCodeBtn2, self.getCodeBtn3, self.getCodeBtn4, self.getCodeBtn5]
        self.textBoxList = [self.lineEdit1,self.lineEdit2,self.lineEdit3,self.lineEdit4,self.lineEdit5]
        self.startBtnList = [self.startBtn1,self.startBtn2,self.startBtn3,self.startBtn4,self.startBtn5]
        self.startStateList = [False for _ in range(5)]
        self.autoPool = [None for _ in range(5)]
        self.phimaLoc = [None for _ in range(5)]
        self.cumaLoc = [None for _ in range(5)]
        self.cuthuLoc = [None for _ in range(5)]
        self.npcLoc = [None for _ in range(5)]
        self.checkLagThread = [None for _ in range(5)]
        
        self.initBtn()
        self.initBtnCode()
        
        

    def initBtn(self):
        index = 0
        for button in self.startBtnList:
            button.clicked.connect(lambda ch, index = index: self.start(index))
            index += 1
        
        
        
        self.copyBtn.clicked.connect(self.copy)

    def initBtnCode(self):
        index = 0
        for button in self.getCodeList:
            button.clicked.connect(lambda ch, index = index: self.getCode(index))
            index += 1
    
    def copy(self):
        textBoxNo = self.spinBox.value() - 1
        self.copyLoc(textBoxNo)

    
    def copyLoc(self, index):
        for i in range(5):
            if i != index:
                self.phimaLoc[i] = self.phimaLoc[index]
                self.cumaLoc[i] = self.cumaLoc[index]
                self.cuthuLoc[i] = self.cuthuLoc[index]
        
        for i in range(5):
            if i != index:
                self.npcLoc[i] = self.npcLoc[index]

    def start(self, index):
        if self.startStateList[index] == False:
            self.startStateList[index] =True
            self.startBtnList[index].setText('stop')
            title = self.textBoxList[index].text().strip()
            if self.delayText.text().strip() == '':
                delay = 0
            else:
                delay = float(self.delayText.text().strip())
            global wincapThread
            wincapThread[index] = WindowCapture(title)
            wincapThread[index].start()
            sleep(0.5)

            self.createAutoObj(index, title, self.phimaLoc[index], self.cumaLoc[index],self.cuthuLoc[index], self.npcLoc[index], delay)
            self.checkLagThread[index] = checkLag(getHandle(title),index, self.autoPool[index],self.npcLoc[index])
            self.checkLagThread[index].start()
            self.autoPool[index].start()

        else:
            self.startStateList[index] = False
            self.startBtnList[index].setText('start')
            self.autoPool[index].stop()
            self.checkLagThread[index].stop()
            self.checkLagThread[index] = None
            self.autoPool[index] = None
            


    def getCode(self, index):
        global listener
        global tempLocphima 
        global tempLoccuma 
        global tempLoccuthu 
        global tempLocnpc 

        tempLocphima =[]
        tempLoccuma = []
        tempLoccuthu =[]
        tempLocnpc =[]
        self.getCodeList[index].setEnabled(False)

        listener = keyboard.Listener(on_release=lambda event: self.on_release(event, index = index))
        listener.setDaemon(True)
        listener.start()
        

        
        pass


    def on_press(self, key):
        try:
            print('alphanumeric key {0} pressed'.format(
                key.char))
        except AttributeError:
            print('special key {0} pressed'.format(
                key))
        pass

    def on_release(self, key, index):
        
        global mouse
        global tempLocphima
        global tempLoccuma
        global tempLoccuthu
        global tempLocnpc
        try:
            if key.char == '1':
                tempLocphima.append(mouse.position)
                pass

            if key.char == '2':
                tempLoccuma.append(mouse.position)
                pass

            if key.char == '3':
                tempLoccuthu.append(mouse.position)
                pass
            
            if key.char == '4':
                tempLocnpc.append(mouse.position)
                pass
        except AttributeError:
            pass
            
        if key == keyboard.Key.enter:
            hwnd = getHandle(self.textBoxList[index].text().strip())
            for i in range(len(tempLocphima)):
                pos = screenToclient(hwnd, tempLocphima[i])
                tempLocphima[i] = pos

            for i in range(len(tempLoccuma)):
                pos = screenToclient(hwnd, tempLoccuma[i])
                tempLoccuma[i] = pos

            for i in range(len(tempLoccuthu)):
                pos = screenToclient(hwnd, tempLoccuthu[i])
                tempLoccuthu[i] = pos

            for i in range(len(tempLocnpc)):
                pos = screenToclient(hwnd, tempLocnpc[i])
                tempLocnpc[i] = pos

            self.phimaLoc[index] = tempLocphima
            self.cumaLoc[index] = tempLoccuma
            self.cuthuLoc[index] = tempLoccuthu
            self.npcLoc[index] = tempLocnpc
            self.getCodeList[index].setEnabled(True)
            return False

    def createAutoObj(self, index, title, phima, cuma, cuthu, npc, delay):
        
        auto = auto_TM(title,phima, cuma, cuthu, npc, index, delay)
        self.autoPool[index] = auto
        pass
    
  


class state (enum.Enum):
    traQ = 1
    timDanh = 2
    reset = 3


def checkImg(index, needle, tolerance = 0.9):
    global wincapThread
    screen = wincapThread[index].screenshot
    point = findImgPoint(needle, screen, tolerance)

    if point != (0, 0):
        return True
    
    return False


class checkLag():
    def __init__(self, hwnd, index, autoObj, npc):
        global wincapThread
        self.wincapThread = wincapThread[index]
        self.hwnd = hwnd
        self.thread = None
        self.city = getImg('./img/truma/bbttext.png')
        self.dht = getImg('./img/truma/dhttext.png')
        self.ttl = getImg('./img/truma/ttltext.png')
        self.inFight = getImg('./img/truma/inFight.png')
        self.thegioi1 = imgProcess.getImg('./img/truma/thegioi1.png')
        self.thegioi2 = imgProcess.getImg('./img/truma/thegioi2.png')
        self.loadmap = getImg('./img/truma/loadmap.png')
        self.traQLoc = npc[0]
        self.currentLoc = None
        self.lastLoc = None
        self.state = 'normal'
        self.lock = Lock()
        self.index = index
        self.auto = autoObj

    def fixLag(self, hwnd):
        self.lock.acquire()
        lagState = self.state
        self.lock.release()

        if lagState == 'lag map':
            self.auto.stop()
            sendKey(hwnd, win32con.VK_ESCAPE)
            sleep(1)
            click(hwnd, (919, 117))
            sleep(0.5)
            click(hwnd, (963, 46))
            sleep(1)
            #click the gioi
            screen = self.wincapThread.screenshot
            thegioiPoint = findImgPoint(self.thegioi1, screen)
            thegioiPoint1 = findImgPoint(self.thegioi2, screen)
            while thegioiPoint == (0,0) and thegioiPoint1 == (0,0):
                screen = self.wincapThread.screenshot
                thegioiPoint = findImgPoint(self.thegioi1, screen)
                thegioiPoint1 = findImgPoint(self.thegioi2, screen)
            
            if thegioiPoint != (0, 0):
                click(hwnd, thegioiPoint)
            elif thegioiPoint1 != (0, 0):
                click(hwnd, thegioiPoint1)
            
            sleep(1)
            click(hwnd, (508,490))
            #check load map
            sleep(1)
            start = time.time()
            while checkImg(self.index, self.loadmap) is True:
                sleep(1)
                Next = time.time()
                if (Next - start) > 60:
                    print('error load map')
                    return
            
            #back to dht
            sleep(1)
            click(hwnd, self.traQLoc)
            #check load map
            sleep(3)
            start = time.time()
            while checkImg(self.index, self.loadmap) is True:
                sleep(2)
                Next = time.time()
                if (Next - start) > 60:
                    print('error load map')
                    return
            sleep(2)
            self.auto.start()
            self.state = 'normal'
            pass

        if lagState == 'f5':
            pass

        pass

    def worker(self):
        while True:
            
            self.getCurrentLoc()

            if self.currentLoc != self.lastLoc:
                self.lastLoc = self.currentLoc
                if self.state != 'normal':
                    self.lock.acquire()
                    self.state = 'normal'
                    self.lock.release()
                
            else:
                start = time.time()
                while self.currentLoc == self.lastLoc:
                    sleep(1)
                    self.getCurrentLoc()
                    if self.currentLoc != self.lastLoc:
                        break
                    else:
                        stop = time.time()
                        print(stop - start)
                        if (stop - start) > 180:
                            if self.currentLoc == 'city' or self.currentLoc == 'dht' or self.currentLoc == 'ttl':
                                self.lock.acquire()
                                self.state = 'lag map'
                                self.lock.release()
                                self.fixLag(self.hwnd)
                            
                            if self.currentLoc == 'fight':
                                self.lock.acquire()
                                self.state = 'lag f5'
                                self.lock.release()
                                self.fixLag(self.hwnd)
                            pass
                    

            sleep(1)

        pass


    def getCurrentLoc(self):
        screen = self.wincapThread.screenshot
        cityCheck = findImgPoint(self.city, screen)
        dhtCheck = findImgPoint(self.dht, screen)
        ttlCheck = findImgPoint(self.ttl, screen)
        fightCheck = findImgPoint(self.inFight, screen)

        if cityCheck != (0, 0):
            self.currentLoc = 'city'
        
        if dhtCheck != (0, 0):
            self.currentLoc = 'dht'

        if ttlCheck != (0, 0):
            self.currentLoc = 'ttl'

        if fightCheck != (0, 0):
            self.currentLoc = 'fight'

    def start(self):
        th = thread_with_trace(target=self.worker)
        th.setDaemon(True)
        self.thread = th
        self.thread.start()
        pass

    def stop(self):
        self.thread.kill()
        self.thread = None
        pass

class hpmp():
    def __init__(self,hwnd, index):
        global wincapThread
        self.wincapThread = wincapThread[index]
        self.hwnd = hwnd
        self.sanxuat = imgProcess.getImg('./img/sanxuat.png')
        self.thread = None
        self.index = index

    def worker(self):
        while True:
            
            if checkImg(self.index, self.sanxuat) is True:
                
                click(self.hwnd, (130, 26))
                click(self.hwnd, (130, 26))
                sleep(1)
                click(self.hwnd,(117, 85))
                click(self.hwnd,(117, 85))
            sleep(1)
    
   

    def start(self):
        th = thread_with_trace(target=self.worker)
        th.setDaemon(True)
        self.thread = th
        self.thread.start()

    def stop(self):
        self.thread.kill()
        
        pass

class auto_TM():
    def __init__(self, title,phima, cuma, cuthu, npc, index, delay):
        global wincapThread
        self.index = index
        self.wincapThread = wincapThread[index]
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
        self.bosstext = imgProcess.getImg('./img/truma/bossTalk.png')
        
        self.qqnTalk = imgProcess.getImg('./img/truma/qqnTalk.png')
        self.dht = imgProcess.getImg('./img/truma/dhttext.png')
        self.currentBoss = None
        self.delay = delay
        self.phimaLoc = phima

        self.cumaLoc = cuma

        self.cuthuLoc = cuthu

        self.traQLoc = npc[0]
        self.ttlLoc = npc[1]
        self.cityLoc = npc[2]
        self.nhiemvuLoc = (979, 648)

        self.checkCurrentBoss()

        
        #lag stuff
        
        #hp mp stuff
        self.hpmp = hpmp(self.hwnd, index)
    
    def fixThienSu(self,hwnd):
        random = (986,46)
        thiensu = getImg('./img/ok.png')
        click(hwnd,random)
        sleep(0.25)
        screen = self.wincapThread.screenshot
        checkThiensu = findImgPoint(thiensu,screen)
        if checkThiensu != (0,0):
            click(hwnd,checkThiensu)
    
    def fixGiaiTru(self,hwnd):
        random = (986,46)
        giaitru = getImg('./img/nhantraQ/co.png')
        click(hwnd, random)
        sleep(0.25)
        screen = self.wincapThread.screenshot
        checkGiaitru = findImgPoint(giaitru,screen)
        if checkGiaitru != (0,0):
            click(hwnd,checkGiaitru)
    
    def fixKetBan(self,hwnd):
        random = (986,46)
        giaitru = getImg('./img/khong.png')
        click(hwnd, random)
        sleep(0.25)
        screen = self.wincapThread.screenshot
        checkGiaitru = findImgPoint(giaitru,screen)
        if checkGiaitru != (0,0):
            click(hwnd,checkGiaitru)


    def checkCurrentBoss(self):

        check1 = checkImg(self.index, self.phima, 0.8)
        check2 = checkImg(self.index, self.cuma, 0.8)
        check3 = checkImg(self.index, self.cuthu, 0.8)
        check4 = checkImg(self.index, self.xongQ1, 0.8)
        check5 = checkImg(self.index, self.xongQ2, 0.8)

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
                
                if checkImg(self.index, self.city) is False:
                    sleep(0.5)
                    busy = False
                    backmiddle = False
                    screen = self.wincapThread.screenshot
                    roikhoiLoc = findImgPoint(self.roikhoi, screen)
                    bossMenu = findImgPoint(self.bosstext, screen)
                    while roikhoiLoc == (0,0) or bossMenu == (0,0):
                        
                        click(self.hwnd, self.phimaLoc[i])
                        sleep(0.6)
                        busy = checkImg(self.index, self.busy)
                        backmiddle = checkImg(self.index, self.city)
                        if busy is True or backmiddle is True:
                            break
                        
                        screen = self.wincapThread.screenshot
                        roikhoiLoc = findImgPoint(self.roikhoi, screen)
                        bossMenu = findImgPoint(self.bosstext, screen)

                    if busy is True or backmiddle is True:
                        continue
                    fightLoc = OffsetPoint(roikhoiLoc, 0, -125)
                    click(self.hwnd, fightLoc)
                    
                    break
                else:
                    continue
        
        if self.currentBoss == 'cu ma':
            for i in range(5):
                click(self.hwnd, self.cumaLoc[i])
                sleep(0.5)
                if checkImg(self.index, self.ttl) is False:
                    sleep(0.5)
                    busy = False
                    backmiddle = False
                    screen = self.wincapThread.screenshot
                    roikhoiLoc = findImgPoint(self.roikhoi, screen)
                    bossMenu = findImgPoint(self.bosstext, screen)
                    while roikhoiLoc == (0,0) or bossMenu == (0,0):
                        
                        click(self.hwnd, self.cumaLoc[i])
                        sleep(0.6)
                        busy = checkImg(self.index, self.busy)
                        backmiddle = checkImg(self.index, self.ttl)
                        if busy is True or backmiddle is True:
                            break
                        
                        screen = self.wincapThread.screenshot
                        roikhoiLoc = findImgPoint(self.roikhoi, screen)
                        bossMenu = findImgPoint(self.bosstext, screen)

                    if busy is True or backmiddle is True:
                        continue
                    fightLoc = OffsetPoint(roikhoiLoc, 0, -125)
                    click(self.hwnd, fightLoc)
                    
                    break
                else:
                    continue
            pass

        if self.currentBoss == 'cu thu':
            for i in range(5):
                click(self.hwnd, self.cuthuLoc[i])
                sleep(0.5)
                if checkImg(self.index, self.ttl) is False:
                    sleep(0.6)
                    busy = False
                    backmiddle = False
                    screen = self.wincapThread.screenshot
                    roikhoiLoc = findImgPoint(self.roikhoi, screen)
                    bossMenu = findImgPoint(self.bosstext, screen)
                    while roikhoiLoc == (0,0) or bossMenu == (0,0):
                        
                        click(self.hwnd, self.cuthuLoc[i])
                        sleep(0.5)
                        busy = checkImg(self.index, self.busy)
                        backmiddle = checkImg(self.index, self.ttl)
                        if busy is True or backmiddle is True:
                            break
                        screen = self.wincapThread.screenshot
                        roikhoiLoc = findImgPoint(self.roikhoi, screen)
                        bossMenu = findImgPoint(self.bosstext, screen)

                    if busy is True or backmiddle is True:
                        continue
                    fightLoc = OffsetPoint(roikhoiLoc, 0, -125)
                    click(self.hwnd, fightLoc)
                    
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
                ResizeWindow(self.hwnd)

            self.fixThienSu(self.hwnd)
            self.fixKetBan(self.hwnd)            
            
            if self.state == state.traQ:
                #initial click to change map
                click(self.hwnd, self.traQLoc)
                
                #waiting to load map
                start = time.time()
                while checkImg(self.index, self.loadmap) is True:
                    sleep(1)
                    Next = time.time()
                    if (Next - start) > 60:
                        print('error load map')
                        return
                while checkImg(self.index, self.dht) is False:
                    sleep(0.2)
                #click until menu popup
                
                if self.delay!= 0:
                    sleep(self.delay)
                while checkImg(self.index, self.roikhoi) is False or checkImg(self.index, self.qqnTalk) is False:
                    click(self.hwnd, self.traQLoc)
                    sleep(0.6)
                #click traQ
                
                screen = self.wincapThread.screenshot
                roikhoiLoc = findImgPoint(self.roikhoi, screen)
                QLoc = OffsetPoint(roikhoiLoc, 0, -125)
                click(self.hwnd, QLoc)
                sleep(0.5)
                while checkImg(self.index, self.roikhoi) is False or checkImg(self.index, self.qqnTalk) is False:
                    click(self.hwnd, self.traQLoc)
                    sleep(0.5)
                click(self.hwnd, QLoc)
                sleep(0.5)
                while checkImg(self.index, self.xong) is False:
                    sleep(0.5)
                screen = self.wincapThread.screenshot
                xongLoc = findImgPoint(self.xong, screen)
                click(self.hwnd,xongLoc)
                sleep(1)

                #check Boss Type or Quest Finish and set corresponding state/boss
                self.currentBoss = 'reset'
                self.checkCurrentBoss()
                if self.currentBoss == 'reset':
                    self.state = state.reset
                else:
                    self.state = state.timDanh

                
                pass

            if self.state == state.timDanh:
                if self.currentBoss == 'phi ma':
                    # click to change map
                    click(self.hwnd, self.cityLoc)
                    sleep(0.6)
                    #waiting to load map
                    start = time.time()
                    while checkImg(self.index, self.loadmap) is True:
                        sleep(0.5)
                        Next = time.time()
                        if (Next - start) > 60:
                            print('error load map')
                            return
                    while checkImg(self.index, self.city) is False:
                        sleep(0.2)
                    #click Boss phi ma
                    if (self.delay != 0):
                        sleep(self.delay)
                    while checkImg(self.index, self.city) is True:
                        self.clickBoss()
                    
                    

                if self.currentBoss == 'cu ma':
                    #click change mapData
                    click(self.hwnd, self.ttlLoc)
                    
                    #waiting to load map
                    start = time.time()
                    while checkImg(self.index, self.loadmap) is True:
                        sleep(0.5)
                        Next = time.time()
                        if (Next - start) > 60:
                            print('error load map')
                            return
                    while checkImg(self.index, self.ttl) is False:
                        sleep(0.2)
                    #click Boss cu ma
                    if(self.delay != 0):
                        sleep(self.delay)
                    while checkImg(self.index, self.ttl) is True:
                        self.clickBoss()
                    

                if self.currentBoss == 'cu thu':
                    #click change mapData
                    click(self.hwnd, self.ttlLoc)
                    
                    #waiting to load map
                    start = time.time()
                    while checkImg(self.index, self.loadmap) is True:
                        sleep(0.5)
                        Next = time.time()
                        if (Next - start) > 60:
                            print('error load map')
                            return
                    while checkImg(self.index, self.ttl) is False:
                        sleep(0.2)
                    #click Boss cu thu
                    if self.delay != 0:
                        sleep(self.delay)
                    while checkImg(self.index, self.ttl) is True:
                        self.clickBoss()

                
                #wait for get in Fight
                stuckWait = False
                start = time.time()
                while checkImg(self.index, self.inFight) is False:
                    sleep(0.2)
                    stop = time.time()
                    if (stop - start) > 30:
                        if checkImg(self.index, self.xongQ1) is True:
                            break
                        if checkImg(self.index, self.xongQ2) is True:
                            break
                        #ve dht
                        click(self.hwnd, self.traQLoc)
                        #load map
                        start = time.time()
                        while checkImg(self.index, self.loadmap) is True:
                            sleep(0.5)
                            Next = time.time()
                            if (Next - start) > 60:
                                print('error load map')
                                return
                        stuckWait = True

                #wait for fight Finish
                
                while checkImg(self.index, self.inFight) is True:
                    sleep(0.2)
                    
                    
                
                
                
                #set state
                if stuckWait == False:
                    self.state = state.traQ
                else:
                    self.checkCurrentBoss()
                


            if self.state == state.reset:
                click(self.hwnd, self.nhiemvuLoc)
                sleep(0.5)
                screen = self.wincapThread.screenshot
                cothenhan = findImgPoint(self.menu1, screen)
                if cothenhan == (0,0):
                    cothenhan = findImgPoint(self.menu2, screen)
                
                lienhoan = OffsetPoint(cothenhan, 75, 0)
                exitP = OffsetPoint(cothenhan, 347, -35)
                click(self.hwnd, lienhoan)
                sleep(0.5)
                screen = self.wincapThread.screenshot
                trianLoc = findImgPoint(self.trian, screen, 0.7)
                trumaLoc = findImgPoint(self.truma, screen, 0.7)
                click(self.hwnd, trianLoc)
                sleep(0.5)
                click(self.hwnd, trumaLoc)
                sleep(0.5)
                screen = self.wincapThread.screenshot
                phuchoiLoc = findImgPoint(self.phuchoi, screen)
                click(self.hwnd, phuchoiLoc)
                sleep(0.5)
                click(self.hwnd, exitP)
                self.state = state.timDanh
                sleep(1)
                self.checkCurrentBoss()
                
                pass
            
            


    def start(self):
        th = thread_with_trace(target = self.worker)
        th.setDaemon(True)
        self.thread = th
        
        self.thread.start()
        
        
        self.hpmp.start()
        pass

    def stop(self):
        
        if self.thread.killed == False:
            self.hpmp.stop()
            self.thread.kill()

        pass




if __name__ == "__main__":
    app = QApplication(sys.argv)
    tm = menu_TM()
    tm.show()
    sys.exit(app.exec_())