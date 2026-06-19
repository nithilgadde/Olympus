import ctypes, sdl2
import numpy as np

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

fb = np.zeros((SCREEN_H, SCREEN_W, 3), dtype=np.uint8)

event = sdl2.SDL_Event()
running = True
while running:
    while sdl2.SDL_PollEvent(ctypes.byref(event)):
        if event.type == sdl2.SDL_QUIT:
            running = False
        elif event.type == sdl2.SDL_KEYDOWN:
            if event.key.keysym.sym == sdl2.SDLK_ESCAPE:
                running = False
    
    fb[:, :] = (0, 0, 40)
    fb[60:68, 60:68] = (255, 255, 255)

    sdl2.SDL_UpdateTexture(texture, None, ctypes.c_void_p(fb.ctypes.data), SCREEN_W * 3)
    sdl2.SDL_RenderClear(renderer)
    sdl2.SDL_RenderCopy(renderer, texture, None, None)
    sdl2.SDL_RenderPresent(renderer)

sdl2.SDL_DestroyTexture(texture)
sdl2.SDL_DestroyRenderer(renderer)
sdl2.SDL_DestroyWindow(window)
sdl2.SDL_Quit()