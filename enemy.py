import pygame
import config
import random
from utilities.animation import Animation
from utilities.fade_in import FadeOut
from entities import EntityPhysics


class Enemy(EntityPhysics):
    # enemy goes from left to right or reverse
    def __init__(self, game, frames, pos, level, type) -> None:
        super().__init__(game, frames, pos, level)
        self.time = 0.0
        self.timeDuration = 3
        self.level = level
        if self.pos[0] <= 0:
            self.partrolDirection = 1
        else:
            self.partrolDirection = -1

        self.type = type
        self.escapeSpeed = config.FISH_ESCAPED[self.type]
        self.speed = config.FISH_SPEED[self.type]

        self.gameStart = True
        self.detect = False

        self.attack = False

    def detectPlayer(self, playerCenter):
        distance = pygame.math.Vector2.distance_to(
            pygame.Vector2(self.get_rect().center), pygame.Vector2(playerCenter)
        )
        return distance

    def isFullyOnScreen(self):
        rect = self.get_rect()
        return rect.left >= 20 and rect.right <= self.game.gameScreen.get_width() - 20

    def followPlayer(self):
        distance = self.detectPlayer(self.game.player.get_rect().center)
        can_chase = (
            self in self.game.reservationSet or len(self.game.reservationSet) < 1
        )

        if (
            distance <= 80
            and can_chase
            and not self.game.player.dying
            and self.game.player.alive
            and self.game.player.time >= self.game.player.coolDown
        ):
            dx = self.game.player.get_rect().centerx - self.get_rect().centerx
            dy = self.game.player.get_rect().centery - self.get_rect().centery
            if self.level <= self.game.player.level:
                direction = pygame.Vector2(-dx, 0)
                self.movementSpeed = self.escapeSpeed
            else:
                self.game.reservationSet.add(self)
                direction = pygame.Vector2(dx, dy)
                self.movementSpeed = self.speed

            if direction and self.isFullyOnScreen():
                direction = direction.normalize()
                self.volicity[0] = direction.x * self.movementSpeed
                self.volicity[1] = direction.y * self.movementSpeed
                self.partrolDirection = 1 if direction.x > 0 else -1
        else:
            self.volicity[0] = self.partrolDirection * self.speed
            self.volicity[1] = 0
            if self in self.game.reservationSet:
                self.game.reservationSet.remove(self)

    def changeState(self):
        if self.dying:
            self.animation.setAnimation(self.game.loader["blood"], loop=False)
            return
        if self.attack:
            self.animation.setAnimation(
                self.game.loader[f"{self.type}/attack"], loop=False, speed=0.1
            )
            if self.animation.finished:
                self.attack = False
            return

        else:
            self.animation.setAnimation(
                self.game.loader[f"{self.type}/idle"], loop=True
            )

    def attackPlayer(self):
        if self.get_hitbox().colliderect(self.game.player.get_hitbox()):
            if (
                self.level > self.game.player.level
                and self.game.player.alive
                and not self.game.player.dying
                and self.game.player.time >= self.game.player.coolDown
            ):
                self.game.player.die()
                self.animation.restart()
                self.attack = True

    def die(self):
        self.dying = True
        self.animation.restart()
        self.volicity = [0, 0]

    def update(self):
        if not self.alive:
            return
        if self.dying and self.animation.finished:
            self.dying = False
            self.alive = False
            return super().update()
        self.followPlayer()
        self.attackPlayer()
        self.changeState()

        if not self.dying:
            self.flip = self.volicity[0] < 0

        self.pos[0] += self.volicity[0]
        if self.pos[0] > config.GAME_WIDTH + 100 or self.pos[0] < -100:
            if self.gameStart:
                self.gameStart = False
            else:
                self.alive = False
        self.pos[1] += self.volicity[1]
        tilesCollision = self.game.tilesMap.get_collisions()
        rect = self.get_rect()
        for collision in tilesCollision:
            if config.DEBUG:
                pygame.draw.rect(self.game.gameScreen, (255, 255, 0), collision, 1)
            if rect.colliderect(collision):
                if self.volicity[1] > 0:
                    rect.bottom = collision.top
                elif self.volicity[1] < 0:
                    rect.top = collision.bottom
                self.pos[1] = rect.y
        return super().update()
