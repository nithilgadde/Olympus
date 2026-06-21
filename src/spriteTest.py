import os
from palette import DARKBLUE
from screen import Screen, LEFT, RIGHT, UP, DOWN
from sprites import load_sprite

HERE = os.path.dirname(__file__)

screen = Screen(128, 128)
hero = load_sprite(os.path.join(HERE, "assets", "hero.png"))

px, py = 56, 56
facing_left = False


def update():
    global px, py, facing_left
    if screen.btn(LEFT):  px -= 2; facing_left = True
    if screen.btn(RIGHT): px += 2; facing_left = False
    if screen.btn(UP):    py -= 2
    if screen.btn(DOWN):  py += 2
    px = max(0, min(128 - 16, px))
    py = max(0, min(128 - 16, py))


def draw():
    screen.cls(DARKBLUE)
    screen.spr(hero, px, py, flip_x=facing_left)

screen.run(update, draw)