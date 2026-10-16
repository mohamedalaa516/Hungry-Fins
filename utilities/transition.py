import pygame


class Transition:
    def __init__(self, screen, radius, backWord=False, upWord=True) -> None:
        self.screen = screen
        self.radius = radius
        self.overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 255))  # أسود بشفافية جزئية
        self.backWord = backWord
        self.upWord = upWord

    def update(self):
        if self.upWord:
            self.radius = max(self.radius - 4, 0)
        if self.backWord:
            self.radius = min(self.radius + 4, 300)

    def draw(self):
        self.overlay.fill((0, 0, 0, 255))  # أسود بشفافية جزئية
        pygame.draw.circle(
            self.overlay,
            (0, 0, 0, 0),
            (self.screen.get_width() // 2, self.screen.get_height() // 2),
            self.radius,
        )
        self.screen.blit(self.overlay, (0, 0))
