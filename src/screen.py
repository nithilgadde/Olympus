import numpy as np
from palette import PALETTE
import ctypes, sdl2

LEFT, RIGHT, UP, DOWN, O, X = 0, 1, 2, 3, 4, 5

_SCANCODES = [
    sdl2.SDL_SCANCODE_LEFT,
    sdl2.SDL_SCANCODE_RIGHT,
    sdl2.SDL_SCANCODE_UP,
    sdl2.SDL_SCANCODE_DOWN,
    sdl2.SDL_SCANCODE_Z,
    sdl2.SDL_SCANCODE_X,
]

class Screen:

    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.fb = np.zeros((h, w), dtype=np.uint8)
        self._btn = [False] * 6
        self._prev = [False] * 6

    def cls(self, color):
        self.fb[:, :] = color

    def pset(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.fb[y, x] = color

    def line(self, x0, y0, x1, y1, color):
        x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            self.pset(x0, y0, color)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy
    
    def rectfill(self, x0, y0, x1, y1, color):
        x0, x1 = sorted((int(x0), int(x1)))
        y0, y1 = sorted((int(y0), int(y1)))
        x0 = max(0, x0)
        y0 = max(0, y0)
        x1 = min(self.w - 1, x1)
        y1 = min(self.h - 1, y1)
        if x0 <= x1 and y0 <= y1:
            self.fb[y0:y1 + 1, x0:x1 + 1] = color
    
    def rect(self, x0, y0, x1, y1, color):
        self.line(x0, y0, x1, y0, color)
        self.line(x0, y1, x1, y1, color)
        self.line(x0, y0, x0, y1, color)
        self.line(x1, y0, x1, y1, color)

    def circ(self, cx, cy, r, color):
        cx, cy, r = int(cx), int(cy), int(r)
        if r < 0:
            return
        x = r
        y = 0
        err = 1 - r
        while x >= y:
            self.pset(cx + x, cy + y, color)
            self.pset(cx + y, cy + x, color)
            self.pset(cx - y, cy + x, color)
            self.pset(cx - x, cy + y, color)
            self.pset(cx - x, cy - y, color)
            self.pset(cx - y, cy - x, color)
            self.pset(cx + y, cy - x, color)
            self.pset(cx + x, cy - y, color)
            y += 1
            if err < 0:
                err += 2 * y + 1
            else:
                x -= 1
                err += 2 * (y - x) + 1
    
    def circfill(self, cx, cy, r, color):
        cx, cy, r = int(cx), int(cy), int(r)
        if r < 0:
            return
        x = r
        y = 0
        err = 1 - r
        while x >= y:
              # instead of plotting 8 edge points, draw horizontal spans between them
            self.rectfill(cx - x, cy + y, cx + x, cy + y, color)
            self.rectfill(cx - x, cy - y, cx + x, cy - y, color)
            self.rectfill(cx - y, cy + x, cx + y, cy + x, color)
            self.rectfill(cx - y, cy - x, cx + y, cy - x, color)
            y += 1
            if err < 0:
                err += 2 * y + 1
            else:
                x -= 1
                err += 2 * (y - x) + 1

    def to_rgb(self):
        return np.ascontiguousarray(PALETTE[self.fb])
    
    def btn(self, i):
        return self._btn[i]
    
    def btnp(self, i):
        return self._btn[i] and not self._prev[i]
    
    def spr(self, sprite, x, y, flip_x=False, flip_y=False):
        s = sprite
        if flip_x:
            s = s[:, ::-1]
        if flip_y:
            s = s[::-1, :]
        sh, sw = s.shape
        x, y = int(x), int(y)

        sx0 = max(0, -x)
        sy0 = max(0, -y)
        sx1 = min(sw, self.w - x)
        sy1 = min(sh, self.h - y)
        if sx0 >= sx1 or sy0 >= sy1:
            return
        
        sub = s[sy0:sy1, sx0:sx1]
        dst = self.fb[y + sy0:y + sy1, x + sx0:x + sx1]
        mask = sub != 255
        dst[mask] = sub[mask]
    
    def run(self, update, draw, scale=5, title=b"Olympus"):
        sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO)
        win_w, win_h = self.w * scale, self.h * scale

        window = sdl2.SDL_CreateWindow(
            title,
            sdl2.SDL_WINDOWPOS_CENTERED, sdl2.SDL_WINDOWPOS_CENTERED,
            win_w, win_h,
            sdl2.SDL_WINDOW_SHOWN)

        renderer = sdl2.SDL_CreateRenderer(window, -1, sdl2.SDL_RENDERER_ACCELERATED)
        sdl2.SDL_SetHint(sdl2.SDL_HINT_RENDER_SCALE_QUALITY, b"0")
        texture = sdl2.SDL_CreateTexture(
            renderer,
            sdl2.SDL_PIXELFORMAT_RGB24,
            sdl2.SDL_TEXTUREACCESS_STREAMING,
            self.w, self.h)
        
        event = sdl2.SDL_Event()
        running = True
        while running:
            while sdl2.SDL_PollEvent(ctypes.byref(event)):
                if event.type == sdl2.SDL_QUIT:
                    running = False
                elif event.type == sdl2.SDL_KEYDOWN and \
                        event.key.keysym.sym == sdl2.SDLK_ESCAPE:
                    running = False
            
            keystate = sdl2.SDL_GetKeyboardState(None)
            self._prev = self._btn
            self._btn = [bool(keystate[sc]) for sc in _SCANCODES]

            update()
            draw()

            rgb = self.to_rgb()
            sdl2.SDL_UpdateTexture(texture, None, ctypes.c_void_p(rgb.ctypes.data), self.w * 3)
            sdl2.SDL_RenderClear(renderer)
            sdl2.SDL_RenderCopy(renderer, texture, None, None)
            sdl2.SDL_RenderPresent(renderer)
            sdl2.SDL_Delay(16)

        sdl2.SDL_DestroyTexture(texture)
        sdl2.SDL_DestroyRenderer(renderer)
        sdl2.SDL_DestroyWindow(window)
        sdl2.SDL_Quit()

        