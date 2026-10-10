import pygame
import config
from os.path import join
from utilities.filehandler import sprite_handler
from entities import Player, Enemy
from utilities.camera import Camera
from tilemap import Tiles
from utilities.particle import Particle
import random


class Game:
    def __init__(self) -> None:
        pygame.init()

        pygame.display.set_caption(config.WINDOW_TITLE)

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
                join("./assets", "player", "player_medium.png"),
                config.PLAYER_ANIMATION_SPEED,
            ),
            "normalFish": sprite_handler(
                join("./assets", "enemy", "normal_fish.png"),
                config.ENEMY_ANIMATION_SPEED,
            ),
            "smallFish": sprite_handler(
                join("./assets", "enemy", "small_fish.png"),
                4,
            ),
            "largeFish": sprite_handler(
                join("./assets", "enemy", "sword_fish.png"),
                config.ENEMY_ANIMATION_SPEED,
            ),
        }

        self.player = Player(
            self,
            self.loader["player"],
            config.PLAYER_START_POS,
        )

        self.enemies = []
        self.timeEnemy = 0
        self.timeRepwanEnemy = 50

        self.particles = []

        self.camera = Camera(
            config.GAME_WIDTH // config.CAMERA_ZOOM,
            config.GAME_HEIGHT // config.CAMERA_ZOOM,
            self,
        )

        self.tilesMap = Tiles(self)

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

            self.player.handleInput()

            self.spawnParticle(self.player)

            self.timeEnemy += 1

            if self.timeEnemy >= self.timeRepwanEnemy:
                fishType = random.choices(
                    ["smallFish", "normalFish", "largeFish"],
                    weights=[
                        config.SMALL_FISH_WEIGHT,
                        config.NORMAL_FISH_WEIGHT,
                        config.LARGE_FISH_WEIGHT,
                    ],
                    k=1,
                )[0]

                self.enemies.append(
                    Enemy(
                        self,
                        self.loader[fishType],
                        (
                            random.choice(
                                [
                                    0,
                                    config.GAME_WIDTH + config.ENEMY_SPAWN_X_OFFSET,
                                ]
                            ),
                            random.randint(
                                80,
                                config.ENEMY_SPAWN_Y_MAX,
                            ),
                        ),
                    )
                )

                self.timeEnemy = 0

            self.player.update()
            self.camera.update()

            self.gameScreen.blit(
                self.loader["background"],
                (0, 0),
            )

            self.player.draw()

            for enemy in self.enemies[:]:
                enemy.update()

                if enemy.alive:
                    self.spawnParticle(enemy)
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

            scaled = pygame.transform.scale(
                view,
                self.screen.get_size(),
            )

            self.screen.blit(scaled, (0, 0))

            pygame.display.flip()
            self.clock.tick(config.FRAME_RATE)

        pygame.quit()

    def spawnParticle(self, entity):
        rect = entity.get_rect()

        if entity.flip:
            pos = (
                rect.right,
                rect.centery
                + random.randint(
                    -config.PARTICLE_OFFSET_Y,
                    config.PARTICLE_OFFSET_Y,
                ),
            )
            speed = [
                random.uniform(
                    config.PARTICLE_SPEED_MIN,
                    config.PARTICLE_SPEED_MAX,
                ),
                random.uniform(
                    -config.PARTICLE_VERTICAL_SPEED,
                    config.PARTICLE_VERTICAL_SPEED,
                ),
            ]
        else:
            pos = (
                rect.left,
                rect.centery
                + random.randint(
                    -config.PARTICLE_OFFSET_Y,
                    config.PARTICLE_OFFSET_Y,
                ),
            )
            speed = [
                -random.uniform(
                    config.PARTICLE_SPEED_MIN,
                    config.PARTICLE_SPEED_MAX,
                ),
                random.uniform(
                    -config.PARTICLE_VERTICAL_SPEED,
                    config.PARTICLE_VERTICAL_SPEED,
                ),
            ]

        self.particles.append(
            Particle(
                self,
                config.PARTICLE_COLOR,
                random.randint(
                    config.PARTICLE_MIN_SIZE,
                    config.PARTICLE_MAX_SIZE,
                ),
                pos,
                speed,
            )
        )


game = Game()
game.run()
