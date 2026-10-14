import config
from os.path import join
from utilities.filehandler import sprite_handler
import pygame

loader = {
    "background": pygame.image.load(join("./assets", "decore", "background.png")),
    "blood": sprite_handler(
        join("./assets", "Bloodybite.png"), 4, column=False, row=True
    ),
    "player/medium/idle": sprite_handler(
        join("./assets", "player", "player_medium_idle.png"),
        config.PLAYER_ANIMATION_SIZE,
    ),
    "player/medium/attack": sprite_handler(
        join("./assets", "player", "player_medium_attack.png"),
        config.PLAYER_ANIMATION_SIZE,
    ),
    "player/small/idle": sprite_handler(
        join("./assets", "player", "player_small_idle.png"),
        config.PLAYER_ANIMATION_SIZE,
    ),
    "player/small/attack": sprite_handler(
        join("./assets", "player", "player_small_attack.png"),
        config.PLAYER_ANIMATION_SIZE,
    ),
    "player/large/idle": sprite_handler(
        join("./assets", "player", "player_large_idle.png"),
        config.PLAYER_ANIMATION_SIZE,
    ),
    "player/large/attack": sprite_handler(
        join("./assets", "player", "player_large_attack.png"),
        config.PLAYER_ANIMATION_SIZE,
    ),
    "normalFish/idle": sprite_handler(
        join("./assets", "enemy", "normal_fish_idle.png"),
        config.ENEMY_ANIMATION_SIZE,
    ),
    "smallFish/idle": sprite_handler(
        join("./assets", "enemy", "small_fish.png"),
        config.ENEMY_ANIMATION_SIZE,
    ),
    "swordFish/idle": sprite_handler(
        join("./assets", "enemy", "sword_fish_idle.png"),
        config.ENEMY_ANIMATION_SIZE,
    ),
    "normalFish/attack": sprite_handler(
        join("./assets", "enemy", "normal_fish_attack.png"),
        config.ENEMY_ANIMATION_SIZE,
    ),
    "swordFish/attack": sprite_handler(
        join("./assets", "enemy", "sword_fish_attack.png"),
        config.ENEMY_ANIMATION_SIZE,
    ),
}

ui_loader = {
    "growthBar": pygame.image.load(join("assets", "Ui", "growthBar_empty.png")),
    "growthBar/progress": pygame.image.load(
        join("assets", "Ui", "growthBar_progress.png")
    ),
    "growthBar/normalFish": pygame.image.load(
        join("assets", "Ui", "growthBar_NormalFish.png")
    ),
    "growthBar/swordFish": pygame.image.load(
        join("assets", "Ui", "growthBar_swordFish.png")
    ),
    "scoreBar": pygame.image.load(join("assets", "Ui", "score.png")),
    "scoreBar/multi": pygame.image.load(join("assets", "Ui", "score_multi.png")),
}
