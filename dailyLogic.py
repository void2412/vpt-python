import asyncio
import ctypes
import json
import sys
import threading
import time
import PyQt5
import autoit
import win32gui
from PyQt5.QtWidgets import *
import autoDaily
import startvpt
from gui import daily
import multiprocessing


parse_account = json.load(open('./account.json', 'r'))

tinhcunglock = threading.Lock()


class thread_with_trace(threading.Thread):
    def __init__(self, *args, **keywords):
        threading.Thread.__init__(self, *args, **keywords)
        self.killed = False

    def start(self):
        self.__run_backup = self.run
        self.run = self.__run
        threading.Thread.start(self)

    def __run(self):
        sys.settrace(self.globaltrace)
        self.__run_backup()
        self.run = self.__run_backup

    def globaltrace(self, frame, event, arg):
        if event == 'call':
            return self.localtrace
        else:
            return None

    def localtrace(self, frame, event, arg):
        if self.killed:
            if event == 'line':
                raise SystemExit()
        return self.localtrace

    def kill(self):
        self.killed = True


def click(hwnd, x, y):
    autoit.control_click_by_handle(hwnd, hwnd, x=x, y=y)


def sendKey(hwnd, key):
    autoit.control_send_by_handle(hwnd, hwnd, key)


nguyenlieu = [
    'Kim Loại',
    'Gỗ',
    'Ngọc',
    'Vải',
    'Lông Thú',
    'Kim Loại Hiếm',
    'Gỗ Tốt',
    'Pha Lê',
    'Gấm Vóc',
    'Da Thú'
]
kenh = [
    'default 5',
    '1',
    '2',
    '3',
    '4',
    '5',
    '6',
    '7',
    '8'
]
loaitinhcung = [
    'Default Sư tử',
    'Bạch Dương',
    'Kim Ngưu',
    'Song Tử',
    'Cự Giải',
    'Sư Tử',
    'Xử Nữ',
    'Thiên Bình',
    'Hổ Cáp',
    'Nhân Mã',
    'Ma Kết',
    'Bảo Bình',
    'Song Ngư'
]
leveltinhcung = [
    'default 12',
    '1',
    '2',
    '3',
    '4',
    '5',
    '6',
    '7',
    '8',
    '9',
    '10',
    '11',
    '12'
]

charloc = [
    '1',
    '2',
    '3'
]


