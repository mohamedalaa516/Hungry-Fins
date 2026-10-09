import pygame


class Particle:
    def __init__(self, game, color, radius, pos, speed) -> None:
        # many circle
        # move to specific direction
        self.game = game
        self.color = color
        self.radius = radius
        self.pos = list(pos)
        self.time = 0.0
        self.timeDuration = 20
        self.speed = speed
        self.alive = True

    def update(self):
        self.time += 1.0
        if self.time >= self.timeDuration:
            self.alive = False
            return
        self.radius -= 0.1
        self.pos[0] += self.speed[0]
        self.pos[1] += self.speed[1]

    def draw(self):
        if self.alive:
            pygame.draw.circle(
                self.game.gameScreen,
                self.color,
                (int(self.pos[0]), int(self.pos[1])),
                int(self.radius),
            )
