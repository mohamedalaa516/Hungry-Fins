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
        self.color = (247, 150, 23)
        # A dark purple with a grayish undertone.
        self.scoreText = self.font.render(f"{self.points}", True, self.color)
        self.multiText = self.font.render("1x", True, self.color)
        self.offsetY = 10

        # health
        self.healthBar = scaleImage(self.game.ui_loader["healthBar"], scale=3)
        self.healthList = []
        for singleHealth in range(self.game.player.health):
            self.healthList.append(
                scaleImage(self.game.ui_loader["healthBar/full"], scale=3)
            )
        self.indexHealthList = len(self.healthList)

    def update(self):
        self.points = self.game.player.score
        self.scoreText = self.font.render(f"{self.points}", True, self.color)

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
