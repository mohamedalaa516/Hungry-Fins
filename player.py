import pygame
import config
import random
from utilities.animation import Animation
from utilities.fade_in import FadeOut
from entities import EntityPhysics


class Player(EntityPhysics):
    def __init__(self, game, frames, pos, level, sizeToGrow) -> None:
        super().__init__(game, frames, pos, level)
        self.speed = config.PLAYER_SPEED
        self.dir = {"left": False, "right": False, "up": False, "down": False}
        self.startGame = True
        self.attack = False
        self.numberOfEating = 0
        self.previousNumberEating = 0
        self.sizeToGrow = sizeToGrow
        self.alive = True
        self.health = 3
        self.coolDown = 100
        self.time = 0.0
        self.score = 0
        self.playerType = config.PLAYER_TYPE
        self.powerUp = False
        self.die_sound = self.game.music_loader.sfx["die"]
        self.timeCombo = 100
        self.timeComboCurrent = 0
        self.eatCombo = 0
        self.eatComboPrevious = 0
        self.double = False
        self.triple = False
        self.doubleFadeOut = FadeOut(
            self.game.ui_loader["double"],
            self.get_rect(),
            "topright",
            [10, -10],
            self.game.gameScreen,
        )
        self.tripleFadeOut = FadeOut(
            self.game.ui_loader["triple"],
            self.get_rect(),
            "topright",
            [10, -10],
            self.game.gameScreen,
        )
        self.timeComboSpeed = 100
        self.timeComboSpeedCur = 0
        self.doubleSpeed = False

        self.multiplierPoint = 1
        self.multiplierPointTimer = 300
        self.multiplierPointRange = 0
        self.multiplierPointCur = 0.0
        self.multiplierPointMax = 6
        self.previousMultiplierPoint = 1

    def makeWhite(self, surface):
        white = surface.copy()

        mask = pygame.mask.from_surface(surface)
        white.blit(
            mask.to_surface(setcolor=(255, 255, 255, 255), unsetcolor=(0, 0, 0, 0)),
            (0, 0),
        )

        return white

    def checkMulti(self):
        if self.previousNumberEating < self.numberOfEating:
            self.multiplierPointRange = min(
                self.multiplierPointRange + 1, self.multiplierPointMax * 2
            )
            self.previousNumberEating = self.numberOfEating

        self.multiplierPointCur += 1

        if self.multiplierPointCur > self.multiplierPointTimer:
            self.multiplierPointRange = max(0, self.multiplierPointRange - 1)
            self.multiplierPointCur = 0

        if self.multiplierPointRange >= 12:
            self.multiplierPoint = 3
        elif self.multiplierPointRange >= 6:
            self.multiplierPoint = 2

        else:
            self.multiplierPoint = 1
        if self.multiplierPoint > self.previousMultiplierPoint:
            self.game.music_loader.sfx[f"{self.multiplierPoint}x"].play()
            self.previousMultiplierPoint = self.multiplierPoint
        elif self.multiplierPoint < self.previousMultiplierPoint:
            self.previousMultiplierPoint = self.multiplierPoint

    def checkCombo(self):
        if self.eatCombo == 0:
            return
        self.timeComboCurrent += 1
        if self.timeComboCurrent <= self.timeCombo:
            if self.eatCombo > 2 and self.eatComboPrevious < 3:
                self.tripleFadeOut.reset()
                self.game.music_loader.sfx["triple"].play()
                self.double = False
                self.triple = True
                self.eatComboPrevious = 3
                self.doubleSpeed = True
                self.timeComboSpeedCur = 0
            elif self.eatCombo == 2 and self.eatComboPrevious < 2:
                self.doubleFadeOut.reset()
                self.game.music_loader.sfx["double"].play()
                self.double = True
                self.eatComboPrevious = 2
                self.doubleSpeed = True
                self.timeComboSpeedCur = 0
        else:
            self.eatCombo = 0
            self.timeComboCurrent = 0
            self.eatComboPrevious = 0
            self.double = False

    def respawn(self):
        if self.health <= 0:
            return

        self.alive = True
        self.dying = False
        self.attack = False
        self.startGame = True

        # Reset player progress for the current life
        self.time = 0
        self.numberOfEating = 0
        self.playerType = config.PLAYER_TYPE
        self.level = 1

        # Reset movement
        self.pos = list(config.PLAYER_START_POS)
        self.volicity = [0, 0]
        self.speed = config.PLAYER_SPEED
        self.dir = {
            "left": False,
            "right": False,
            "up": False,
            "down": False,
        }
        self.flip = False

        # Reset combo state
        self.eatCombo = 0
        self.eatComboPrevious = 0
        self.timeComboCurrent = 0
        self.double = False
        self.triple = False

        # Reset speed boost
        self.doubleSpeed = False
        self.timeComboSpeedCur = 0

        # Reset combo UI
        self.doubleFadeOut.reset()
        self.tripleFadeOut.reset()
        # Reset multiplier state
        self.multiplierPoint = 1
        self.multiplierPointRange = 0
        self.multiplierPointCur = 0.0
        self.previousNumberEating = 0
        # Restore idle animation
        self.animation.restart()
        self.animation.setAnimation(
            self.game.loader[f"player/{self.playerType}/idle"],
            loop=True,
        )

    def handleInput(self):
        if not self.alive:
            return
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

    def startPowerUp(self):
        self.powerUp = True
        self.game.music_loader.sfx["growth"].play()
        self.animation.setAnimation(
            self.game.loader[f"player/{self.playerType}/powerUp"],
            loop=False,
            speed=0.05,
        )
        self.animation.restart()

    def changeState(self):
        if self.dying:
            if self.animation.finished:
                self.dying = False
                self.alive = False
                self.health -= 1
                self.respawn()
            return

        if self.powerUp:
            if self.animation.finished:
                self.powerUp = False
            return

        if self.attack:
            self.animation.setAnimation(
                self.game.loader[f"player/{self.playerType}/attack"],
                loop=False,
            )
            if self.animation.finished:
                self.attack = False
            return

        self.animation.setAnimation(
            self.game.loader[f"player/{self.playerType}/idle"],
            loop=True,
        )

    def attackEnemy(self):
        if not self.attack:
            return
        for enemy in self.game.enemies[:]:
            if self.get_hitbox().colliderect(enemy.get_hitbox()):
                if self.level >= enemy.level and not enemy.dying:
                    self.score += self.multiplierPoint * config.FISH_POINTS[enemy.type]
                    self.previousNumberEating = self.numberOfEating
                    self.numberOfEating += enemy.level
                    enemy.die()
                    self.chomp = random.choice(self.game.music_loader.sfx["chomp"])
                    self.chomp.play()
                    self.eatCombo += 1

    def die(self):
        self.dying = True
        self.die_sound.play()
        self.animation.restart()
        self.animation.setAnimation(self.game.loader["blood"], loop=False)

    def changeSize(self):
        if self.level == 1 and self.numberOfEating >= self.sizeToGrow[0]:
            self.playerType = "medium"
            self.level = 2
            self.startPowerUp()

        elif self.level == 2 and self.numberOfEating >= self.sizeToGrow[1]:
            self.playerType = "large"
            self.level = 3
            self.startPowerUp()

        if self.numberOfEating >= self.sizeToGrow[2]:
            self.game.win = True

    def update(self):
        self.time = min(self.time + 1, self.coolDown)
        self.changeState()
        self.attackEnemy()
        self.changeSize()
        self.checkCombo()
        self.checkMulti()
        if self.double:
            self.doubleFadeOut.update()
        if self.triple:
            self.tripleFadeOut.update()

        if self.doubleSpeed:
            self.timeComboSpeedCur += 1

        if self.timeComboSpeedCur > 0:
            if self.timeComboSpeedCur <= self.timeComboSpeed:
                self.speed = config.PLAYER_SPEED + 1
            else:
                self.speed = config.PLAYER_SPEED
                self.timeComboSpeedCur = 0
                self.doubleSpeed = False

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

    def draw(self):
        if not self.alive and not self.dying:
            return

        if self.time < self.coolDown and int(self.time / 6) % 2 == 0:
            image = self.makeWhite(self.surface)
        else:
            image = self.surface

        flippedSurf = pygame.transform.flip(image, self.flip, False)
        self.game.gameScreen.blit(flippedSurf, self.pos)

        if self.double:
            self.doubleFadeOut.draw(self.get_rect())
        if self.triple:
            self.tripleFadeOut.draw(self.get_rect())

        if config.DEBUG:
            pygame.draw.rect(self.game.gameScreen, (255, 0, 0), self.get_rect(), 1)
            pygame.draw.rect(self.game.gameScreen, (0, 255, 255), self.get_hitbox(), 1)
