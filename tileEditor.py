import pygame
from entities import EntityPhysics
from utilities.filehandler import sprite_handler
from tilemap import Tiles
import config
from os.path import join
from dataclasses import dataclass, field
from utilities.camera import Camera


@dataclass
class Tile:
    tileSet: object
    pos: list[int] = field(default_factory=lambda: [0, 0])
    index: int = 0


if __name__ == "__main__":

    class TileEditor:
        def __init__(self):

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
            self.deleteMode = False

            self.tilesMap = {
                "collisions": sprite_handler(
                    "assets/decore/collisions.png", 4, row=False, column=True
                ),
            }
            print(self.tilesMap["collisions"])
            self.current_index_tiles = 0
            self.tilesManager = Tiles(self)
            self.tile = Tile(tileSet=self.tilesManager)

            try:
                self.tilesManager.load()
                print("file load successfully")
            except FileNotFoundError:
                print("Error: file does not exist")

            self.camera = Camera(
                config.GAME_WIDTH // 1.5, config.GAME_HEIGHT // 1.5, self
            )

        def run(self):

            while self.running:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # 400->800  , x->260
                game_x = mouse_x * config.GAME_WIDTH // config.SCREEN_WIDTH
                game_y = mouse_y * config.GAME_HEIGHT // config.SCREEN_HEIGHT
                tile_x = game_x // 16
                tile_y = game_y // 16

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == pygame.BUTTON_LEFT:
                            if tile_x == 0:
                                self.tile.index = tile_y
                        if event.button == pygame.BUTTON_RIGHT:
                            self.pos = [game_x // 16, game_y // 16]
                            if self.deleteMode:
                                for tile in self.tilesManager.outground_tiles:
                                    if tile["pos"] == self.pos:
                                        self.tilesManager.outground_tiles.remove(tile)
                                        print("yes")
                            else:
                                self.tilesManager.outground_tiles.append(
                                    {
                                        "type": f"{list(self.tilesMap)[self.current_index_tiles]}",
                                        "variation": self.tile.index,
                                        "pos": (self.pos[0], self.pos[1]),
                                    },
                                )

                        if event.button == pygame.BUTTON_WHEELUP:
                            self.current_index_tiles = (
                                self.current_index_tiles + 1
                            ) % len(list(self.tilesMap))
                        if event.button == pygame.BUTTON_WHEELDOWN:
                            self.current_index_tiles = (
                                self.current_index_tiles - 1
                            ) % len(list(self.tilesMap))

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_s:
                            self.tilesManager.save()
                            print("file save successfully")
                        if event.key == pygame.K_d:
                            self.deleteMode = True
                            print("delete mode")
                        if event.key == pygame.K_i:
                            self.deleteMode = False
                            print("insert mode")

                self.gameScreen.fill("black")

                self.gameScreen.blit(self.loader["background"], (1, 0))
                tilesDecores = self.tilesMap[
                    list(self.tilesMap)[self.current_index_tiles]
                ]
                for i, decore in enumerate(tilesDecores):
                    self.gameScreen.blit(decore, (0, i * 16))
                    pygame.draw.rect(
                        self.gameScreen, (250, 0, 0), (0, i * 16, 16, 16), 1
                    )

                preview = self.tilesMap[list(self.tilesMap)[self.current_index_tiles]][
                    self.tile.index
                ].copy()
                preview.set_alpha(100)
                self.gameScreen.blit(preview, (tile_x * 16, tile_y * 16))
                self.tilesManager.draw(tileEditor=True)
                scaled_surface = pygame.transform.scale(
                    self.gameScreen, (config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
                )
                self.screen.blit(scaled_surface, (0, 0))
                pygame.display.flip()
                self.clock.tick(60)


game = TileEditor()
game.run()
