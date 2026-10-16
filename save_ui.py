from os.path import exists, join
import json

from utilities.ui_helper import scaleImage
import pygame
import config
from utilities.button import Button, CustomButton


class SaveSlots:
    def __init__(self, screen) -> None:
        self.screen = screen
        self.gameScreen = pygame.Surface((config.GAME_WIDTH, config.GAME_HEIGHT))
        self.running = True
        self.nextScreen = None
        self.titleClicked = False

        from loaderTexture import ui_loader

        self.ui_loader = ui_loader
        self.saveButtonList = []
        button_height = ui_loader["buttonSave/idle"].get_height() * 2
        spacing = 16
        total_height = 3 * button_height + 2 * spacing

        start_y = (config.GAME_HEIGHT - total_height) // 2

        for i in range(3):
            savePath = join("save_slots", f"save_slot{i + 1}.json")
            y = start_y + i * (button_height + spacing)
            buttonData = None
            if exists(savePath):
                with open(savePath, "r") as file:
                    buttonData = json.load(file)
                self.saveButtonList.append(
                    CustomButton(
                        self.gameScreen,
                        ui_loader["buttonSave"],
                        ui_loader["buttonSave2"],
                        "",
                        self.gameScreen.get_rect(),
                        "midtop",
                        [0, y],
                        f"{i + 1}.",
                        f"{buttonData['completion']}%",
                        f"{buttonData['playTime']}",
                        scale=2,
                        fontSize=24,
                    )
                )
            else:
                self.saveButtonList.append(
                    Button(
                        self.gameScreen,
                        ui_loader["buttonSave/idle"],
                        ui_loader["buttonSave/click"],
                        "New Save",
                        self.gameScreen.get_rect(),
                        "midtop",
                        [0, y],
                        scale=2,
                        fontSize=24,
                    )
                )

    def run(self):
        clock = pygame.time.Clock()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
                    scale_x = config.GAME_WIDTH / self.screen.get_width()
                    scale_y = config.GAME_HEIGHT / self.screen.get_height()

                    event.pos = (
                        int(event.pos[0] * scale_x),
                        int(event.pos[1] * scale_y),
                    )

                for index, slotButton in enumerate(self.saveButtonList):
                    if slotButton.handle_input(event):
                        savePath = join("save_slots", f"save_slot{index + 1}.json")
                        data = {
                            "id": index,
                            "currentLevel": 1,
                            "completedLevels": 0,
                            "score": 0,
                            "playTime": 0,
                        }

                        data["completion"] = (data["completedLevels"] // 2) * 100
                        with open(savePath, "w") as file:
                            json.dump(data, file, indent=4)
                        self.saveButtonList[index] = CustomButton(
                            self.gameScreen,
                            self.ui_loader["buttonSave"],
                            self.ui_loader["buttonSave2"],
                            "",
                            self.gameScreen.get_rect(),
                            "midtop",
                            [0, slotButton.offset[1]],
                            f"{index + 1}.",
                            f"{data['completion']}%",
                            str(data["playTime"]),
                            scale=2,
                            fontSize=24,
                        )
                        self.titleClicked = True

            self.gameScreen.fill((0, 0, 0))
            if self.titleClicked:
                self.nextScreen = "Game"
                self.running = False
            for saveButton in self.saveButtonList:
                saveButton.draw()

            scaled = pygame.transform.scale(
                self.gameScreen,
                self.screen.get_size(),
            )
            self.screen.blit(scaled, (0, 0))

            pygame.display.flip()
            clock.tick(config.FRAME_RATE)
