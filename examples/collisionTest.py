from olympus import BLACK, WHITE, RED, YELLOW, BLUE
from olympus import Screen, LEFT, RIGHT, UP, DOWN
from olympus import overlap, hits_any

screen = Screen(128, 128)

SIZE = 8
SPEED = 2
px, py = 16, 16

  # walls: (x, y, w, h) — border + a couple of obstacles
walls = [
      (0, 0, 128, 4),     # top
      (0, 124, 128, 4),   # bottom
      (0, 0, 4, 128),     # left
      (124, 0, 4, 128),   # right
      (40, 40, 48, 8),    # horizontal bar
      (60, 72, 8, 40),    # vertical bar
  ]

coins = [(100, 20, 6, 6), (20, 100, 6, 6), (100, 104, 6, 6)]
score = 0


def player_box(x, y):
    return (x, y, SIZE, SIZE)


def update():
      global px, py, score, coins

      # move on X, but cancel the move if it would put us inside a wall
      nx = px
      if screen.btn(LEFT):  nx -= SPEED
      if screen.btn(RIGHT): nx += SPEED
      if not hits_any(player_box(nx, py), walls):
          px = nx

      # move on Y separately (this is what lets you slide along walls)
      ny = py
      if screen.btn(UP):    ny -= SPEED
      if screen.btn(DOWN):  ny += SPEED
      if not hits_any(player_box(px, ny), walls):
          py = ny

      # pick up any coin we're touching
      keep = []
      for c in coins:
          if overlap(player_box(px, py), c):
              score += 1
          else:
              keep.append(c)
      coins = keep


def draw():
      screen.cls(BLACK)
      for (x, y, w, h) in walls:
          screen.rectfill(x, y, x + w - 1, y + h - 1, BLUE)
      for (x, y, w, h) in coins:
          screen.rectfill(x, y, x + w - 1, y + h - 1, YELLOW)
      screen.rectfill(px, py, px + SIZE - 1, py + SIZE - 1, RED)
      screen.text("COINS: " + str(score), 8, 8, WHITE)

screen.run(update, draw)