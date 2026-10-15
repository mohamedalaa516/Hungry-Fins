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


class Player(EntityPhysics):
    def __init__(self, game, frames, pos, level, sizeToGrow) -> None:
        super().__init__(game, frames, pos, level)
        self.speed = 3
        self.dir = {"left": False, "right": False, "up": False, "down": False}
        self.startGame = True
        self.attack = False
        self.numberOfEating = 5
        self.sizeToGrow = sizeToGrow
        self.tempVolicity = self.volicity
        self.alive = True
        self.health = 3
        self.coolDown = 100
        self.time = 0.0
        self.score = 0

    def makeWhite(self, surface):
        white = surface.copy()

        mask = pygame.mask.from_surface(surface)
        white.blit(
            mask.to_surface(setcolor=(255, 255, 255, 255), unsetcolor=(0, 0, 0, 0)),
            (0, 0),
        )

        return white

    def respawn(self):
        if self.health > 0:
            self.alive = True
            self.dying = False
            self.attack = False
            self.eaten = False
            self.startGame = True
            self.time = 0
            self.numberOfEating = 8
            self.game.playerType = "small"
            self.level = 1

            self.pos = list(config.PLAYER_START_POS)
            self.volicity = [0, 0]

            self.animation.restart()
            self.animation.setAnimation(
                self.game.loader[f"player/{self.game.playerType}/idle"], loop=True
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

    def changeState(self):
        if self.dying:
            if self.animation.finished:
                self.dying = False
                self.alive = False
                self.health -= 1
                self.respawn()
            return
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

    def attackEnemy(self):
        if not self.attack:
            return
        for enemy in self.game.enemies[:]:
            if self.get_hitbox().colliderect(enemy.get_hitbox()):
                if self.level >= enemy.level and not enemy.dying:
                    self.score += config.FISH_POINTS[enemy.type]
                    self.numberOfEating += enemy.level
                    enemy.die()
                    self.eaten = False

    def die(self):
        self.dying = True
        self.animation.restart()
        self.animation.setAnimation(self.game.loader["blood"], loop=False)

    def changeSize(self):
        if self.numberOfEating >= self.sizeToGrow[0]:
            self.game.playerType = "medium"
            self.level = 2
        if self.numberOfEating >= self.sizeToGrow[1]:
            self.game.playerType = "large"
            self.level = 3
        if self.numberOfEating >= self.sizeToGrow[2]:
            self.game.win = True

    def update(self):
        self.time = min(self.time + 1, self.coolDown)
        self.changeState()
        self.attackEnemy()
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

    def draw(self):
        if not self.alive and not self.dying:
            return

        if self.time < self.coolDown and int(self.time / 6) % 2 == 0:
            image = self.makeWhite(self.surface)
        else:
            image = self.surface

        flippedSurf = pygame.transform.flip(image, self.flip, False)
        self.game.gameScreen.blit(flippedSurf, self.pos)

        if config.DEBUG:
            pygame.draw.rect(self.game.gameScreen, (255, 0, 0), self.get_rect(), 1)
            pygame.draw.rect(self.game.gameScreen, (0, 255, 255), self.get_hitbox(), 1)
