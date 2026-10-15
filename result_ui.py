import pygame
from os.path import join
from utilities.ui_helper import scaleImage
from utilities.button import Button


class ResultScreen:
    def __init__(self, game, items):
        self.game = game
        self.visible = False
        self.items = items

        self.overlay = pygame.Surface(
            self.game.screen.get_size(),
            pygame.SRCALPHA,
        )
        self.overlay.fill((0, 0, 0, 160))

        self.fontMinSize = 34
        self.fontSize = 120
        self.currentItemIndex = 0

        self.fontString = pygame.font.Font(
            join("assets", "Fonts", "yoster.ttf"), self.fontMinSize
        )
        self.fontNumber = pygame.font.Font(
            join("assets", "Fonts", "yoster.ttf"), self.fontSize
        )

        self.text_color = (46, 34, 47)
        self.result_image = scaleImage(self.game.ui_loader["result"], scale=3)
        self.component_image = scaleImage(
            self.game.ui_loader["result/component"], scale=3
        )

        self.resultX = (
            self.game.screen.get_width() - self.result_image.get_width()
        ) // 2
        self.resultY = (
            self.game.screen.get_height() - self.result_image.get_height()
        ) // 2
        self.result_rect = self.result_image.get_rect(
            topleft=(self.resultX, self.resultY)
        )
        self.button = Button(
            self.game.screen,
            self.game.ui_loader["button/small"],
            self.game.ui_loader["button/small/clicked"],
            "retry",
            self.result_rect,
            "bottomleft",
            [15, -55],
        )
        self.buttonPressed = False

    def update(self):
        if self.visible:
            if self.fontSize > self.fontMinSize:
                self.fontSize -= 3

            else:
                self.currentItemIndex = min(self.currentItemIndex + 1, len(self.items))
                if self.currentItemIndex <= len(self.items) - 1:
                    self.fontSize = 100
            self.fontNumber = pygame.font.Font(
                join("assets", "Fonts", "yoster.ttf"), self.fontSize
            )

    def handleInput(self, event):
        if not self.visible:
            return
        if self.button.handle_input(event):
            print("Retry action!")
            self.game.restart()

    def draw(self):
        if not self.visible:
            return

        self.game.screen.blit(self.result_image, self.result_rect)
        self.button.draw()
        for i, item in enumerate(self.items):
            if i > self.currentItemIndex:
                continue
            if item != "numberOfEating":
                itemText = self.fontString.render(item, True, self.text_color)
            else:
                itemText = self.fontString.render("fishEaten", True, self.text_color)
            self.value = getattr(self.game.player, item)

            if i == self.currentItemIndex:
                itemNumber = self.fontNumber.render(
                    str(self.value), True, self.text_color
                )
            else:
                itemNumber = self.fontString.render(
                    str(self.value), True, self.text_color
                )
            componentX = self.resultX + 30
            componentY = (
                self.resultY + 60 + i * (self.component_image.get_height() + 10)
            )

            self.game.screen.blit(self.component_image, (componentX, componentY))
            numberRect = itemNumber.get_rect(
                center=(
                    componentX + self.component_image.get_width() // 2,
                    componentY + self.component_image.get_height() // 2,
                )
            )
            self.game.screen.blit(itemNumber, numberRect)

            textRect = itemText.get_rect(
                midleft=(
                    componentX + self.component_image.get_width() + 10,
                    componentY + self.component_image.get_height() // 2,
                )
            )
            self.game.screen.blit(itemText, textRect)
