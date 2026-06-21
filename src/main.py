import os
from palette import DARKBLUE, YELLOW, WHITE, RED
from screen import Screen, LEFT, RIGHT, O
from sprites import load_sprite

HERE = os.path.dirname(__file__)

screen = Screen(128, 128)
score = 0
lx = 44

def update():
    global score, lx
    if screen.btn(O):
        score += 10
    if screen.btn(LEFT): lx -= 1
    if screen.btn(RIGHT): lx += 1


def draw():
    screen.cls(DARKBLUE)
    screen.text("OLYMPUS", 38, 18, YELLOW)
    screen.text("SCORE: " + str(score), 30, 44, WHITE)
    screen.text("PRESS Z", lx, 80, RED)

screen.run(update, draw)