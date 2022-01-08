import subprocess
import autoUtils
from time import sleep
from imgProcess import *
from autoUtils import *
import datetime
import pytz
import win32con
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'./Tesseract-OCR/tesseract.exe'
def startGame(title,link):

    subprocess.Popen("flashplayer.exe "+link,shell=False,creationflags= subprocess.DETACHED_PROCESS)
    hwnd = 0
    for i in range(20):
        hwnd = autoUtils.getHandle('Adobe Flash Player 10')
        if(hwnd != 0):
            break
        else:
            sleep(0.5)
    autoUtils.changeWinTitle(hwnd,title)


def startGameAuto(title,link, charLoc, kenh):
    hwnd = autoUtils.getHandle(title)
    if hwnd != 0:   
        autoUtils.closeWindow(hwnd)
    startGame(title, link)
    hwnd = autoUtils.getHandle(title)
    auto = autoLogin(hwnd,charLoc,kenh)
    auto.start()

def getStringOCR(img):
    stringOCR = pytesseract.image_to_string(img, lang='vie', config='--psm 6')
    stringOCR = stringOCR.strip()
    return stringOCR

def getKenhLoc(kenh):
    x = 528
    y=0
    if kenh == 1:
        y = 236
    if kenh == 2:
        y=270
    if kenh == 3:
        y=305
    if kenh == 4:
        y=339
    if kenh == 5:
        y=372
    if kenh == 6:
        y=408
    if kenh == 7:
        y=441
    if kenh == 8:
        y= 476
    return (x,y)

def getCharLoc(charLoc):
    y = 468
    x = 0
    if charLoc == 1:
        x = 370
    if charLoc == 2:
        x = 500
    if charLoc == 3:
        x = 637
    return (x,y)

class autoLogin:
    #login vo game after open flash
    def __init__(self, hwnd, charLoc, kenh):
        self.batbuoc = getImg('./img/login/batbuoc.png')
        self.lienket = getImg('./img/login/lienketquahan.png')
        self.nhanvat = getImg('./img/login/checkNhanVat.png')
        self.serveroff = getImg('./img/ok.png')
        self.inGame = getImg('./img/login/inGame.png')
        self.vaoGame = getImg('./img/login/finalCheck.png')
        self.hwnd = hwnd
        self.kenh = kenh
        self.charLoc = charLoc
        self.kenhdaugiaRect = rect((441,470),(606,486))
        self.bbLoc = (527,554)

    def batbuocProc(self,hwnd):
        screen = captureWindow(hwnd)
        bb = findImgPoint(self.batbuoc,screen)
        if bb != (0,0):
            click(hwnd,self.bbLoc)
            sleep(0.5)
            return True
        else:
            return False

    def chonKenh(self,hwnd,kenh):
        screen = captureWindow(hwnd)
        cropdaugia = cropImg(screen,self.kenhdaugiaRect)
        stringOCR = getStringOCR(cropdaugia)
        if stringOCR.find('Kênh') == 0:
            click(hwnd,getKenhLoc(kenh))
            sleep(0.5)
            return True
        else:
            return False

    def checkKenh(self,hwnd):
        screen = captureWindow(hwnd)
        cropdaugia = cropImg(screen, self.kenhdaugiaRect)
        stringOCR = getStringOCR(cropdaugia)
        if stringOCR.find('Kênh') == 0:
            return True
        else:
            return False

    def chonNhanVat(self,hwnd,charLoc):
        screen = captureWindow(hwnd)
        nhanvat = findImgPoint(self.nhanvat,screen)
        if nhanvat != (0,0):
            click(hwnd,getCharLoc(charLoc))
            sleep(0.5)
            click(hwnd,(392,551))
            return True
        else:
            return False


    def vaoGameProc(self,hwnd):
        screen = captureWindow(hwnd)
        vaoGame = findImgPoint(self.vaoGame,screen)
        if vaoGame != (0,0):
            sendKey(hwnd,win32con.VK_ESCAPE)
            sleep(0.5)
            return True
        else:
            return False

    def checkLagAndInvalidLink(self,hwnd):
        screen = captureWindow(hwnd)
        check1 = findImgPoint(self.lienket,screen)
        check2 = findImgPoint(self.serveroff,screen)
        if check1 != (0,0) or check2 != (0,0):
            if check1 != (0,0):
                click(hwnd,check1)
                sleep(0.5)
                return True
            if check2 != (0,0):
                click(hwnd,check2)
                sleep(0.5)
                return True
        else:
            return False

    def checkBaoTri(self):
        currenttime = datetime.datetime.now(pytz.timezone('Asia/Ho_Chi_Minh'))
        time = currenttime.time()
        weekday = currenttime.isoweekday()+1
        if weekday == 5 and time.hour in range(8,12):
            if time.hour == 11 and time.minute >15:
                return False
            else:
                return True
        else:
            return False



    def start(self):    #return -1 if maintanace, 0 if failed (link invalid,etc), hwnd if success
        if self.hwnd != 0:
            baotri = self.checkBaoTri()
            if baotri is False:
                sleep(0.5)
                for i in range(12):
                    bb = self.batbuocProc(self.hwnd)
                    if bb is True:
                        sleep(10)
                        checklag = self.checkLagAndInvalidLink(self.hwnd)
                        checkKenh = self.checkKenh(self.hwnd)
                        if checkKenh is False:
                            sleep(20)
                            if checklag is True:
                                for i in range(4):
                                    bb = self.batbuocProc(self.hwnd)
                                    sleep(30)
                                    checklag = self.checkLagAndInvalidLink(self.hwnd)
                                    if checklag is False:
                                        break
                                return 0
                        sleep(5)
                        for i in range(12):
                            chonKenh = self.chonKenh(self.hwnd,self.kenh)
                            if chonKenh is True:
                                sleep(5)
                                chonnv = self.chonNhanVat(self.hwnd,self.charLoc)
                                if chonnv is True:
                                    sleep(5)
                                    inGame = self.vaoGameProc(self.hwnd)
                                    if inGame is True:
                                        sleep(5)
                                        inGame = self.vaoGameProc(self.hwnd)
                                    while inGame is False:
                                        sleep(5)
                                        inGame = self.vaoGameProc(self.hwnd)
                                    return self.hwnd
                            else: #else chon kenh
                                sleep(5)
                    else:
                        sleep(5)
            else:
                return -1
        else:
            return 0