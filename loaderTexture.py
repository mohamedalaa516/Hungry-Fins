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
    "player/medium/powerUp": sprite_handler(
        join("./assets", "player", "player_medium_powerUp.png"),
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
    "player/large/powerUp": sprite_handler(
        join("./assets", "player", "player_large_powerUp.png"),
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
    "growthBar/progress/full": pygame.image.load(
        join("assets", "Ui", "growthBar_progress_full.png")
    ),
    "growthBar/normalFish": pygame.image.load(
        join("assets", "Ui", "growthBar_NormalFish.png")
    ),
    "growthBar/swordFish": pygame.image.load(
        join("assets", "Ui", "growthBar_swordFish.png")
    ),
    "growthBar/win": pygame.image.load(join("assets", "Ui", "growthBar_win.png")),
    "scoreBar": pygame.image.load(join("assets", "Ui", "score.png")),
    "scoreBar/multi": pygame.image.load(join("assets", "Ui", "score_multi.png")),
    "result": pygame.image.load(join("assets", "Ui", "result.png")),
    "result/component": pygame.image.load(join("assets", "Ui", "result_score.png")),
    "button/small": pygame.image.load(join("assets", "Ui", "button_small.png")),
    "button/small/clicked": pygame.image.load(
        join("assets", "Ui", "button_small_clicked.png")
    ),
    "healthBar": pygame.image.load(join("assets", "Ui", "healthBar.png")),
    "healthBar/full": pygame.image.load(
        join("assets", "Ui", "healthBar_heart_full.png")
    ),
    "healthBar/empty": pygame.image.load(
        join("assets", "Ui", "healthBar_heart_empty.png")
    ),
    "mainUi/layer1": pygame.image.load(join("assets", "Ui", "main_layer_1.png")),
    "mainUi/layer2": sprite_handler(
        join("assets", "Ui", "main_layer_2.png"), 7, column=False, row=True
    ),
    "mainUi/title/idle": sprite_handler(join("assets", "Ui", "main_title_idle.png"), 6),
    "mainUi/title/click": sprite_handler(
        join("assets", "Ui", "main_title_click.png"), 6
    ),
    "buttonSave": pygame.image.load(join("assets", "Ui", "buttonSave.png")),
    "buttonSave2": pygame.image.load(join("assets", "Ui", "buttonSave2.png")),
    "buttonSave/idle": pygame.image.load(join("assets", "Ui", "buttonSave_idle.png")),
    "buttonSave/click": pygame.image.load(join("assets", "Ui", "buttonSave_click.png")),
    "double": pygame.image.load(join("assets", "Ui", "double.png")),
    "triple": pygame.image.load(join("assets", "Ui", "triple.png")),
    "mouse": pygame.image.load(join("assets", "Ui", "mouse_cursor.png")),
    "fins/1x": pygame.image.load(join("assets", "Ui", "fins_1x.png")),
    "fins/2x": pygame.image.load(join("assets", "Ui", "fins_2x.png")),
    "fins/3x": pygame.image.load(join("assets", "Ui", "fins_3x.png")),
}
