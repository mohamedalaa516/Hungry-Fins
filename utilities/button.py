import pygame
from os.path import join
from utilities.ui_helper import scaleImage


class Button:
    def __init__(
        self,
        screen,
        surface,
        clickedSurface,
        text,
        parent_rect,
        anchor,
        offset,
        scale=3,
        fontSize=34,
        color=(247, 150, 23),
    ):
        self.screen = screen
        self.scale = scale
        self.clickedSurface = scaleImage(clickedSurface, scale=scale)
        self.mainSurface = scaleImage(surface, scale=scale)
        self.surface = self.mainSurface
        self.text = text
        self.parent_rect = parent_rect
        self.anchor = anchor

        self.color = color
        self.fontSize = fontSize
        self.font = pygame.font.Font(join("assets", "Fonts", "yoster.ttf"), fontSize)
        self.render_text = self.font.render(self.text, True, self.color)

        self.rect = self.surface.get_rect()
        self.offset = offset
        self.pressed = False

    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos) and event.button == pygame.BUTTON_LEFT:
                self.pressed = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == pygame.BUTTON_LEFT:
                wasPressed = self.pressed
                self.pressed = False

            if wasPressed and self.rect.collidepoint(event.pos):
                return True
        return False

    def draw(self):
        parent_pos = getattr(self.parent_rect, self.anchor)

        setattr(
            self.rect,
            self.anchor,
            (
                parent_pos[0] + self.offset[0],
                parent_pos[1] + self.offset[1],
            ),
        )

        self.surface = self.clickedSurface if self.pressed else self.mainSurface
        text_rect = self.render_text.get_rect(center=self.rect.center)

        self.screen.blit(self.surface, self.rect)
        self.screen.blit(self.render_text, text_rect)


class CustomButton(Button):
    def __init__(
        self,
        screen,
        surface,
        clickedSurface,
        text,
        parent_rect,
        anchor,
        offset,
        number,
        playTime,
        completion,
        scale=3,
        fontSize=34,
        color=(247, 150, 23),
    ):
        super().__init__(
            screen,
            surface,
            clickedSurface,
            text,
            parent_rect,
            anchor,
            offset,
            scale,
            fontSize,
            color,
        )

        self.font = pygame.font.Font(None, fontSize)
        self.number = str(number)
        self.playTime = str(playTime)
        self.completion = str(completion)

        self.extraTexts = [
            (self.number, "topleft", (10, 10)),
            (self.playTime, "bottomleft", (10, -10)),
            (self.completion, "bottomright", (-10, -10)),
        ]

    def drawExtraText(self, text, anchor, offset):
        renderedText = self.font.render(text, True, self.color)

        textRect = renderedText.get_rect()
        setattr(
            textRect,
            anchor,
            (
                getattr(self.rect, anchor)[0] + offset[0],
                getattr(self.rect, anchor)[1] + offset[1],
            ),
        )

        self.screen.blit(renderedText, textRect)

    def draw(self):
        super().draw()

        self.extraTexts = [
            (self.number, "topleft", (10, 10)),
            (self.playTime, "bottomleft", (10, -10)),
            (self.completion, "bottomright", (-10, -10)),
        ]

        for text, anchor, offset in self.extraTexts:
            self.drawExtraText(text, anchor, offset)
