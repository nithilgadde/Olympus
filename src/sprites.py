import numpy as np
import os
from PIL import Image
from palette import PALETTE

TRANSPARENT = 255

def make_sprite(rows):
    h = len(rows)
    w = len(rows[0])
    s = np.full((h, w), TRANSPARENT, dtype=np.uint8)
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            if ch != '.':
                s[j, i] = int(ch, 16)
    return s

def load_sprite(path):
    img = Image.open(path).convert("RGBA")
    arr = np.array(img)
    rgb = arr[:, :, :3].astype(np.int32)
    alpha = arr[:, :, 3]

    pal = PALETTE.astype(np.int32)

    diff = rgb[:, :, None, :] - pal[None, None, :, :]
    dist = (diff * diff).sum(axis=3)
    idx = dist.argmin(axis=2).astype(np.uint8)

    idx[alpha < 128] = TRANSPARENT
    return idx

FISH = make_sprite([
      "........",
      "....999.",
      "9..9999.",
      "9999979.",
      "9999999.",
      "9..9999.",
      "....999.",
      "........",
])

SMILEY = make_sprite([
      "..aaaa..",
      ".aaaaaa.",
      "aa0aa0aa",
      "aaaaaaaa",
      "a0aaaa0a",
      "aa0000aa",
      ".aaaaaa.",
      "..aaaa..",
])
