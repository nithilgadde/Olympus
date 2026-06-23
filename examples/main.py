import os
from olympus import BLACK, WHITE
from olympus import Screen
from olympus import Sound, load_wav

HERE = os.path.dirname(__file__)

screen = Screen(128, 128)
snd = Sound()
music = load_wav(os.path.join(HERE, "assets", "bkgmusic.wav"))

started = False


def update():
      global started
      if not started:          # play the music once, on the first frame
          snd.play_clip(music)
          started = True


def draw():
      screen.cls(BLACK)
      screen.text("MUSIC PLAYING", 24, 60, WHITE)


screen.run(update, draw)