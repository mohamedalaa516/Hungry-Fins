class FadeOut:
    def __init__(self, surface, parentRect, anchor, offset, screen) -> None:
        self.surface = surface
        self.screen = screen
        self.parentRect = parentRect
        self.anchor = anchor
        self.offset = offset
        self.parentValue = getattr(self.parentRect, self.anchor)
        self.rect = self.surface.get_rect(
            **{
                self.anchor: (
                    self.parentValue[0] + self.offset[0],
                    self.parentValue[1] + self.offset[1],
                )
            }
        )
        self.alpha = 255

    def reset(self):
        self.alpha = 255

    def update(self):
        self.alpha = max(0, self.alpha - 5)

    def draw(self, parentRect):
        self.parentRect = parentRect
        self.parentValue = getattr(self.parentRect, self.anchor)
        self.rect = self.surface.get_rect(
            **{
                self.anchor: (
                    self.parentValue[0] + self.offset[0],
                    self.parentValue[1] + self.offset[1],
                )
            }
        )
        self.surface.set_alpha(self.alpha)
        self.screen.blit(self.surface, self.rect)
