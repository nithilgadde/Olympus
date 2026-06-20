import numpy as np
from palette import PALETTE

class Screen:

    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.fb = np.zeros((h, w), dtype=np.uint8)

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