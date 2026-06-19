import ctypes, sdl2
sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO)

window = sdl2.SDL_CreateWindow(
    b"Olympus",
    sdl2.SDL_WINDOWPOS_CENTERED, sdl2.SDL_WINDOWPOS_CENTERED,
    640, 640,
    sdl2.SDL_WINDOW_SHOWN)
renderer = sdl2.SDL_CreateRenderer(window, -1, sdl2.SDL_RENDERER_ACCELERATED)

event = sdl2.SDL_Event()
running = True
while running:
    while sdl2.SDL_PollEvent(ctypes.byref(event)):
        if event.type == sdl2.SDL_QUIT:
            running = False
        elif event.type == sdl2.SDL_KEYDOWN:
            if event.key.keysym.sym == sdl2.SDLK_ESCAPE:
                running = False
    
    sdl2.SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255)
    sdl2.SDL_RenderClear(renderer)
    sdl2.SDL_RenderPresent(renderer)

sdl2.SDL_DestroyRenderer(renderer)
sdl2.SDL_DestroyWindow(window)
sdl2.SDL_Quit()