import pygame
from pygame.locals import *
import win32api
import win32con
import win32gui
from ctypes import windll
import requests
import pandas as pd
import time
import warnings
import random
warnings.filterwarnings("ignore")
import character

def move_transparent_window(x, y, fuchsia):

    SetWindowPos = windll.user32.SetWindowPos
    hwnd = pygame.display.get_wm_info()["window"]
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                           win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
    win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*fuchsia), 0, win32con.LWA_COLORKEY)
    SetWindowPos(hwnd, -1, x, y, 0, 0, 0x0001)


SIZE = (500, 500)
pygame.init()
pygame.display.set_caption("Game v0.0.1")
screen = pygame.display.set_mode(SIZE, pygame.NOFRAME)
fuchsia = (255, 250, 250)
move_transparent_window(1450, 550, fuchsia)
done = False
clock = pygame.time.Clock()
kalsit = character.Kalsit(screen, Rect(100, 100, 300, 300))


while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    screen.fill(fuchsia)  # Transparent background
    kalsit.refresh()
    pygame.display.update()
    clock.tick(30)