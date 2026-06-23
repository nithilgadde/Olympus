class Anim:
    def __init__(self, frames, speed=6):
        self.frames = frames
        self.speed = speed
        self.t = 0
        self.i = 0

    def reset(self):
        self.t = 0
        self.i = 0

    def update(self):
        self.t += 1
        if self.t >= self.speed:
            self.t = 0
            self.i = (self.i + 1) % len(self.frames)

    def frame(self):
        return self.frames[self.i]

