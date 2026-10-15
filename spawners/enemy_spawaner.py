import config
from entities import Enemy
import random


def choiceTypeFish(game):
    count = {}
    for enemy in game.levelConfig["typeEnemies"]:
        count.update({enemy: 0})

    for enemy in game.enemies:
        if enemy.alive:
            count[enemy.type] += 1
    if sum(count.values()) >= game.levelConfig["max_enemies"]:
        return None
    limits = {
        "smallFish": game.levelConfig["max_small_fish"],
        "normalFish": game.levelConfig["max_normal_fish"],
        "swordFish": game.levelConfig["max_sword_fish"],
    }

    allowed = []

    for fishType in game.levelConfig["typeEnemies"]:
        if count[fishType] >= limits[fishType]:
            continue
        else:
            allowed.append(fishType)

    if not allowed:
        return
    weights = {
        "smallFish": game.levelConfig["SMALL_FISH_WEIGHT"],
        "normalFish": game.levelConfig["NORMAL_FISH_WEIGHT"],
        "swordFish": game.levelConfig["LARGE_FISH_WEIGHT"],
    }

    return random.choices(
        allowed,
        weights=[weights[fishType] for fishType in allowed],
        k=1,
    )[0]


def createEnemies(game, fishType):
    game.enemies.append(
        Enemy(
            game,
            game.loader[f"{fishType}/idle"],
            (
                random.choice(
                    [
                        -50,
                        config.GAME_WIDTH + config.ENEMY_SPAWN_X_OFFSET,
                    ]
                ),
                random.randint(
                    80,
                    config.ENEMY_SPAWN_Y_MAX,
                ),
            ),
            level=config.FISH_LEVELS[fishType],
            type=fishType,
        )
    )
