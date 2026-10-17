import json
from main_ui import MainMenu
from save_ui import SaveSlots
import pygame
import config
from os.path import exists, join
from entities import Player
from utilities import transition
from utilities.camera import Camera
from tilemap import Tiles
from growth_ui import Growth
from score_ui import Score
from result_ui import ResultScreen
from spawners.enemy_spawaner import createEnemies, choiceTypeFish
from spawners.particle_spawaner import spawnParticle
from utilities.transition import Transition


class Game:
    def __init__(self, screen, currentSlot) -> None:
        self.screen = screen
        self.currentSlot = currentSlot
        self.gameScreen = pygame.Surface((config.GAME_WIDTH, config.GAME_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        import loaderTexture
        import loaderMusic

        loaderMusic.load()

        self.loader = loaderTexture.loader
        self.ui_loader = loaderTexture.ui_loader
        self.music_loader = loaderMusic

        self.loadSlots()
        self.sessionStartTime = pygame.time.get_ticks()
        # load levels json
        try:
            with open(join("levels", f"level{self.currentLevel}.json"), "r") as file:
                self.levelConfig = json.load(file)
        except FileNotFoundError:
            print("level not found")
            return
        self.loadLevel()
        self.player.score = self.currentScore
        self.timeEnemy = 0.0

        self.transition = Transition(self.gameScreen, 0, backWord=True, upWord=False)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.resultScreen.handleInput(event)

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
                self.gameScreen.blit(self.resultScreen.overlay, (0, 0))

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

        return f"{hours:02}:{minutes:02}:{seconds:02}"

    def get_completion(self, totalLevel, currentLevel):
        return ((currentLevel - 1) / totalLevel) * 100

    def loadSlots(self):
        try:
            with open(
                join("save_slots", f"save_slot{self.currentSlot}.json"), "r"
            ) as file:
                slot = json.load(file)

            self.currentLevel = slot.get("currentLevel", 1)
            self.currentScore = slot.get("score", 0)
            self.completedLevels = slot.get("completedLevels", 0)
            self.playTime = slot.get("playTime", 0)

        except FileNotFoundError:
            print("slot not found")
            self.currentLevel = 1
            self.currentScore = 0
            self.completedLevels = 0
            self.playTime = 0
            self.completion = 0

    def saveSlots(self):
        data = {
            "id": self.currentSlot,
            "currentLevel": self.currentLevel,
            "completedLevels": self.completedLevels,
            "score": self.player.score,
            "playTime": self.getPlayTime(),
            "playTimeFormat": self.formatPlayTime(self.getPlayTime()),
            "completion": self.get_completion(2, self.currentLevel),
        }

        with open(join("save_slots", f"save_slot{self.currentSlot}.json"), "w") as file:
            json.dump(data, file, indent=4)

    def loadLevel(self):
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
        self.resultScreen = ResultScreen(self, ["score", "numberOfEating"])
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

    def nextLevel(self):
        currentScore = self.player.score

        nextLevel = self.currentLevel + 1
        nextLevelPath = join("levels", f"level{nextLevel}.json")

        try:
            with open(nextLevelPath, "r") as file:
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
        nextLevelPath = join("levels", f"level{self.currentLevel + 1}.json")
        return exists(nextLevelPath)


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption(config.WINDOW_TITLE)
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    menu = MainMenu(screen)
    menu.run()

    if menu.nextScreen == "save_slots":
        saveslots = SaveSlots(screen)
        saveslots.run()
        if saveslots.nextScreen == "Game":
            Game(screen, saveslots.currentSlot).run()
