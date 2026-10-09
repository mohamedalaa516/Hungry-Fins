import pygame
from utilities.animation import Animation


class EntityPhysics:
    def __init__(self, surface, pos) -> None:
        pass


class Player:
    def __init__(self, game, frames, pos) -> None:
        self.frames = frames
        self.frameDuration = 1
        self.frameSpeed = 0.2
        self.animation = Animation(
            self.frameDuration, frames, self.frameSpeed, loop=True
        )
        self.surface = self.animation.getImage()
        self.pos = list(pos)
        self.game = game
        self.volicity = [0, 0]
        self.speed = 3
        self.flip = False
        self.dir = {"left": False, "right": False, "up": False, "down": False}
        self.startGame = True

    def get_rect(self):
        return self.surface.get_rect(topleft=(self.pos[0], self.pos[1]))

    def handleInput(self):
        key = pygame.key.get_pressed()
        self.volicity = [0, 0]

        if key[pygame.K_d]:
            self.volicity[0] += self.speed
            self.dir = {"left": False, "right": True, "up": False, "down": False}
        if key[pygame.K_a]:
            self.volicity[0] -= self.speed
            self.dir = {"left": True, "right": False, "up": False, "down": False}
        if key[pygame.K_w]:
            self.volicity[1] -= self.speed
            self.dir = {"left": False, "right": False, "up": True, "down": False}
        if key[pygame.K_s]:
            self.volicity[1] += self.speed
            self.dir = {"left": False, "right": False, "up": False, "down": True}

    def update(self):
        self.animation.update()
        self.surface = self.animation.getImage()
        if self.dir["left"]:
            self.flip = True
        elif self.dir["right"]:
            self.flip = False
        if self.startGame:
            self.volicity[1] += self.speed * 3
            if self.pos[1] >= 200:
                self.startGame = False
        self.pos[0] += self.volicity[0]
        if not self.startGame:
            tilesCollision = self.game.tilesMap.get_collisions()
            for collision in tilesCollision:
                rect = self.get_rect()
                if self.get_rect().colliderect(collision):
                    if self.volicity[0] > 0:
                        rect.right = collision.left
                    elif self.volicity[0] < 0:
                        rect.left = collision.right

                    self.pos[0] = rect.x
        self.pos[1] += self.volicity[1]
        if not self.startGame:
            tilesCollision = self.game.tilesMap.get_collisions()
            for collision in tilesCollision:
                rect = self.get_rect()
                if self.get_rect().colliderect(collision):
                    if self.volicity[1] > 0:
                        rect.bottom = collision.top
                    elif self.volicity[1] < 0:
                        rect.top = collision.bottom
                    self.pos[1] = rect.y

    def draw(self):
        flippedSurf = pygame.transform.flip(self.surface, self.flip, False)

        self.game.gameScreen.blit(flippedSurf, self.pos)
