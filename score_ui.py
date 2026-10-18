from pygame.transform import scale

from utilities.ui_helper import scaleImage
import pygame
from os.path import join


class Score:
    def __init__(self, game) -> None:
        # add ui and score point
        # add ui and mutli point
        self.game = game
        self.font = pygame.font.Font(join("assets", "Fonts", "yoster.ttf"), 34)
        self.points = 0
        self.mutliPoint = 1
        self.color = (247, 150, 23)
        # A dark purple with a grayish undertone.
        self.scoreText = self.font.render(f"{self.points}", True, self.color)
        self.multiText = self.font.render(f"{self.mutliPoint}X", True, self.color)
        self.offsetY = 10

        # health
        self.healthBar = scaleImage(self.game.ui_loader["healthBar"], scale=3)
        self.healthList = []
        for singleHealth in range(self.game.player.health):
            self.healthList.append(
                scaleImage(self.game.ui_loader["healthBar/full"], scale=3)
            )
        self.indexHealthList = len(self.healthList)

        # multipler fins
        self.fins1X = scaleImage(self.game.ui_loader["fins/1x"], scale=3)
        self.fins2X = scaleImage(self.game.ui_loader["fins/2x"], scale=3)
        self.fins3X = scaleImage(self.game.ui_loader["fins/3x"], scale=3)
        self.finsRect = self.fins1X.get_rect(
            midtop=(
                self.game.screen.get_rect().midtop[0],
                self.game.screen.get_rect().midtop[1] + 50,
            )
        )

    def update(self):
        self.points = self.game.player.score
        self.mutliPoint = self.game.player.multiplierPoint
        self.scoreText = self.font.render(f"{self.points}", True, self.color)
        self.multiText = self.font.render(f"{self.mutliPoint}X", True, self.color)
        if self.game.player.health < self.indexHealthList:
            self.healthList[self.indexHealthList - 1] = scaleImage(
                self.game.ui_loader["healthBar/empty"], scale=3
            )
            self.indexHealthList -= 1

    def draw(self):
        scoreBar = self.game.ui_loader["scoreBar"]
        scoreMulti = self.game.ui_loader["scoreBar/multi"]
        scoreBarScale = scaleImage(scoreBar, scale=3)
        scoreMultiScale = scaleImage(scoreMulti, scale=3)
        scoreBar_x = (
            self.game.screen.get_width()
            - scoreBarScale.get_width()
            - scoreMultiScale.get_width()
            - 10
        )
        scoreMulti_x = self.game.screen.get_width() - scoreMultiScale.get_width()
        scoreBarRect = scoreBarScale.get_rect(topleft=(scoreBar_x, self.offsetY))
        self.game.screen.blit(scoreBarScale, scoreBarRect)
        self.game.screen.blit(scoreMultiScale, (scoreMulti_x, self.offsetY))

        # Draw the base 1x image
        self.game.screen.blit(self.fins1X, self.finsRect)

        currentMulti = self.fins1X
        visibleWidth = 0
        if self.game.player.multiplierPointRange <= 6:
            progress = min(
                self.game.player.multiplierPointRange
                / self.game.player.multiplierPointMax,
                1,
            )
            visibleWidth = int(self.fins2X.get_width() * progress)
            currentMulti = self.fins2X
        elif self.game.player.multiplierPointRange <= 12:
            progress = min(
                (self.game.player.multiplierPointRange - 6)
                / (self.game.player.multiplierPointMax),
                1,
            )
            visibleWidth = int(self.fins3X.get_width() * progress)
            currentMulti = self.fins3X

        if visibleWidth > 0:
            sourceRect = pygame.Rect(
                0,
                0,
                visibleWidth,
                currentMulti.get_height(),
            )

            self.game.screen.blit(
                currentMulti,
                self.finsRect,
                area=sourceRect,
            )

        scoreRect = self.scoreText.get_rect(
            center=(
                scoreBar_x + scoreBarScale.get_width() // 2,
                self.offsetY + scoreBarScale.get_height() // 2,
            )
        )
        multiRect = self.multiText.get_rect(
            center=(
                scoreMulti_x - 10 + scoreMultiScale.get_width() // 2,
                self.offsetY + scoreMultiScale.get_height() // 2,
            )
        )
        healthRect = self.healthBar.get_rect(
            midtop=(scoreBarRect.midbottom[0], scoreBarRect.midbottom[1] + 10)
        )

        self.game.screen.blit(self.scoreText, scoreRect)
        self.game.screen.blit(self.multiText, multiRect)
        self.game.screen.blit(self.healthBar, healthRect)
        for index, healthItem in enumerate(self.healthList):
            healthItemRect = healthItem.get_rect(
                center=((healthRect.center[0] - 25) + index * 25, healthRect.center[1])
            )
            self.game.screen.blit(healthItem, healthItemRect)
