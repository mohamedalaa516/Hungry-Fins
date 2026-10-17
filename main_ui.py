import pygame
import config
from utilities import animation
from utilities.animation import Animation
from utilities.transition import Transition


class MainMenu:
    def __init__(self, screen) -> None:
        self.gameScreen = pygame.Surface((config.GAME_WIDTH, config.GAME_HEIGHT))
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.nextScreen = None

        from loaderTexture import ui_loader
        import loaderMusic

        loaderMusic.load()

        self.music_loader = loaderMusic
        self.ui_loader = ui_loader
        # layer 1 image
        self.imageLayer1 = self.ui_loader["mainUi/layer1"]
        self.imageLayerRect1 = self.imageLayer1.get_rect(
            bottom=self.gameScreen.get_rect().bottom
        )
        self.imageLayerRect2 = self.imageLayerRect1.copy()
        self.imageLayerRect2.left = self.imageLayerRect1.right

        # layer 2 image

        self.animationLayer = Animation(
            1, self.ui_loader["mainUi/layer2"], 0.2, loop=True
        )
        self.imageLayer2 = self.animationLayer.getImage()

        self.animationTitle = Animation(
            1, self.ui_loader["mainUi/title/idle"], 0.2, loop=True
        )
        # title
        self.title = self.animationTitle.getImage()
        self.titleClicked = False
        self.startGame = False

        self.transition = Transition(self.gameScreen, 320)
        self.background_sound = self.music_loader.sound["mainMenu"]
        self.background_sound.play(loops=True)

        self.start = self.music_loader.sfx["start"]

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and not self.titleClicked:
                        self.start.play()
                        self.titleClicked = True
                        self.animationTitle = Animation(
                            1, self.ui_loader["mainUi/title/click"], 0.2, loop=False
                        )

            self.gameScreen.fill((0, 0, 0))  # Clear previous frame
            if self.titleClicked:
                self.transition.update()
            self.animationLayer.update()
            self.animationTitle.update()
            self.imageLayer2 = self.animationLayer.getImage()
            self.title = self.animationTitle.getImage()
            self.updateLayer()
            self.exit()

            self.gameScreen.blit(self.imageLayer2, (0, 0))
            self.gameScreen.blit(self.imageLayer1, self.imageLayerRect1)
            self.gameScreen.blit(self.imageLayer1, self.imageLayerRect2)
            self.gameScreen.blit(
                self.title,
                (
                    (self.gameScreen.get_width() - self.title.get_width()) // 2,
                    (self.gameScreen.get_height() - self.title.get_height()) // 2,
                ),
            )

            self.transition.draw()
            scaled = pygame.transform.scale(
                self.gameScreen,
                self.screen.get_size(),
            )

            self.screen.blit(scaled, (0, 0))

            pygame.display.flip()
            if config.DEBUG:
                print(self.clock.get_fps())
            self.clock.tick(config.FRAME_RATE)

    def updateLayer(self):
        # layer 1
        self.imageLayerRect1.x += 1
        self.imageLayerRect2.x += 1
        if self.imageLayerRect1.left >= self.gameScreen.get_width():
            self.imageLayerRect1.right = self.imageLayerRect2.left
        if self.imageLayerRect2.left >= self.gameScreen.get_width():
            self.imageLayerRect2.right = self.imageLayerRect1.left

    def exit(self):
        if (
            self.animationTitle.finished
            and self.transition.radius <= 0
            and self.titleClicked
        ):
            self.nextScreen = "save_slots"
            self.running = False
            self.background_sound.stop()
