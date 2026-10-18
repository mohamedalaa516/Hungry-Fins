from os.path import exists
import json

import pygame
import config

from utilities.button import Button, CustomButton
from paths import save_path


class SaveSlots:
    def __init__(self, screen) -> None:
        self.screen = screen
        self.gameScreen = pygame.Surface((config.GAME_WIDTH, config.GAME_HEIGHT))

        self.running = True
        self.nextScreen = None
        self.titleClicked = False
        self.currentSlot = 0

        from loaderTexture import ui_loader

        self.ui_loader = ui_loader
        self.saveButtonList = []

        button_height = self.ui_loader["buttonSave/idle"].get_height() * 2
        spacing = 16
        total_height = 3 * button_height + 2 * spacing
        start_y = (config.GAME_HEIGHT - total_height) // 2

        for i in range(3):
            savePath = save_path(i + 1)
            y = start_y + i * (button_height + spacing)

            if exists(savePath):
                with open(savePath, "r", encoding="utf-8") as file:
                    buttonData = json.load(file)

                self.saveButtonList.append(
                    CustomButton(
                        self.gameScreen,
                        self.ui_loader["buttonSave"],
                        self.ui_loader["buttonSave2"],
                        "",
                        self.gameScreen.get_rect(),
                        "midtop",
                        [0, y],
                        f"{i + 1}.",
                        str(buttonData.get("playTimeFormat", 0)),
                        f"{buttonData.get('completion', 0)}%",
                        color=(46, 34, 47),
                        scale=2,
                        fontSize=12,
                    )
                )

            else:
                self.saveButtonList.append(
                    Button(
                        self.gameScreen,
                        self.ui_loader["buttonSave/idle"],
                        self.ui_loader["buttonSave/click"],
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
                    continue

                if event.type in (
                    pygame.MOUSEBUTTONDOWN,
                    pygame.MOUSEBUTTONUP,
                ):
                    scale_x = config.GAME_WIDTH / self.screen.get_width()
                    scale_y = config.GAME_HEIGHT / self.screen.get_height()

                    event.pos = (
                        int(event.pos[0] * scale_x),
                        int(event.pos[1] * scale_y),
                    )

                for index, slotButton in enumerate(self.saveButtonList):
                    if slotButton.handle_input(event):
                        savePath = save_path(index + 1)

                        # Create a new save file if needed.
                        if not exists(savePath):
                            data = {
                                "id": index + 1,
                                "currentLevel": 1,
                                "completedLevels": 0,
                                "score": 0,
                                "playTime": 0,
                                "playTimeFormat": "00:00:00",
                                "completion": 0,
                            }

                            with open(savePath, "w", encoding="utf-8") as file:
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
                                str(data["playTimeFormat"]),
                                f"{data['completion']}%",
                                color=(46, 34, 47),
                                scale=2,
                                fontSize=12,
                            )

                        # Select the slot without resetting its data.
                        self.currentSlot = index + 1
                        self.titleClicked = True
                        break

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
