from palette import DARKBLUE
from screen import Screen, LEFT, RIGHT, UP, DOWN
from sprites import FISH

screen = Screen(128, 128)
px, py = 60, 60
facing_left = False


def update():
    global px, py, facing_left
    if screen.btn(LEFT):  px -= 2; facing_left = True
    if screen.btn(RIGHT): px += 2; facing_left = False
    if screen.btn(UP):    py -= 2
    if screen.btn(DOWN):  py += 2
    px = max(0, min(128 - 8, px))
    py = max(0, min(128 - 8, py))


def draw():
    screen.cls(DARKBLUE)
    screen.spr(FISH, px, py, flip_x=facing_left)

screen.run(update, draw)