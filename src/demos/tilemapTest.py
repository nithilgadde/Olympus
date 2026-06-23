from palette import BLACK, WHITE, RED
from screen import Screen, LEFT, RIGHT, UP, DOWN
from tilemap import Tilemap, TILES, SOLID, TILE

  # the whole level, drawn as text. W = wall, C = coin, . = empty
LEVEL = [
      "WWWWWWWWWWWWWWWW",
      "W..............W",
      "W..WWW....C....W",
      "W.........WWW..W",
      "W..C...........W",
      "W......WW......W",
      "W......WW..C...W",
      "W..............W",
      "W...WWWW.......W",
      "W..........C...W",
      "W....C.........W",
      "W.......WWWW...W",
      "W..............W",
      "W..C.......C...W",
      "W..............W",
      "WWWWWWWWWWWWWWWW",
  ]

screen = Screen(128, 128)
level = Tilemap(list(LEVEL), TILES, SOLID)

SIZE = 8
SPEED = 1
px, py = 16, 16
score = 0


def update():
      global px, py, score

      nx = px
      if screen.btn(LEFT):  nx -= SPEED
      if screen.btn(RIGHT): nx += SPEED
      if not level.box_hits_solid(nx, py, SIZE, SIZE):
          px = nx

      ny = py
      if screen.btn(UP):    ny -= SPEED
      if screen.btn(DOWN):  ny += SPEED
      if not level.box_hits_solid(px, ny, SIZE, SIZE):
          py = ny

      # eat a coin if we're standing on one (check the tile under our center)
      col = (px + SIZE // 2) // TILE
      row = (py + SIZE // 2) // TILE
      if level.get(col, row) == 'C':
          level.set(col, row, '.')
          score += 1


def draw():
      screen.cls(BLACK)
      level.draw(screen)
      screen.rectfill(px, py, px + SIZE - 1, py + SIZE - 1, RED)
      screen.text("COINS: " + str(score), 8, 8, WHITE)

screen.run(update, draw)