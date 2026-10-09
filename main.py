import pygame
import config
from os.path import join
from utilities.filehandler import sprite_handler
from entities import Player
from utilities.camera import Camera
from tilemap import Tiles
from utilities.particle import Particle
import random


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode(
            (config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        )
        self.gameScreen = pygame.Surface((config.GAME_WIDTH, config.GAME_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        self.loader = {
            "background": pygame.image.load(
                join("./assets", "decore", "background.png")
            ),
            "player": sprite_handler(
                join("./assets", "player", "player_medium.png"), 8
            ),
        }
        self.tilesMap = {
            "collisions": sprite_handler(
                "assets/decore/collisions.png", 4, column=True
            ),
        }

        self.player = Player(self, self.loader["player"], (100, -100))
        self.particles = []
        self.camera = Camera(config.GAME_WIDTH // 1.5, config.GAME_HEIGHT // 1.5, self)
        self.tilesMap = Tiles(self)
        try:
            self.tilesMap.load()
            print("file load successfully")
        except FileNotFoundError:
            print("file not found")

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.player.handleInput()
            rect = self.player.get_rect()

            if self.player.flip:
                pos = (rect.right, rect.centery + random.randint(-4, 4))
                speed = [random.uniform(0.5, 2), random.uniform(-0.5, 0.5)]
            else:
                pos = (rect.left, rect.centery + random.randint(-4, 4))
                speed = [-random.uniform(0.5, 2), random.uniform(-0.5, 0.5)]

            self.particles.append(
                Particle(self, (180, 220, 255), random.randint(1, 3), pos, speed)
            )
            self.player.update()
            self.camera.update()

            self.gameScreen.blit(self.loader["background"], (1, 0))

            self.player.draw()

            for particle in self.particles[:]:
                particle.update()
                if particle.alive:
                    particle.draw()
                else:
                    self.particles.remove(particle)
            # Camera view
            view = self.gameScreen.subsurface(self.camera.camera)

            # Zoom
            scaled = pygame.transform.scale(view, self.screen.get_size())

            self.screen.blit(scaled, (0, 0))

            pygame.display.flip()
            self.clock.tick(config.FRAME_RATE)


game = Game()
game.run()
