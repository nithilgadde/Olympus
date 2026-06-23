from .sprites import make_sprite

TILE = 8

WALL = make_sprite([
    "55555555",
    "56666665",
    "56666665",
    "56666665",
    "56666665",
    "56666665",
    "56666665",
    "55555555",
])

COIN = make_sprite([
    "........",
    "..aaaa..",
    ".aaaaaa.",
    ".aaaaaa.",
    ".aaaaaa.",
    ".aaaaaa.",
    "..aaaa..",
    "........",
])

TILES = {
    'W': WALL,
    'C': COIN,
}

SOLID = {'W'}

class Tilemap:
    def __init__(self, rows, tiles, solid):
        self.rows = rows
        self.tiles = tiles
        self.solid = solid
        self.h = len(rows)
        self.w = len(rows[0])

    def get(self, col, row):
        if 0 <= row < self.h and 0 <= col < self.w:
            return self.rows[row][col]
        
    def set(self, col, row, ch):
        line = self.rows[row]
        self.rows[row] = line[:col] + ch + line[col + 1:]

    def draw(self, screen):
        for row in range(self.h):
            for col in range(self.w):
                sprite = self.tiles.get(self.rows[row][col])
                if sprite is not None:
                    screen.spr(sprite, col * TILE, row * TILE)

    def solid_at(self, x, y):
        return self.get(x // TILE, y // TILE) in self.solid
    
    def box_hits_solid(self, x, y, w, h):
        return (self.solid_at(x, y) or
                self.solid_at(x + w - 1, y) or
                self.solid_at(x, y + h - 1) or
                self.solid_at(x + w - 1, y + h - 1))
    