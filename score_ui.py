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
        # A dark purple with a grayish undertone.
        self.scoreText = self.font.render(f"{self.points}", True, (46, 34, 47))
        self.multiText = self.font.render("1x", True, (46, 34, 47))
        self.offsetY = 10

    def update(self):
        self.points = self.game.player.score
        self.scoreText = self.font.render(f"{self.points}", True, (46, 34, 47))

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
        self.game.screen.blit(scoreBarScale, (scoreBar_x, self.offsetY))
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
        self.game.screen.blit(self.scoreText, scoreRect)
        self.game.screen.blit(self.multiText, multiRect)
