import pygame
import json


class Tiles:
    def __init__(self, game):
        self.outground_tiles = [
            # {"type": "decorations", "variation": 1, "pos": (100, 50)},
        ]
        self.game = game

    def save(self, filename="map.json"):
        with open(filename, "w") as file:
            json.dump(self.outground_tiles, file, indent=4)

    def load(self, filename="map.json"):
        with open(filename, "r") as file:
            self.outground_tiles = json.load(file)

    def draw(self, tileEditor=False):
        for tile in self.outground_tiles:
            surface = self.game.tilesMap[tile["type"]][tile["variation"]]
            if tileEditor:
                surface = surface.copy()
                if (
                    tile["type"]
                    != list(self.game.tilesMap)[self.game.current_index_tiles]
                ):
                    surface.set_alpha(100)
                self.game.gameScreen.blit(
                    surface, (tile["pos"][0] * 16, tile["pos"][1] * 16)
                )

    def get_collisions(self):
        collisions = []

        for tile in self.outground_tiles:
            if tile["type"] == "collisions":
                x = tile["pos"][0] * 16
                y = tile["pos"][1] * 16

                collisions.append(pygame.Rect(x, y, 16, 16))

        return collisions
