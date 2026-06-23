from olympus import DARKBLUE
from olympus import Screen, LEFT, RIGHT, UP, DOWN
from olympus import make_sprite
from olympus import Anim

HERO_WALK = [
      make_sprite([
          "..bbbb..",
          ".bbbbbb.",
          ".b7bb7b.",
          ".bbbbbb.",
          ".bbbbbb.",
          "..bbbb..",
          "..bb.b..",
          ".3...3..",
      ]),
      make_sprite([
          "..bbbb..",
          ".bbbbbb.",
          ".b7bb7b.",
          ".bbbbbb.",
          ".bbbbbb.",
          "..bbbb..",
          "..b.bb..",
          "..3...3.",
      ]),
  ]

HERO_IDLE = make_sprite([
      "..bbbb..",
      ".bbbbbb.",
      ".b7bb7b.",
      ".bbbbbb.",
      ".bbbbbb.",
      "..bbbb..",
      "..b..b..",
      "..3..3..",
  ])


screen = Screen(128, 128)
px, py = 60, 60
facing_left = False
moving = False
walk = Anim(HERO_WALK, speed=6)




def update():
      global px, py, facing_left, moving
      moving = False
      if screen.btn(LEFT):  px -= 1; facing_left = True;  moving = True
      if screen.btn(RIGHT): px += 1; facing_left = False; moving = True
      if screen.btn(UP):    py -= 1; moving = True
      if screen.btn(DOWN):  py += 1; moving = True

      px = max(0, min(128 - 8, px))
      py = max(0, min(128 - 8, py))

      if moving:
          walk.update()    # cycle the legs while walking
      else:
          walk.reset()     # stand still on the first frame


def draw():
      screen.cls(DARKBLUE)
      sprite = walk.frame() if moving else HERO_IDLE
      screen.spr(sprite, px, py, flip_x=facing_left)

screen.run(update, draw)