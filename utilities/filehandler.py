from PIL import Image
import pygame


def sprite_handler(path, num_frame, column=False, row=True):
    sheet = pygame.image.load(path).convert_alpha()
    frames = []

    img = Image.open(path)

    if row:
        width = img.width // num_frame
        height = img.height
    elif column:
        width = img.width
        height = img.height // num_frame
    for i in range(num_frame):
        if row:
            frame = sheet.subsurface(pygame.Rect(i * width, 0, width, height))
        elif column:
            frame = sheet.subsurface(pygame.Rect(0, i * height, width, height))

        frames.append(frame)

    return frames
