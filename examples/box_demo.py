import ctypes, sdl2
import numpy as np
import math
from olympus import BLACK, RED, YELLOW, GREEN, WHITE
from olympus import Screen, LEFT, RIGHT, UP, DOWN, O, X

screen = Screen(128, 128)

px, py = 60, 60
color = RED

def update():
    global px, py, color
    if screen.btn(LEFT): px -= 2
    if screen.btn(RIGHT): px += 2
    if screen.btn(UP): py -= 2
    if screen.btn(DOWN): py += 2

    px = max(0, min(128 - 8, px))
    py = max(0, min(128 - 8, py))

    if screen.btnp(O): color = YELLOW
    if screen.btnp(X): color = GREEN

def draw():
    screen.cls(BLACK)
    screen.rectfill(px, py, px + 7, py + 7, color)
    screen.rect(px, py, px + 7, py + 7, WHITE)

screen.run(update, draw)