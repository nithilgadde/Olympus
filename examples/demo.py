import olympus as ol

screen = ol.Screen(128, 128)
snd = ol.Sound()

player = ol.make_sprite([
    "..0000..",
    ".0aaaa0.",
    ".0a00a0.",
    ".0aaaa0.",
    ".0aaaa0.",
    ".0a00a0.",
    ".0a..a0.",
    ".00..00.",
])
x, y = 60, 60


def update():
    global x, y
    if screen.btn(ol.LEFT):  x -= 1
    if screen.btn(ol.RIGHT): x += 1
    if screen.btn(ol.UP):    y -= 1
    if screen.btn(ol.DOWN):  y += 1
    if screen.btnp(ol.O):    snd.play(660, 80)


def draw():
    screen.cls(ol.DARKBLUE)
    screen.spr(player, x, y)
    screen.text("OLYMPUS DEMO", 28, 110, ol.WHITE)


screen.run(update, draw)
