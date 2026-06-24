# Olympus

A from-scratch game engine for Python. Build tiny pixel games on a 128×128 screen with a fixed 16-color palette and a few lines of code.

<img width="628" height="664" alt="CleanShot 2026-06-22 at 21 23 02" src="https://github.com/user-attachments/assets/c13f556d-5366-4835-88db-5f09cf761020" />


## Try it

```
pip install olympus-engine
```

## Quick start

Make a game in about 15 lines:

```python
import olympus as ol

screen = ol.Screen(128, 128)
x, y = 60, 60

def update():
    global x, y
    if screen.btn(ol.LEFT):  x -= 1
    if screen.btn(ol.RIGHT): x += 1
    if screen.btn(ol.UP):    y -= 1
    if screen.btn(ol.DOWN):  y += 1

def draw():
    screen.cls(ol.BLACK)
    screen.rectfill(x, y, x + 7, y + 7, ol.RED)
    screen.text("HELLO OLYMPUS", 18, 40, ol.WHITE)

screen.run(update, draw)
```

You write `update` (game logic) and `draw` (pixels); the engine runs them 60 times a second and handles the window, input, and rendering.

# You can check out the documentation in the Wiki Tab!

## Features

- **128×128 indexed framebuffer** with a fixed 16-color palette — the classic fantasy-console look.
- **Hand-written rasterizers**: pixels, lines (Bresenham), rectangles, and circles (midpoint), outlined or filled.
- **Sprites** you can hand-draw as text or load from a PNG — loaded images are automatically quantized down to the 16-color palette.
- **Animation, tilemaps, and AABB collision** — cycle frames for walk cycles, build levels as grids of characters, and check what's solid.
- **A built-in pixel font** for scores, labels, and menus.
- **Sound**: square-wave synthesis for retro blips, plus loading and playing your own `.wav` files.
- **A built-in sprite editor** — draw with the mouse and export straight to engine code, with undo, save/load, and onion-skinning.


To run the sprite editor, run this command in the terminal:
```
olympus-editor
```

## Running locally

Requirements:

- **Python 3.9+**
- No system libraries to install by hand — `pysdl2-dll` ships the SDL2 binaries, and `pip` installs everything else (numpy, PySDL2, Pillow) automatically.

From the project root (the folder with `pyproject.toml`):

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -e .

python examples/demo.py         # run the demo game
olympus-editor                  # open the sprite editor
```

## How it works

Olympus is "from scratch" in a specific, deliberate way: **no graphics or game library does the drawing.** The screen is a NumPy array of palette *indices* (not RGB), and every shape is rasterized by hand — Bresenham lines, midpoint circles, a sprite blitter, a pixel font, and square-wave audio synthesized sample by sample. SDL2 is only used to open a window, present the finished pixel buffer, and read input. It is **not** a wrapper around pygame.

A couple of decisions worth calling out:

- **The framebuffer stores color indices, not RGB.** Drawing just writes small integers (0–15) into a 2D array, which is fast and keeps the palette constraint baked into the design. The conversion to real RGB happens once per frame, with a single NumPy lookup, right before handing the buffer to SDL.
- **Loading a PNG means quantizing it.** Because the framebuffer is indexed, imported images can't be copied pixel-for-pixel — every pixel is snapped to its nearest palette color in a vectorized NumPy pass. That preserves the console's look no matter what art you throw at it.

## Credits

Built with [PySDL2](https://github.com/py-sdl/py-sdl2) (windowing, input, audio output), [NumPy](https://numpy.org/) (the framebuffer and rasterization), and [Pillow](https://python-pillow.org/) (PNG decoding). Inspired by [PICO-8](https://www.lexaloffle.com/pico-8.php) and the fantasy-console idea.

Created by Nithil Gadde (@nithilgadde) · MIT License
