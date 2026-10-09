import pygame
import config


class Camera:
    def __init__(self, width, height, game):
        self.game = game

        self.width = width
        self.height = height

        self.x = 0
        self.y = 0

        self.camera = pygame.Rect(0, 0, width, height)

    def update(self):
        player = self.game.player.get_rect()

        target_x = player.centerx - self.width // 2
        target_y = player.centery - self.height // 2

        self.x += (target_x - self.x) * 0.1
        self.y += (target_y - self.y) * 0.1

        self.x = max(0, min(self.x, self.game.gameScreen.width - self.width))

        self.y = max(0, min(self.y, self.game.gameScreen.height - self.height))

        self.camera.topleft = (int(self.x), int(self.y))
