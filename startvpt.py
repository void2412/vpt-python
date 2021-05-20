import subprocess
import autoUtils
import time
from imgProcess import *
from autoUtils import *
import os
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
            time.sleep(0.5)
    autoUtils.changeWinTitle(hwnd,title)


class autoLogin:
    def __init__(self):
        self.batbuoc = getImg('./img/login/batbuoc.png')
        self.lienket = getImg('./img/login/lienketquahan.png')
        self.nhanvat = getImg('./img/login/checkNhanVat.png')
        self.serveroff = getImg('./img/ok.png')
        self.inGame = getImg('./img/login/inGame.png')
        self.thread = None
        self.kenhdaugiaRect = rect(Point(452,501),Point(613,518))

