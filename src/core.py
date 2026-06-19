import ctypes, sdl2
import numpy as np

SCREEN_W, SCREEN_H = 128, 128
SCALE = 5
WINDOW_W, WINDOW_H = SCREEN_W * SCALE, SCREEN_H * SCALE

PALETTE = np.array([
    (0, 0, 0),        # 0  black
    (29, 43, 83),     # 1  dark-blue
    (126, 37, 83),    # 2  dark-purple
    (0, 135, 81),     # 3  dark-green
    (171, 82, 54),    # 4  brown
    (95, 87, 79),     # 5  dark-grey
    (194, 195, 199),  # 6  light-grey
    (255, 241, 232),  # 7  white
    (255, 0, 77),     # 8  red
    (255, 163, 0),    # 9  orange
    (255, 236, 39),   # 10 yellow
    (0, 228, 54),     # 11 green
    (41, 173, 255),   # 12 blue
    (131, 118, 156),  # 13 indigo
    (255, 119, 168),  # 14 pink
    (255, 204, 170),  # 15 peach
  ], dtype=np.uint8)

  # friendly names, so you can write screen.pset(x, y, RED)
BLACK, DARKBLUE, DARKPURPLE, DARKGREEN = 0, 1, 2, 3
BROWN, DARKGREY, LIGHTGREY, WHITE = 4, 5, 6, 7
RED, ORANGE, YELLOW, GREEN = 8, 9, 10, 11
BLUE, INDIGO, PINK, PEACH = 12, 13, 14, 15

class Screen:

    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.fb = np.zeros((h, w, 3), dtype=np.uint8)

    def cls(self, color):
        self.fb[:, :] = color

    def pset(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.fb[y, x] = color

    def to_rgb(self):
        return np.ascontiguousarray(PALETTE[self.fb])


sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO)

window = sdl2.SDL_CreateWindow(
    b"Olympus",
    sdl2.SDL_WINDOWPOS_CENTERED, sdl2.SDL_WINDOWPOS_CENTERED,
    WINDOW_W, WINDOW_H,
    sdl2.SDL_WINDOW_SHOWN)

renderer = sdl2.SDL_CreateRenderer(window, -1, sdl2.SDL_RENDERER_ACCELERATED)

sdl2.SDL_SetHint(sdl2.SDL_HINT_RENDER_SCALE_QUALITY, b"0")
texture = sdl2.SDL_CreateTexture(
    renderer,
    sdl2.SDL_PIXELFORMAT_RGB24,
    sdl2.SDL_TEXTUREACCESS_STREAMING,
    SCREEN_W, SCREEN_H,
)

screen = Screen(SCREEN_W, SCREEN_H)

event = sdl2.SDL_Event()
running = True
while running:
    while sdl2.SDL_PollEvent(ctypes.byref(event)):
        if event.type == sdl2.SDL_QUIT:
            running = False
        elif event.type == sdl2.SDL_KEYDOWN:
            if event.key.keysym.sym == sdl2.SDLK_ESCAPE:
                running = False
    
    screen.cls(GREEN)
    for i in range(20):
        screen.pset(i, i, RED)

    rgb = screen.to_rgb()
    sdl2.SDL_UpdateTexture(texture, None, ctypes.c_void_p(rgb.ctypes.data), SCREEN_W * 3)
    sdl2.SDL_RenderClear(renderer)
    sdl2.SDL_RenderCopy(renderer, texture, None, None)
    sdl2.SDL_RenderPresent(renderer)

sdl2.SDL_DestroyTexture(texture)
sdl2.SDL_DestroyRenderer(renderer)
sdl2.SDL_DestroyWindow(window)
sdl2.SDL_Quit()