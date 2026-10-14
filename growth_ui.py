import pygame
from utilities.ui_helper import scaleImage


class Growth:
    def __init__(self, game, numberOfBars, fishs) -> None:
        self.game = game
        self.numberOfBars = numberOfBars
        self.progressMap = {}
        self.fishs = fishs

    def update(self):
        sizeToGrowth = self.game.player.sizeToGrow
        numberOfEating = self.game.player.numberOfEating

        if numberOfEating < sizeToGrowth[0]:
            self.progressMap = {
                0: numberOfEating / sizeToGrowth[0],
                1: 0,
                2: 0,
            }

        elif numberOfEating < sizeToGrowth[1]:
            self.progressMap = {
                0: 1,
                1: (numberOfEating - sizeToGrowth[0])
                / (sizeToGrowth[1] - sizeToGrowth[0]),
                2: 0,
            }

        else:
            self.progressMap = {
                0: 1,
                1: 1,
                2: 1,
            }

    def draw(self):
        bar = self.game.ui_loader["growthBar"]
        progress = self.game.ui_loader["growthBar/progress"]
        scaledBar = scaleImage(bar)
        scaledProgress = scaleImage(progress)
        scaledFishs = [scaleImage(fish) for fish in self.fishs]

        for i in range(self.numberOfBars):
            x = i * scaledBar.get_width()
            progressHeight = int(scaledProgress.get_height() * self.progressMap[i])

            self.game.screen.blit(scaledBar, (x, 0))

            if progressHeight > 0:
                croppedProgress = scaledProgress.subsurface(
                    (
                        0,
                        scaledProgress.get_height() - progressHeight,
                        scaledProgress.get_width(),
                        progressHeight,
                    )
                )
                progressX = self.posImageRlationToBar(x, scaledBar, scaledProgress)
                progressY = (
                    self.posImageRlationToBar(
                        x, scaledBar, scaledProgress, x=False, y=True
                    )
                    + scaledProgress.get_height()
                    - progressHeight
                )

                self.game.screen.blit(croppedProgress, (progressX, progressY))
            fishX = self.posImageRlationToBar(x, scaledBar, scaledFishs[i])
            fishY = self.posImageRlationToBar(
                x, scaledBar, scaledFishs[i], x=False, y=True
            )

            self.game.screen.blit(scaledFishs[i], (fishX, fishY))

    def posImageRlationToBar(self, barX, scaledBar, image, x=True, y=False):
        if x:
            return barX + (scaledBar.get_width() - image.get_width()) // 2
        else:
            return (scaledBar.get_height() - image.get_height()) // 2
