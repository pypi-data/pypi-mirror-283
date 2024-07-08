from win32file import *
from win32con import *
from win32api import *
from win32gui import *
from win32ui import *
from random import *
import win32con
import win32gui
import win32api
import random
import ctypes
import time
import math

class GDI:
    def BW_screen():
        """
        Creates a black and white effect on the screen.
        """
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        [sw, sh] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)] 
        hdc = win32gui.GetDC(0)

        while True:

            win32gui.BitBlt(hdc, 0, 0, sw, sh, hdc, -5,-5, win32con.NOTSRCCOPY)

    def error_screen():    
        """
        Displays error icons at various positions on the screen.
        """
        hdc = win32gui.GetDC(0)
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        [w, h] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]


        x = y = 0
        while True:
            win32gui.DrawIcon(hdc, x , y , win32gui.LoadIcon(None, win32con.IDI_ERROR))
            x = x +  random.randint(30, 100)
            if x >= w:
                y = y + random.randint(30, 100)
                x = 0
            if y >= h:
                x = y = 0

    def invert_screen():
        """
        Inverts the colors on the screen.
        """
        hdc = win32gui.GetDC(0)
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        [w, h] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)] 
        while True:
            win32gui.InvertRect(hdc, (0, 0, w ,h))
            time.sleep(0.5)


    def pan_screen(): 
        """
        Pans the screen in random directions.
        """
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
    def Rainbow_blink():
        """
        Creates random rainbow effects on the screen.
        """
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        [sw, sh] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)] 
        while True:
            hdc = win32gui.GetDC(0)
            color = (random.randint(0, 122), random.randint(0, 430), random.randint(0, 310))
            brush = win32gui.CreateSolidBrush(win32api.RGB(*color))
            win32gui.SelectObject(hdc, brush)
            win32gui.BitBlt(hdc, random.randint(-8, 8), random.randint(-8, 8), sw, sh, hdc, 0, 0, win32con.SRCCOPY)
            win32gui.BitBlt(hdc, random.randint(-10, 10), random.randint(-10, 10), sw, sh, hdc, 0, 0, win32con.PATINVERT)

    def screen_wavy():
        """
        Creates a wavy effect on the screen.
        """
        desktop = win32gui.GetDesktopWindow()
        hdc = win32gui.GetWindowDC(desktop)
        sw = win32api.GetSystemMetrics(0)
        sh = win32api.GetSystemMetrics(1)
        angle = 0

        while True:
            hdc = win32gui.GetWindowDC(desktop)
            for i in range(int(sw + sh)):
                a = int(math.sin(angle) * 30)
                win32gui.BitBlt(hdc, 0, i, sw, 1, hdc, a, i, win32con.SRCCOPY)
                angle += math.pi / 30
                print(angle)
            win32gui.ReleaseDC(desktop, hdc)
            time.sleep(0.01)
    def void_screen():
        """
        Creates a void effect on the screen.
        """
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

    def glitch_screen():
        """
        Creates a glitch effect on the screen.
        """
        desk = GetDC(0)
        x,y = (GetSystemMetrics(0), GetSystemMetrics(1))
        while True:
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            brush = win32gui.CreateSolidBrush(win32api.RGB(*color))
            SelectObject(desk, brush)
            PatBlt(desk, random.randrange(x), random.randrange(y), random.randrange(x), random.randrange(y), PATINVERT)
            DeleteObject(brush)
            time.sleep(0.02)

    def warning_screen():    
        """
        Displays a warning icon randomly on the screen.
        """
        hdc = win32gui.GetDC(0)
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        [w, h] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]


        x = y = 0
        while True:
            win32gui.DrawIcon(hdc, x , y , win32gui.LoadIcon(None, win32con.IDI_WARNING))
            x = x +  random.randint(30, 100)
            if x >= w:
                y = y + random.randint(30, 100)
                x = 0
            if y >= h:
                x = y = 0

    def question_screen():    
        """
        Displays a question icon randomly on the screen.
        """
        hdc = win32gui.GetDC(0)
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        [w, h] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]


        x = y = 0
        while True:
            win32gui.DrawIcon(hdc, x , y , win32gui.LoadIcon(None, win32con.IDI_QUESTION))
            x = x +  random.randint(30, 100)
            if x >= w:
                y = y + random.randint(30, 100)
                x = 0
            if y >= h:
                x = y = 0

    def asterisk_screen():    
        """
        Displays an asterisk icon randomly on the screen.
        """
        hdc = win32gui.GetDC(0)
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        [w, h] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]


        x = y = 0
        while True:
            win32gui.DrawIcon(hdc, x , y , win32gui.LoadIcon(None, win32con.IDI_ASTERISK))
            x = x +  random.randint(30, 100)
            if x >= w:
                y = y + random.randint(30, 100)
                x = 0
            if y >= h:
                x = y = 0

    def super_icon_screen():   
        """
        displays various system icons randomly on the screen. 
        """
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        [w, h] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]

        hdc = win32gui.GetDC(0)

        icon_ids = [
            win32con.IDI_APPLICATION,
            win32con.IDI_ASTERISK,
            win32con.IDI_ERROR,
            win32con.IDI_EXCLAMATION,
            win32con.IDI_HAND,
            win32con.IDI_INFORMATION,
            win32con.IDI_QUESTION,
            win32con.IDI_WARNING,
            win32con.IDI_WINLOGO
        ]

        x = y = 0
        while True:
            icon_id = random.choice(icon_ids)
            icon = win32gui.LoadIcon(None, icon_id)
            win32gui.DrawIcon(hdc, x, y, icon)

            x = x + random.randint(30, 100)
            if x >= w:
                y = y + random.randint(30, 100)
                x = 0
            if y >= h:
                x = y = 0

    def copy_screen():
        """
        Continuously copies the entire screen area and displays it without any offset.
        """
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        [sw, sh] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)] 
        hdc = win32gui.GetDC(0)

        while True:

            win32gui.BitBlt(hdc, 0, 0, sw, sh, hdc, -5,-5, win32con.SRCCOPY)

    def tunnel_screen():
        """
        Creates a tunnel effect by continuously stretching and copying the screen content inwards from the edges.
        """
        sw,sh = (GetSystemMetrics(0), GetSystemMetrics(1))
        HDC = GetDC(0)
        while True:
            StretchBlt(HDC, 50, 50, sw - 100, sh - 100, HDC, 0, 0, sw, sh, SRCCOPY)
            time.sleep(0.1)

    def twisted_screen():
        """
        Apply a twisted screen effect by performing bitwise operations on the screen content.
        """
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        [sw, sh] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)] 
        hdc = win32gui.GetDC(0)


        NOTSRCCOPY = 0x00330008
        SRCAND = 0x008800C6

        dx1, dy1 = -3, -3
        dx2, dy2 = 1, 1
        angle = 0
        size = 1
        speed = 5

        try:
            while True:
                win32gui.BitBlt(hdc, 0, 0, sw, sh, hdc, dx1, dy1, NOTSRCCOPY)  
                win32gui.BitBlt(hdc, 0, 0, sw, sh, hdc, dx2, dy2, SRCAND)      

                dx1 = math.ceil(math.sin(angle) * size * 10)
                dy1 = math.ceil(math.cos(angle) * size * 10)
                dx2 = math.ceil(math.sin(angle) * size * -10)
                dy2 = math.ceil(math.cos(angle) * size * -10)
                angle += speed / 10.0

                if angle > math.pi:
                    angle = math.pi * -1

                time.sleep(0.01)  

        finally:
            win32gui.ReleaseDC(0, hdc)


















































































































































































































































































































































































































































































































































































































































































































































        
class Meme:
    """
    Secret
    """
    def easter_eggs():
        import webbrowser
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        webbrowser.open(url)