import ctypes
import wave
import numpy as np
import sdl2

SAMPLE_RATE = 22050   # audio samples per second


def load_wav(path, rate=SAMPLE_RATE):
      """Load a .wav file and convert it to the engine's format
      (mono, 16-bit, SAMPLE_RATE). Returns an int16 numpy array."""
      wv = wave.open(path, "rb")
      nch = wv.getnchannels()
      width = wv.getsampwidth()
      fr = wv.getframerate()
      raw = wv.readframes(wv.getnframes())
      wv.close()

      # raw bytes -> float samples in -1..1, whatever the bit depth was
      if width == 1:
          a = (np.frombuffer(raw, np.uint8).astype(np.float32) - 128) / 128.0
      elif width == 2:
          a = np.frombuffer(raw, np.int16).astype(np.float32) / 32768.0
      elif width == 4:
          a = np.frombuffer(raw, np.int32).astype(np.float32) / 2147483648.0
      else:
          raise ValueError("unsupported WAV sample width: %d bytes" % width)

      if nch > 1:                       # stereo -> mono: average the channels
          a = a.reshape(-1, nch).mean(axis=1)

      if fr != rate:                    # resample to our rate
          m = len(a)
          new = max(1, int(m * rate / fr))
          a = np.interp(np.linspace(0, 1, new), np.linspace(0, 1, m), a)

      return (a * 32767).astype(np.int16)


class Sound:
      def __init__(self):
          sdl2.SDL_InitSubSystem(sdl2.SDL_INIT_AUDIO)
          spec = sdl2.SDL_AudioSpec(SAMPLE_RATE, sdl2.AUDIO_S16SYS, 1, 1024)
          self.dev = sdl2.SDL_OpenAudioDevice(None, 0, spec, None, 0)
          if self.dev:
              sdl2.SDL_PauseAudioDevice(self.dev, 0)

      def play(self, freq, ms, volume=0.3):
          """Synthesize and play a square-wave beep."""
          if not self.dev:
              return
          n = int(SAMPLE_RATE * ms / 1000)
          t = np.arange(n)
          phase = (freq * t / SAMPLE_RATE) % 1.0
          square = np.where(phase < 0.5, 1.0, -1.0)
          fade = max(1, int(SAMPLE_RATE * 0.005))
          if n > 2 * fade:
              square[:fade] *= np.linspace(0, 1, fade)
              square[-fade:] *= np.linspace(1, 0, fade)
          data = (square * volume * 32767).astype(np.int16)
          sdl2.SDL_QueueAudio(self.dev, data.ctypes.data_as(ctypes.c_void_p), data.nbytes)

      def play_clip(self, clip, volume=1.0):
          """Play a clip loaded with load_wav()."""
          if not self.dev or clip is None:
              return
          if volume != 1.0:
              clip = (clip.astype(np.float32) * volume).astype(np.int16)
          sdl2.SDL_QueueAudio(self.dev, clip.ctypes.data_as(ctypes.c_void_p), clip.nbytes)