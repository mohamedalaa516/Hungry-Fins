import pygame
from pygame.mixer import find_channel
import config
from utilities.animation import Animation
import random


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

    def update(self):
        self.animation.update()
        self.surface = self.animation.getImage()

    def get_rect(self):
        return self.surface.get_rect(topleft=(self.pos[0], self.pos[1]))

    def draw(self):
        if config.DEBUG:
            pygame.draw.rect(self.game.gameScreen, (255, 0, 0), self.get_rect(), 1)
        flippedSurf = pygame.transform.flip(self.surface, self.flip, False)

        self.game.gameScreen.blit(flippedSurf, self.pos)


class Enemy(EntityPhysics):
    # enemy goes from left to right or reverse
    def __init__(self, game, frames, pos, level) -> None:
        super().__init__(game, frames, pos, level)
        self.time = 0.0
        self.timeDuration = 3
        self.level = level
        if self.pos[0] <= 0:
            self.speed = 1
        else:
            self.speed = -1

        self.escapeSpeed = 1.5
        self.dying = False

        self.flip = self.speed == -1
        self.alive = True
        self.gameStart = True

    def detectPlayer(self, playerPos):
        distance = pygame.math.Vector2.distance_to(
            pygame.Vector2(self.pos), pygame.Vector2(playerPos)
        )
        return distance <= 100

    def update(self):
        if not self.dying:
            self.flip = self.speed < 0
        self.time += 1
        if self.time > self.timeDuration:
            self.volicity[0] = self.speed
            self.time = 0

        if self.detectPlayer(self.game.player.pos):
            if self.level <= self.game.player.level:
                if self.game.player.pos[0] > self.pos[0]:
                    self.speed = -abs(self.escapeSpeed)
                else:
                    self.speed = abs(self.escapeSpeed)
            else:
                dx = self.game.player.pos[0] - self.pos[0]
                dy = self.game.player.pos[1] - self.pos[1]

                self.volicity[0] = self.speed if dx > 0 else -self.speed
                self.volicity[1] = self.speed if dy > 0 else -self.speed

        if self.dying and self.animation.finished:
            self.alive = False

        self.pos[0] += self.volicity[0]
        if self.pos[0] > config.GAME_WIDTH + 100 or self.pos[0] < -100:
            if self.gameStart:
                self.gameStart = False
            else:
                self.alive = False
        self.pos[1] += self.volicity[1]
        tilesCollision = self.game.tilesMap.get_collisions()
        for collision in tilesCollision:
            if config.DEBUG:
                pygame.draw.rect(self.game.gameScreen, (255, 255, 0), collision, 1)
            rect = self.get_rect()
            if self.get_rect().colliderect(collision):
                if self.volicity[1] < 0:
                    rect.top = collision.bottom
                elif self.volicity[1] > 0:
                    rect.bottom = collision.top
                self.pos[1] = rect.y
        return super().update()

    def draw(self):
        if self.alive:
            return super().draw()


class Player(EntityPhysics):
    def __init__(self, game, frames, pos, level, sizeToGrow) -> None:
        super().__init__(game, frames, pos, level)
        self.speed = 3
        self.dir = {"left": False, "right": False, "up": False, "down": False}
        self.startGame = True
        self.attack = False
        self.numberOfEating = 8
        self.sizeToGrow = sizeToGrow

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

        if key[pygame.K_SPACE] and not self.attack:
            self.attack = True
            self.animation.restart()

    def changeState(self):
        if self.attack:
            self.animation.setAnimation(
                self.game.loader[f"player/{self.game.playerType}/attack"], loop=False
            )
            if self.animation.finished:
                self.attack = False
        else:
            self.animation.setAnimation(
                self.game.loader[f"player/{self.game.playerType}/idle"], loop=True
            )

    def eat(self):
        if not self.attack:
            return
        for enemy in self.game.enemies[:]:
            if self.get_rect().colliderect(enemy.get_rect()):
                if self.level >= enemy.level and not enemy.dying:
                    enemy.dying = True
                    enemy.animation.restart()
                    enemy.animation.setAnimation(self.game.loader["blood"], loop=False)
                    enemy.volicity = [0, 0]
                    self.numberOfEating += enemy.level

    def changeSize(self):
        if self.numberOfEating >= self.sizeToGrow[0]:
            self.game.playerType = "medium"
            self.level = 2
        if self.numberOfEating >= self.sizeToGrow[1]:
            self.game.playerType = "large"
            self.level = 3

    def update(self):
        self.changeState()
        self.eat()
        self.changeSize()
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
        return super().update()
