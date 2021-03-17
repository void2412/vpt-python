import autoit
import threading
import sys
import win32gui
import win32process
def click(hwnd, point):
    autoit.control_click_by_handle(hwnd,hwnd,x=point.x,y=point.y)
    pass

def get_window_pid_by_title(title):
    hwnd = autoit.win_get_handle(title)
    threadid,pid = win32process.GetWindowThreadProcessId(hwnd)
    return pid

def sendKey(hwnd,key):
    autoit.control_send_by_handle(hwnd,hwnd,key)

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