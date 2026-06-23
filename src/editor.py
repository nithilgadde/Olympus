import ctypes 
import sdl2
import numpy as np
from screen import Screen

VW = VH = 128
SCALE = 5
GRID = 16
CANVAS = 96
CELL = CANVAS // GRID
CANVAS_X = CANVAS_Y = 4
PAL_X, PAL_Y, SW = 4, 104, 7
PV_X, PV_Y = 104, 4
TRANSPARENT = 255
SAVE_FILE = "sprite.sav"

grid = np.full((GRID, GRID), TRANSPARENT, dtype=np.uint8)
selected = 8
undo_stack = []
onion = None
show_onion = True

def in_canvas(mx, my):
    return (CANVAS_X <= mx < CANVAS_X + GRID * CELL and CANVAS_Y <= my < CANVAS_Y + GRID * CELL)

def canvas_cell(mx, my):
    return (my - CANVAS_Y) // CELL, (mx - CANVAS_X) // CELL

def palette_index(mx, my):
    if PAL_Y <= my < PAL_Y + SW and mx >= PAL_X:
        i = (mx - PAL_X) // SW
        if 0 <= i < 16:
            return i
    return None

def grid_rows():
    out = []
    for r in range(GRID):
        line = "".join("." if grid[r, c] == TRANSPARENT else format(grid[r, c], "x") for c in range(GRID))
        out.append(line)
    return out

def to_code():
    body = "\n".join('    "%s",' % row for row in grid_rows())
    return "make_sprite([\n" + body + "\n])"

def push_undo():
      undo_stack.append(grid.copy())
      if len(undo_stack) > 50:
          undo_stack.pop(0)


def save_grid():
      with open(SAVE_FILE, "w") as f:
          f.write("\n".join(grid_rows()) + "\n")


def load_grid():
      try:
          with open(SAVE_FILE) as f:
              lines = [ln.rstrip("\n") for ln in f if ln.strip()]
      except FileNotFoundError:
          return
      push_undo()
      grid[:, :] = TRANSPARENT
      for r in range(min(GRID, len(lines))):
          for c in range(min(GRID, len(lines[r]))):
              ch = lines[r][c]
              grid[r, c] = TRANSPARENT if ch == "." else int(ch, 16)


def draw(screen):
      screen.cls(1)   # dark-blue background = grid lines
      # canvas
      for r in range(GRID):
          for c in range(GRID):
              x = CANVAS_X + c * CELL
              y = CANVAS_Y + r * CELL
              v = grid[r, c]
              if v != TRANSPARENT:
                  col = v
              elif show_onion and onion is not None and onion[r, c] != TRANSPARENT:
                  col = 2          # ghost of the onion frame (dark purple)
              else:
                  col = 6 if (r + c) % 2 == 0 else 5   # empty = checkerboard
              screen.rectfill(x, y, x + CELL - 2, y + CELL - 2, col)
      # palette strip
      for i in range(16):
          x = PAL_X + i * SW
          screen.rectfill(x, PAL_Y, x + SW - 2, PAL_Y + SW - 2, i)
      sx = PAL_X + selected * SW
      screen.rect(sx - 1, PAL_Y - 1, sx + SW - 1, PAL_Y + SW - 1, 7)
      # 1x live preview (actual size)
      for r in range(GRID):
          for c in range(GRID):
              if grid[r, c] != TRANSPARENT:
                  screen.pset(PV_X + c, PV_Y + r, grid[r, c])
      screen.rect(PV_X - 1, PV_Y - 1, PV_X + GRID, PV_Y + GRID, 6)
      screen.text("C:" + str(selected), 104, 26, 7)
      screen.text("ON" if show_onion else "OFF", 104, 34, 7)
      # help
      screen.text("E:CODE S:SAVE L:LOAD", 4, 114, 7)
      screen.text("Z:UNDO C:CLR O/H:ONION", 4, 120, 7)


def main():
      global selected, onion, show_onion
      sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO)
      window = sdl2.SDL_CreateWindow(
          b"Olympus Sprite Editor",
          sdl2.SDL_WINDOWPOS_CENTERED, sdl2.SDL_WINDOWPOS_CENTERED,
          VW * SCALE, VH * SCALE, sdl2.SDL_WINDOW_SHOWN)
      renderer = sdl2.SDL_CreateRenderer(window, -1, sdl2.SDL_RENDERER_ACCELERATED)
      sdl2.SDL_SetHint(sdl2.SDL_HINT_RENDER_SCALE_QUALITY, b"0")
      texture = sdl2.SDL_CreateTexture(
          renderer, sdl2.SDL_PIXELFORMAT_RGB24,
          sdl2.SDL_TEXTUREACCESS_STREAMING, VW, VH)

      screen = Screen(VW, VH)
      event = sdl2.SDL_Event()
      mxp, myp = ctypes.c_int(0), ctypes.c_int(0)
      prev_held = False
      running = True

      while running:
          while sdl2.SDL_PollEvent(ctypes.byref(event)):
              if event.type == sdl2.SDL_QUIT:
                  running = False
              elif event.type == sdl2.SDL_KEYDOWN:
                  k = event.key.keysym.sym
                  if k == sdl2.SDLK_ESCAPE:
                      running = False
                  elif k == sdl2.SDLK_c:
                      push_undo(); grid[:, :] = TRANSPARENT
                  elif k == sdl2.SDLK_e:
                      code = to_code()
                      print("\n" + code + "\n")
                      with open("sprite_out.txt", "w") as f:
                          f.write(code + "\n")
                  elif k == sdl2.SDLK_s:
                      save_grid()
                  elif k == sdl2.SDLK_l:
                      load_grid()
                  elif k == sdl2.SDLK_z:
                      if undo_stack:
                          grid[:, :] = undo_stack.pop()
                  elif k == sdl2.SDLK_o:
                      onion = grid.copy(); show_onion = True
                  elif k == sdl2.SDLK_h:
                      show_onion = not show_onion

          buttons = sdl2.SDL_GetMouseState(ctypes.byref(mxp), ctypes.byref(myp))
          mx, my = mxp.value // SCALE, myp.value // SCALE
          left = buttons & sdl2.SDL_BUTTON_LMASK
          right = buttons & sdl2.SDL_BUTTON_RMASK
          held = bool(left or right)

          # snapshot once at the start of each stroke that begins on the canvas
          if held and not prev_held and in_canvas(mx, my):
              push_undo()
          prev_held = held

          if left:
              if in_canvas(mx, my):
                  r, c = canvas_cell(mx, my)
                  grid[r, c] = selected
              else:
                  pi = palette_index(mx, my)
                  if pi is not None:
                      selected = pi
          if right and in_canvas(mx, my):
              r, c = canvas_cell(mx, my)
              grid[r, c] = TRANSPARENT

          draw(screen)
          rgb = screen.to_rgb()
          sdl2.SDL_UpdateTexture(texture, None, ctypes.c_void_p(rgb.ctypes.data), VW *
  3)
          sdl2.SDL_RenderClear(renderer)
          sdl2.SDL_RenderCopy(renderer, texture, None, None)
          sdl2.SDL_RenderPresent(renderer)
          sdl2.SDL_Delay(16)

      sdl2.SDL_DestroyTexture(texture)
      sdl2.SDL_DestroyRenderer(renderer)
      sdl2.SDL_DestroyWindow(window)
      sdl2.SDL_Quit()


if __name__ == "__main__":
    main()