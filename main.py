import json
from main_ui import MainMenu
import pygame
import config
from os.path import join
from entities import Player
from utilities import transition
from utilities.camera import Camera
from tilemap import Tiles
from growth_ui import Growth
from score_ui import Score
from result_ui import ResultScreen
from spawners.enemy_spawaner import createEnemies, choiceTypeFish
from spawners.particle_spawaner import spawnParticle
from utilities.transition import Transition


class Game:
    def __init__(self, screen) -> None:
        self.screen = screen
        self.gameScreen = pygame.Surface((config.GAME_WIDTH, config.GAME_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        import loaderTexture

        self.loader = loaderTexture.loader
        self.ui_loader = loaderTexture.ui_loader

        # load levels json
        with open(join("levels", "level2.json"), "r") as file:
            self.levelConfig = json.load(file)
        self.loadLevel()
        self.timeEnemy = 0.0

        self.transition = Transition(self.gameScreen, 0, backWord=True, upWord=False)

    def loadLevel(self):
        self.player = Player(
            self,
            self.loader[f"player/{config.PLAYER_TYPE}/idle"],
            config.PLAYER_START_POS,
            config.PLAYER_LEVELS[config.PLAYER_TYPE],
            self.levelConfig["growthMeter"],
        )
        self.win = False
        self.reservationSet = set()
        self.enemies = []

        self.particles = []

        self.camera = Camera(
            config.GAME_WIDTH // config.CAMERA_ZOOM,
            config.GAME_HEIGHT // config.CAMERA_ZOOM,
            self,
        )
        self.tilesMap = Tiles(self)
        self.growth = Growth(
            self,
            self.levelConfig["growthInterval"],
            [
                self.ui_loader[f"growthBar/{self.levelConfig['typeEnemies'][1]}"],
                self.ui_loader[f"growthBar/{self.levelConfig['typeEnemies'][2]}"],
                self.ui_loader["growthBar/win"],
            ],
        )
        self.score = Score(self)
        self.resultScreen = ResultScreen(self, ["score", "numberOfEating"])

        try:
            self.tilesMap.load()
            print("File loaded successfully")
        except FileNotFoundError:
            print("File not found")

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.resultScreen.handleInput(event)

            self.player.handleInput()
            if self.player.alive:
                spawnParticle(self, self.player, self.particles)

            self.timeEnemy += 1

            if self.timeEnemy >= self.levelConfig["spawnInterval"]:
                fishType = choiceTypeFish(self)
                if fishType is not None:
                    createEnemies(self, fishType)
                    self.timeEnemy = 0

            self.transition.update()
            self.camera.update()
            self.growth.update()
            self.score.update()
            if self.win or self.player.health <= 0:
                self.resultScreen.visible = True
            else:
                self.player.update()

            self.resultScreen.update()

            self.gameScreen.blit(
                self.loader["background"],
                (0, 0),
            )

            self.transition.draw()
            self.player.draw()

            for enemy in self.enemies[:]:
                enemy.update()

                if enemy.alive:
                    spawnParticle(self, enemy, self.particles)
                    enemy.draw()
                else:
                    self.enemies.remove(enemy)

            for particle in self.particles[:]:
                particle.update()

                if particle.alive:
                    particle.draw()
                else:
                    self.particles.remove(particle)

            view = self.gameScreen.subsurface(self.camera.camera)
            if self.resultScreen.visible:
                self.gameScreen.blit(self.resultScreen.overlay, (0, 0))

            scaled = pygame.transform.scale(
                view,
                self.screen.get_size(),
            )

            self.screen.blit(scaled, (0, 0))

            self.growth.draw()
            self.score.draw()
            self.resultScreen.draw()
            pygame.display.flip()
            if config.DEBUG:
                print(self.clock.get_fps())
            self.clock.tick(config.FRAME_RATE)

        pygame.quit()

    def restart(self):
        self.timeEnemy = 0.0
        self.loadLevel()
        print("Game restarted!")


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption(config.WINDOW_TITLE)
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    menu = MainMenu(screen)
    menu.run()

    if menu.startGame:
        Game(screen).run()
