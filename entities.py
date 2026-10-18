import pygame
import config
from utilities.animation import Animation


class EntityPhysics:
    def __init__(self, game, frames, pos, level) -> None:
        self.frames = frames
        self.level = level
        self.frameDuration = 1
        self.frameSpeed = 0.2
        self.animation = Animation(
            self.frameDuration, frames, self.frameSpeed, loop=True
        )
        self.surface = self.animation.getImage()
        self.pos = list(pos)
        self.game = game
        self.volicity = [0, 0]
        self.flip = False
        self.alive = True
        self.dying = False

    def update(self):
        self.animation.update()
        self.surface = self.animation.getImage()

    def get_rect(self):
        return self.surface.get_rect(topleft=(self.pos[0], self.pos[1]))

    def get_hitbox(self):
        rect = self.get_rect()

        mouthWidth = rect.width * 0.4
        mouthHeight = rect.height * 0.5
        mouthOffset = rect.width * 0.1

        if self.flip:
            x = rect.left - mouthOffset
        else:
            x = rect.right - mouthWidth + mouthOffset

        y = rect.centery - mouthHeight / 2
        return pygame.Rect(x, y, mouthWidth, mouthHeight)

    def draw(self):
        if config.DEBUG:
            pygame.draw.rect(self.game.gameScreen, (255, 0, 0), self.get_rect(), 1)

        if self.alive or self.dying:
            flippedSurf = pygame.transform.flip(self.surface, self.flip, False)
            self.game.gameScreen.blit(flippedSurf, self.pos)
        if config.DEBUG:
            pygame.draw.rect(self.game.gameScreen, (0, 255, 255), self.get_hitbox(), 1)
