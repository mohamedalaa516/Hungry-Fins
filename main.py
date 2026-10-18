from paths import resource_path, save_path
from utilities.ui_helper import scaleImage
from utilities.transition import Transition
from spawners.particle_spawaner import spawnParticle
from spawners.enemy_spawaner import createEnemies, choiceTypeFish
from result_ui import ResultScreen
from score_ui import Score
from growth_ui import Growth
from tilemap import Tiles
from utilities.camera import Camera
from utilities import transition
from player import Player
import config
import pygame
from save_ui import SaveSlots
import json
from main_ui import MainMenu
import sys
import traceback
from pathlib import Path


def log_exception(exc_type, exc_value, exc_traceback):
    log_path = Path.home() / "HungryFins_error.log"

    with open(log_path, "w", encoding="utf-8") as file:
        traceback.print_exception(exc_type, exc_value, exc_traceback, file=file)


sys.excepthook = log_exception


class Game:
    def __init__(self, screen, currentSlot) -> None:
        self.screen = screen
        self.currentSlot = currentSlot
        self.gameScreen = pygame.Surface((config.GAME_WIDTH, config.GAME_HEIGHT))
        self.clock = pygame.time.Clock()
        self.end = False
        self.running = True

        import loaderTexture
        import loaderMusic

        loaderMusic.load()

        self.loader = loaderTexture.loader
        self.ui_loader = loaderTexture.ui_loader
        self.music_loader = loaderMusic

        self.loadSlots()
        self.sessionStartTime = pygame.time.get_ticks()

        # Load level JSON
        try:
            with open(
                resource_path("levels", f"level{self.currentLevel}.json"),
                "r",
                encoding="utf-8",
            ) as file:
                self.levelConfig = json.load(file)

        except FileNotFoundError:
            print("level not found")
            return

        self.loadLevel()
        self.player.score = self.currentScore
        self.timeEnemy = 0.0

        self.transition = Transition(
            self.gameScreen,
            0,
            backWord=True,
            upWord=False,
        )

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                self.resultScreen.handleInput(event)

            if self.end:
                self.endLevel()
                return

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
                self.player.multiplierPointRange = 0
                self.backgroundMusic.stop()
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
                self.gameScreen.blit(
                    self.resultScreen.overlay,
                    (0, 0),
                )

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

    def getPlayTime(self):
        currentSession = (pygame.time.get_ticks() - self.sessionStartTime) // 1000

        return self.playTime + currentSession

    def formatPlayTime(self, seconds):
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        remainingSeconds = seconds % 60

        return f"{hours:02}:{minutes:02}:{remainingSeconds:02}"

    def get_completion(self, totalLevel, currentLevel):
        return ((currentLevel - 1) / totalLevel) * 100

    def loadSlots(self):
        try:
            with open(
                save_path(self.currentSlot),
                "r",
                encoding="utf-8",
            ) as file:
                slot = json.load(file)

            self.currentLevel = slot.get("currentLevel", 1)
            self.currentScore = slot.get("score", 0)
            self.completedLevels = slot.get("completedLevels", 0)
            self.playTime = slot.get("playTime", 0)
            self.completion = slot.get("completion", 0)

        except FileNotFoundError:
            print("slot not found")
            self.currentLevel = 1
            self.currentScore = 0
            self.completedLevels = 0
            self.playTime = 0
            self.completion = 0

    def saveSlots(self):
        playTime = self.getPlayTime()

        data = {
            "id": self.currentSlot,
            "currentLevel": self.currentLevel,
            "completedLevels": self.completedLevels,
            "score": self.player.score,
            "playTime": playTime,
            "playTimeFormat": self.formatPlayTime(playTime),
            "completion": self.get_completion(5, self.currentLevel),
        }

        with open(
            save_path(self.currentSlot),
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(data, file, indent=4)

    def loadLevel(self):
        if self.end:
            return

        self.player = Player(
            self,
            self.loader[f"player/{config.PLAYER_TYPE}/idle"],
            config.PLAYER_START_POS,
            config.PLAYER_LEVELS[config.PLAYER_TYPE],
            self.levelConfig["growthMeter"],
        )

        self.player.score = self.currentScore
        print(self.player.score, self.currentScore)

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

        self.resultScreen = ResultScreen(
            self,
            ["score", "numberOfEating"],
        )

        self.backgroundMusic = self.music_loader.sound["chapter1"]
        self.backgroundMusic.play(loops=True)

        try:
            self.tilesMap.load()
            print("File loaded successfully")
        except FileNotFoundError:
            print("File not found")

    def restart(self):
        self.timeEnemy = 0.0
        self.loadLevel()
        print("Game restarted!")

    def endLevel(self):
        endSurface = pygame.transform.scale(
            self.loader["endLevel"],
            self.screen.get_size(),
        )

        self.screen.blit(endSurface, (0, 0))
        pygame.display.flip()

        waiting = True

        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False

            self.clock.tick(config.FRAME_RATE)

    def nextLevel(self):
        currentScore = self.player.score
        nextLevel = self.currentLevel + 1

        if nextLevel == 5:
            self.end = True
            return

        nextLevelPath = resource_path("levels", f"level{nextLevel}.json")

        try:
            with open(
                nextLevelPath,
                "r",
                encoding="utf-8",
            ) as file:
                nextLevelConfig = json.load(file)

        except FileNotFoundError:
            print("level not found")
            return

        self.currentLevel = nextLevel
        self.levelConfig = nextLevelConfig
        self.currentScore = currentScore

        self.loadLevel()
        self.timeEnemy = 0.0

        self.transition = Transition(
            self.gameScreen,
            0,
            backWord=True,
            upWord=False,
        )

        self.saveSlots()

    def hasNextLevel(self):
        nextLevelPath = resource_path(
            "levels",
            f"level{self.currentLevel + 1}.json",
        )

        return nextLevelPath.exists()


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption(config.WINDOW_TITLE)

    screen = pygame.display.set_mode(
        (config.SCREEN_WIDTH, config.SCREEN_HEIGHT),
        flags=pygame.FULLSCREEN | pygame.SCALED,
    )

    print("1. Starting MainMenu")
    menu = MainMenu(screen)
    menu.run()

    print("2. MainMenu closed:", menu.nextScreen)

    if menu.nextScreen == "save_slots":
        print("3. Starting SaveSlots")

        saveslots = SaveSlots(screen)
        saveslots.run()

        print("4. SaveSlots closed:", saveslots.nextScreen)

        if saveslots.nextScreen == "Game":
            print("5. Starting Game")
            Game(screen, saveslots.currentSlot).run()

    print("6. Program finished")
