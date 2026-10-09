import random


class CameraShake:
    def __init__(self):
        self.time = 0
        self.strength = 0

    def start(self, duration, strength):
        self.time = duration
        self.strength = strength

    def update(self, dt):
        if self.time <= 0:
            return (0, 0)

        self.time -= dt

        return (
            random.randint(-self.strength, self.strength),
            random.randint(-self.strength, self.strength)
        )