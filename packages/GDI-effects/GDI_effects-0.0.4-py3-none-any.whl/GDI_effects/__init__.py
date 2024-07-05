from random import *
import random
import win32con
import win32gui
import win32api
import ctypes
import time
import math
from win32con import *
from win32ui import *
from win32gui import *
from win32api import *
from win32file import *



def BWscreen():
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    [sw, sh] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)] 
    hdc = win32gui.GetDC(0)

    while True:

        win32gui.BitBlt(hdc, 0, 0, sw, sh, hdc, -3,-3, win32con.NOTSRCCOPY)

def errorscreen():    
    hdc = win32gui.GetDC(0)
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    [w, h] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]


    x = y = 0
    while True:
        win32gui.DrawIcon(hdc, x , y , win32gui.LoadIcon(None, win32con.IDI_ERROR))
        x = x + 30
        if x >= w:
            y = y + 30
            x = 0
        if y >= h:
            x = y = 0

def invertscreen():
    hdc = win32gui.GetDC(0)
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    [w, h] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)] 
    while True:
        win32gui.InvertRect(hdc, (0, 0, w ,h))


def panscreen(): 
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    [sw, sh] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)] 
    hdc = win32gui.GetDC(0)
    dx = dy = 1
    angle = 0
    size = 1
    speed = 5
    while True:

        win32gui.BitBlt(hdc, 0, 0, sw, sh, hdc, dx, dy, win32con.SRCCOPY)
        dx = math.ceil(math.sin(angle) * size * 10)
        dy = math.ceil(math.cos(angle) * size * 10)
        angle += speed / 10
        if angle > math.pi :
            angle = math.pi * -1
def Rainbowblink():
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    [sw, sh] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)] 
    while True:
        hdc = win32gui.GetDC(0)
        color = (random.randint(0, 122), random.randint(0, 430), random.randint(0, 310))
        brush = win32gui.CreateSolidBrush(win32api.RGB(*color))
        win32gui.SelectObject(hdc, brush)
        win32gui.BitBlt(hdc, random.randint(-3, 3), random.randint(-3, 3), sw, sh, hdc, 0, 0, win32con.SRCCOPY)
        win32gui.BitBlt(hdc, random.randint(-10, 10), random.randint(-10, 10), sw, sh, hdc, 0, 0, win32con.PATINVERT)

def screenwavy():
    desktop = win32gui.GetDesktopWindow()
    hdc = win32gui.GetWindowDC(desktop)
    sw = win32api.GetSystemMetrics(0)
    sh = win32api.GetSystemMetrics(1)
    angle = 0

    while True:
        hdc = win32gui.GetWindowDC(desktop)
        for i in range(int(sw + sh)):
            a = int(math.sin(angle) * 20)
            win32gui.BitBlt(hdc, 0, i, sw, 1, hdc, a, i, win32con.SRCCOPY)
            angle += math.pi / 50
        win32gui.ReleaseDC(desktop, hdc)
        time.sleep(0.01)
def voidscreen():
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    [sw, sh] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)] 
    hdc = win32gui.GetDC(0)
    dx = dy = 1
    angle = 0
    size = 1
    speed = 5
    while True:

        win32gui.BitBlt(hdc, 0, 0, sw, sh, hdc, dx,dy, win32con.SRCAND)
        dx = math.ceil(math.sin(angle) * size * 10)
        dy = math.ceil(math.cos(angle) * size * 10)
        angle += speed / 10
        if angle > math.pi :
            angle = math.pi * -1

def glitchscreen():
    desk = GetDC(0)
    x,y = (GetSystemMetrics(0), GetSystemMetrics(1))
    while True:
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        brush = win32gui.CreateSolidBrush(win32api.RGB(*color))
        SelectObject(desk, brush)
        PatBlt(desk, random.randrange(x), random.randrange(y), random.randrange(x), random.randrange(y), PATINVERT)
        DeleteObject(brush)
        time.sleep(0.02)
