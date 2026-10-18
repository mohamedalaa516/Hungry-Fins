import os
import sys
import pygame
from os.path import join

BASE_DIR = getattr(
    sys,
    "_MEIPASS",
    os.path.dirname(os.path.abspath(__file__)),
)


def asset_path(*parts):
    return join(BASE_DIR, "assets", *parts)


sound = {}
sfx = {}


def load():
    sound.update(
        {
            "mainMenu": pygame.mixer.Sound(asset_path("music", "main_menu_music.mp3")),
            "chapter1": pygame.mixer.Sound(
                asset_path("music", "background_chapter1_music.mp3")
            ),
        }
    )

    sound["mainMenu"].set_volume(0.25)
    sound["chapter1"].set_volume(0.4)

    sfx.update(
        {
            "chomp": [
                pygame.mixer.Sound(asset_path("music", "chomp.mp3")),
                pygame.mixer.Sound(asset_path("music", "chomp_low.mp3")),
                pygame.mixer.Sound(asset_path("music", "chomp_high.mp3")),
            ],
            "confirm": pygame.mixer.Sound(asset_path("music", "confirm.mp3")),
            "start": pygame.mixer.Sound(asset_path("music", "start.mp3")),
            "die": pygame.mixer.Sound(asset_path("music", "die.mp3")),
            "double": pygame.mixer.Sound(asset_path("music", "power_up_sfx.mp3")),
            "triple": pygame.mixer.Sound(asset_path("music", "power_up_sfx_high.mp3")),
            "growth": pygame.mixer.Sound(asset_path("music", "growth.mp3")),
            "2x": pygame.mixer.Sound(asset_path("music", "2x.wav")),
            "3x": pygame.mixer.Sound(asset_path("music", "3x.wav")),
        }
    )

    sfx["die"].set_volume(0.25)

    for chomp in sfx["chomp"]:
        chomp.set_volume(0.5)