class dailyMenu(QMainWindow, daily.Ui_MainWindow):
    def __init__(self):
        super(dailyMenu, self).__init__()
        self.setupUi(self)
        self.link = None
        self.title = None
        self.server = None
        self.svIndex = 0
        self.accIndex = 0
        self.populateData()
        self.th = None
        self.res = None
        self.nguyenlieubox.addItems(nguyenlieu)
        self.kenhBox.addItems(kenh)
        self.leveltinhcungbox.addItems(leveltinhcung)
        self.nguyenlieu = 0
        self.kenh = 5
        self.charloc = 1
        self.leveltinhcung = 12
        self.loaitinhcung = 5
        self.charlocBox.addItems(charloc)
        self.loaitinhcungbox.addItems(loaitinhcung)
        self.nhanvipbox.setChecked(True)
        self.trangvienbox.setChecked(True)
        self.tinhcungbox.setChecked(True)
        self.hanhlangbox.setChecked(True)
        self.pbbox.setChecked(True)
        self.thantubox.setChecked(True)
        self.tuhanhbox.setChecked(True)
        self.hwnd = 0

    def setup(self):
        self.startBtn.clicked.connect(self.startbtnClicked)
        self.svCombo.activated.connect(self.getsvIndex)
        self.accCombo.activated.connect(self.getaccIndex)
        self.kenhBox.activated.connect(self.getkenhIndex)
        self.charlocBox.activated.connect(self.getcharLocation)
        self.nguyenlieubox.activated.connect(self.getnguyenlieuIndex)
        self.leveltinhcungbox.activated.connect(self.getlvtinhcungIndex)
        self.loaitinhcungbox.activated.connect(self.getloaitinhcungIndex)
        self.stopBtn.clicked.connect(self.stopBtnClicked)

    def stopBtnClicked(self):
        self.th.kill()
        self.th.join()
        if not self.th.isAlive():
            self.statusTextBox.append('Auto Stopped! Thread killed!')
            self.th = thread_with_trace()

    def getsvIndex(self, index):
        self.svIndex = index

    def getaccIndex(self, index):
        self.accIndex = index

    def getkenhIndex(self, index):
        if index != 0:
            self.kenh = index

    def getcharLocation(self, index):
        self.charloc = index + 1

    def getnguyenlieuIndex(self, index):
        self.nguyenlieu = index

    def getlvtinhcungIndex(self, index):
        if index != 0:
            self.leveltinhcung = index

    def getloaitinhcungIndex(self, index):
        if index != 0:
            self.loaitinhcung = index

    def do_tasks(self, title, link, sv):
        self.th = thread_with_trace(target=self.auto_thread, args=(title, link, sv))
        self.th.start()

    def auto_thread(self, title, link, sv):
        ch = win32gui.FindWindow(None, title)
        if self.logacc_checkBox.isChecked():
            if ch != 0:
                autoit.win_close_by_handle(ch)

            self.statusTextBox.append('bắt đầu log in')
            self.hwnd = startvpt.startGame(title, link, sv)
            self.res = startvpt.fullLogin(self.hwnd, self.kenh, self.charloc)
            self.statusTextBox.append(self.res)
            self.res = None
            time.sleep(15)
            click(self.hwnd, 774, 156)
            time.sleep(2)
            click(self.hwnd, 236, 521)
            time.sleep(2)
        else:
            self.hwnd = ch
        self.statusTextBox.append('bắt đầu chỉnh thiết lập')
        self.res = autoDaily.setupthietlap(self.hwnd)
        self.statusTextBox.append(self.res)
        self.res = None
        time.sleep(2)
        self.statusTextBox.append('bắt đầu sửa đồ')
        self.res = autoDaily.fixdo(self.hwnd)
        self.statusTextBox.append(self.res)
        self.res = None
        if self.nhanvipbox.isChecked():
            time.sleep(2)
            self.statusTextBox.append('bắt đầu nhận vip')
            self.res = autoDaily.nhanvip(self.hwnd)
            self.statusTextBox.append(self.res)
            self.res = None
        if self.trangvienbox.isChecked():
            time.sleep(2)
            self.statusTextBox.append('bắt đầu trồng trang viên')
            self.res = autoDaily.trongtrangvien(self.hwnd, self.nguyenlieu)
            self.statusTextBox.append(self.res)
            self.res = None
        if self.hanhlangbox.isChecked():
            time.sleep(2)
            self.statusTextBox.append('bắt đầu nhận hành lang')
            self.res = autoDaily.nhanhanhlang(self.hwnd, 90)
            self.statusTextBox.append(self.res)
            self.res = None
        if self.pbbox.isChecked():
            time.sleep(2)
            self.statusTextBox.append('bắt đầu auto pb')
            self.res = autoDaily.autopb(self.hwnd, 90)
            self.statusTextBox.append(self.res)
            self.res = None
        time.sleep(1)
        if self.tinhcungbox.isChecked():
            time.sleep(2)
            self.statusTextBox.append('bắt đầu auto tinh cung')
            self.statusTextBox.append('waiting for trigger setup tinh cung')
            tinhcunglock.acquire()
            self.statusTextBox.append('setup tinh cung triggered')
            self.res = autoDaily.tinhcungsetup(self.hwnd, self.leveltinhcung, self.loaitinhcung)
            tinhcunglock.release()
            if self.res != 'tc setup finished':
                self.res = 'loi setup tinh cung'
                self.statusTextBox.append(self.res)
            else:
                self.triggertinhcungfinish = True
                self.res = autoDaily.finishingautotinhcung(self.hwnd)
                self.statusTextBox.append(self.res)
                self.res = None

        if self.thantubox.isChecked():
            time.sleep(2)
            self.statusTextBox.append('bắt đầu auto tt')
            self.res = autoDaily.autothantu(self.hwnd, 90)
            self.statusTextBox.append(self.res)
            self.res = None
        if self.tuhanhbox.isChecked():
            time.sleep(2)
            self.statusTextBox.append('bắt đầu auto tu hành')
            self.res = autoDaily.autotuhanh(self.hwnd, 90)
            self.statusTextBox.append(self.res)
            self.res = None
        time.sleep(2)
        self.statusTextBox.append('bắt đầu bug onl')
        self.res = autoDaily.bugonl(self.hwnd, self.charloc)
        self.statusTextBox.append(self.res)
        self.res = None

        time.sleep(1)
        self.statusTextBox.append('Auto Finished')

    def startbtnClicked(self):
        self.title = parse_account[self.accIndex]['title']
        link = parse_account[self.accIndex]['link']
        self.link = link.replace('&isExpand=true', '')
        self.server = parsed_server[self.svIndex]['server']
        winTitle = 'auto daily - ' + str(self.title)
        self.setWindowTitle(winTitle)
        self.do_tasks(self.title, self.link, self.server)

    def populateData(self):
        for item in range(len(parsed_server)):
            self.svCombo.addItem(parsed_server[item]['server'])
        for item in range(len(parse_account)):
            self.accCombo.addItem(parse_account[item]['title'])
