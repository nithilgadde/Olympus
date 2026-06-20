import ctypes, sdl2
import numpy as np
import math
from palette import BLACK, RED, YELLOW
from screen import Screen

SCREEN_W, SCREEN_H = 128, 128
SCALE = 5
WINDOW_W, WINDOW_H = SCREEN_W * SCALE, SCREEN_H * SCALE


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
    
    #test new code in here
    # screen.cls(BLACK)
    # screen.circfill(40, 64, 20, RED)
    # screen.circ(90, 64, 25, YELLOW)

    screen.cls(BLACK)
    cx, cy = 64, 64
    for angle in range(0, 360, 15):
        rad = math.radians(angle)
        x = cx + int(50 * math.cos(rad))
        y = cy + int(50 * math.sin(rad))
        screen.line(cx, cy, x, y, 8 + (angle // 45) % 8)

    rgb = screen.to_rgb()
    sdl2.SDL_UpdateTexture(texture, None, ctypes.c_void_p(rgb.ctypes.data), SCREEN_W * 3)
    sdl2.SDL_RenderClear(renderer)
    sdl2.SDL_RenderCopy(renderer, texture, None, None)
    sdl2.SDL_RenderPresent(renderer)

sdl2.SDL_DestroyTexture(texture)
sdl2.SDL_DestroyRenderer(renderer)
sdl2.SDL_DestroyWindow(window)
sdl2.SDL_Quit()