import subprocess
import autoUtils
import time
from imgProcess import *
from autoUtils import *
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'./Tesseract-OCR/tesseract.exe'
def startGame(title,link):

    subprocess.Popen('flashplayer.exe '+link)
    time.sleep(0.5)
    hwnd = autoUtils.getHandle('Adobe Flash Player 10')
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

