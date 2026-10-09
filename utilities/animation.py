import pygame


class Animation:
    def __init__(self, frameDuration, frames, speed, loop=False) -> None:
        # increase the value of index
        # finished Animation
        # loop Animation
        # return current image
        self.frames = frames
        self.currentIndex = 0
        self.timer = 0.0
        self.frameDuration = frameDuration
        self.speed = speed
        self.finished = False
        self.loop = loop

    def update(self):
        self.timer += self.speed

        if self.timer > self.frameDuration:
            self.timer = 0.0
            if self.currentIndex >= len(self.frames) - 1:
                if not self.loop:
                    self.currentIndex = len(self.frames) - 1
                    self.finished = True
                else:
                    self.currentIndex = (self.currentIndex + 1) % len(self.frames)
            else:
                self.currentIndex += 1

    def getImage(self):
        return self.frames[self.currentIndex]
