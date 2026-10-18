from os.path import join
import pygame

sound = {}
sfx = {}


def load():
    sound.update(
        {
            "mainMenu": pygame.mixer.Sound(
                join("assets", "music", "main_menu_music.mp3")
            ),
            "chapter1": pygame.mixer.Sound(
                join("assets", "music", "background_chapter1_music.mp3")
            ),
        }
    )

    sound["mainMenu"].set_volume(0.25)
    sound["chapter1"].set_volume(0.4)

    sfx.update(
        {
            "chomp": [
                pygame.mixer.Sound(join("assets", "music", "chomp.mp3")),
                pygame.mixer.Sound(join("assets", "music", "chomp_low.mp3")),
                pygame.mixer.Sound(join("assets", "music", "chomp_high.mp3")),
            ],
            "confirm": pygame.mixer.Sound(join("assets", "music", "confirm.mp3")),
            "start": pygame.mixer.Sound(join("assets", "music", "start.mp3")),
            "die": pygame.mixer.Sound(join("assets", "music", "die.mp3")),
            "double": pygame.mixer.Sound(join("assets", "music", "power_up_sfx.mp3")),
            "triple": pygame.mixer.Sound(
                join("assets", "music", "power_up_sfx_high.mp3")
            ),
            "growth": pygame.mixer.Sound(join("assets", "music", "growth.mp3")),
            "2x": pygame.mixer.Sound(join("assets", "music", "2x.wav")),
            "3x": pygame.mixer.Sound(join("assets", "music", "3x.wav")),
        }
    )
    sfx["die"].set_volume(0.25)

    for chomp in sfx["chomp"]:
        chomp.set_volume(0.5)
