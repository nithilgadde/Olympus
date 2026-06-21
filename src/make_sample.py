import os
from PIL import Image, ImageDraw

HERE = os.path.dirname(__file__)
os.makedirs(os.path.join(HERE, "assets"), exist_ok=True)

img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))   # transparent background
d = ImageDraw.Draw(img)
d.ellipse([4, 1, 11, 8], fill=(40, 200, 60))      # head  (not exactly palette green)
d.rectangle([5, 8, 10, 14], fill=(200, 40, 40))   # body  (not exactly palette red)
d.point((6, 4), fill=(255, 255, 255))             # eyes
d.point((9, 4), fill=(255, 255, 255))

img.save(os.path.join(HERE, "assets", "hero.png"))
print("wrote assets/hero.png")