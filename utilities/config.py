from dataclasses import dataclass
import pygame_gui
import pygame
from pygame_gui.core import ObjectID


def linearScaling(old_value,new_range,old_range):
    return int(old_value*new_range/old_range)


def positionCalc(start,index,spacing):
    return start+index*spacing


def drag_image(self, event,pygame,image_rect,mouse_x,mouse_y):

    if event.type == pygame.MOUSEBUTTONDOWN:

        if event.button == 1:

            if image_rect.collidepoint(
                mouse_x,
                mouse_y
            ):

                dragging = True

    elif event.type == pygame.MOUSEMOTION:

        if dragging:

            image_rect.center = (
                mouse_x,
                mouse_y
            )

    elif event.type == pygame.MOUSEBUTTONUP:

        if event.button == 1:

            dragging = False

@dataclass
class UILayout:
    margin: int = 5
    width: int = 32
    height: int = 32
    spacing: int = 5
    vertical: bool = False

def ui_add_buttton(
    items,
    item_name,
    ui_manager,
    container,
    layout,
    object_id,
    text='',
    key_button=False,
):
    button = pygame_gui.elements.UIButton(
        object_id=ObjectID(class_id=object_id),
        relative_rect=pygame.Rect(
            0,
            0,
            layout.width,
            layout.height
        ),
        text=text,
        manager=ui_manager,
        container=container
    )

    items[item_name] = button

    ui_update_layout(items, layout)

    return button

def ui_update_layout(items, layout):

    for index, item in enumerate(items.values()):

        if not layout.vertical:
            x = positionCalc(
                layout.margin,
                index,
                layout.width + layout.spacing
            )
            item.set_relative_position(
                (x, layout.margin)
            )
        else:
            y= positionCalc(
                layout.margin,
                index,
                layout.height + layout.spacing
            )
            item.set_relative_position(
                (layout.margin,y)
            )

colors={
    'red':(255,0,0),
    'green':(0,255,0),
    'blue':(0,0,255),
    'yellow':(255,255,0),
    'dark_red': (140, 25, 25),
    'dark_green': (35, 110, 45),
    'dark_blue': (30, 55, 120),
    'dark_yellow': (145, 125, 25)
}