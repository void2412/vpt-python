from gui import resetAuto
import autoUtils
from imgProcess import Point
import imgProcess
import time
import sys
import ctypes
from mem_edit import Process
from PyQt5.QtWidgets import *
from autoUtils import thread_with_trace

class resetAutoUI(QMainWindow, resetAuto.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('reset Auto')
        self.textBoxList = [self.lineEdit1,self.lineEdit2,self.lineEdit3,self.lineEdit4,self.lineEdit5]
        self.startBtnList = [self.startBtn1,self.startBtn2,self.startBtn3,self.startBtn4,self.startBtn5]
        self.checkboxList = [self.checkBox,self.checkBox_2,self.checkBox_3,self.checkBox_4,self.checkBox_5]
        self.startStateList = [False,False,False,False,False]

        for x in self.checkboxList:
            x.setEnabled(False)
        self.delayLine.setText('10000')
        self.threads = [None]*5
        self.autoTat = imgProcess.getImg('./img/resetAuto/autoTat.png')
        self.initBtn()

    def initBtn(self):
        index = 0
        for button in self.startBtnList:
            button.clicked.connect(lambda ch, index = index: self.start(index))
            index=index+1

    def start(self,index):
        if(self.startStateList[index] == False):
            self.startStateList[index] = True
            self.startBtnList[index].setText('stop')
            title = self.textBoxList[index].text()
            delay = int(self.delayLine.text()) * 0.001
            self.createThread(index,title,delay)
            self.threads[index].start()
        else:
            self.startStateList[index] = False
            self.startBtnList[index].setText('start')
            self.threads[index].kill()
            self.threads[index] = None
            self.checkboxList[index].setChecked(False)



    def createThread(self,index,title,delay):
        th = thread_with_trace(target=self.doWork,args=(index,title,delay,))
        th.setDaemon(True)
        self.threads[index] = th
        pass

    def doWork(self,index,title,delay):
        autoPoint = Point(1029,605)
        randomPoint = Point(388,654)
        hwnd = autoUtils.getHandle(title)
        autoUtils.ResizeWindow(hwnd)
        autoUtils.click(hwnd,randomPoint)
        time.sleep(0.3)
        screen = imgProcess.captureWindow(hwnd)
        point = imgProcess.findImgPointandFixCoord(self.autoTat,screen)
        if(point != Point(0, 0)):
            autoUtils.click(hwnd, autoPoint)
        else:
            autoUtils.click(hwnd, autoPoint)
            time.sleep(0.5)
            autoUtils.click(hwnd, autoPoint)
            time.sleep(0.3)
        pid = autoUtils.get_window_pid_by_title(title)
        with Process.open_process(pid) as p:

            autobat = True
            addrs = p.search_all_memory(ctypes.c_int(150))
            while len(addrs) > 1:
                autoUtils.click(hwnd, autoPoint)
                time.sleep(0.5)
                if(autobat==True):
                    autobat=False
                    filtered = p.search_addresses(addrs,ctypes.c_int(0))
                else:
                    autobat=True
                    filtered = p.search_addresses(addrs,ctypes.c_int(150))
                addrs.clear()
                addrs = filtered
                time.sleep(0.5)

            addr = addrs[0]
            autoUtils.click(hwnd,randomPoint)
            time.sleep(0.3)
            screen = imgProcess.captureWindow(hwnd)
            point = imgProcess.findImgPointandFixCoord(self.autoTat, screen)
            if (point != Point(0, 0)):
                autoUtils.click(hwnd, autoPoint)
                time.sleep(0.5)
            self.checkboxList[index].setChecked(True)
        self.resetWork(addr,pid,delay)



    def resetWork(self,address,pid,delay):
        with Process.open_process(pid) as p:
            while(True):
                num_cint = p.read_memory(address, ctypes.c_int())
                num = num_cint.value
                if (num != 150):
                    p.write_memory(address, ctypes.c_int(150))
                time.sleep(delay)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = resetAutoUI()
    win.show()
    sys.exit(app.exec_())