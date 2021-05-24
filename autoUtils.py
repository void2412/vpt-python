
import threading
import sys
import win32gui
import win32process
import win32con
import win32api


def changeWinTitle(hwnd,title):
    win32gui.SetWindowText(hwnd,title)

def closeWindow(hwnd):
    win32gui.PostMessage(hwnd,win32con.WM_CLOSE,0,0)

def getHandle(title):
    return win32gui.FindWindow(None, title)

def getWinPos(hwnd):
    return win32gui.GetWindowRect(hwnd)


def click(hwnd, point):
    lParam = win32api.MAKELONG(point.x,point.y)
    win32gui.PostMessage(hwnd,win32con.WM_LBUTTONDOWN,win32con.MK_LBUTTON,lParam)
    win32gui.PostMessage(hwnd,win32con.WM_LBUTTONUP,win32con.MK_LBUTTON,lParam)
    pass

def clickusingSend(hwnd, point):
    lParam = win32api.MAKELONG(point.x, point.y)
    win32gui.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
    win32gui.SendMessage(hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, lParam)

def get_window_pid_by_title(title):
    hwnd = getHandle(title)
    threadid,pid = win32process.GetWindowThreadProcessId(hwnd)
    return pid

def sendKey(hwnd,key):
    pass

def ResizeWindow(hwnd):
    (x, y, x1, y1) = win32gui.GetWindowRect(hwnd)
    w = 1066
    h = 724
    win32gui.MoveWindow(hwnd,x,y,w,h,True)

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