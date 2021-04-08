import subprocess
import autoUtils
import time
def startGame(title,link):

    subprocess.Popen('flashplayer.exe '+link)
    time.sleep(0.5)
    hwnd = autoUtils.getHandle('Adobe Flash Player 10')
    autoUtils.changeWinTitle(hwnd,title)

