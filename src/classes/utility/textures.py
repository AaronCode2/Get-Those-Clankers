import pygame
import classes.utility.utils as utils
import enum

class imgIndex[Enum]:

    PLAYER_IMG = 0
    TILE_IMG = 1

# This is constant and should not be changed for storing texture data

images = {      

        # Tiles
        "Tiles": {
            "location": "assets/tiles/objects.png",
            "maxFramesX": 2,
            "FramesY": 1,
            "image": {

                "surface": None,
                "FrameWidth": None,
                "FrameHeight": None
            },

            "rotatedImages": {

                utils.RotationType.LEFT: None,
                utils.RotationType.UP: None,
                utils.RotationType.RIGHT: None
            }
        },

        "Battery": {

            "location": "assets/tiles/battery.png",
            "maxFramesX": 6,
            "FramesY": 1,
            "image": {

                "surface": None,
                "FrameWidth": None,
                "FrameHeight": None
            },

        },

        "keys": {

            "location": "assets/ui/keys.png",
            "maxFramesX": 3,
            "FramesY": 1,
            "image": {

                "surface": None,
                "FrameWidth": None,
                "FrameHeight": None
            },
        },

        "guiPlates": {

            "location": "assets/ui/guiPlates.png",
            "FramesX": 6,
            "FramesY": 10,
            "image": {

                "surface": None,
                "FrameWidth": None,
                "FrameHeight": None
            },
        },

        "batteryIndicator": {

            "location": "ui/battery_indicator.png",
            "FramesX": 2,
            "FramesY": 6,

            "animationNames": [
                "BATTERY_FULL", "BATTERY_DRAIN_1", 
                "BATTERY_DRAIN_2", "BATTERY_DRAIN_3",
                "BATTERY_DRAIN_4", "BATTERY_EMPTY"
            ]
        },

        "Items": {

            "location": "assets/ui/items.png",
            "FramesX": 9,
            "FramesY": 1,
            "image": {

                "surface": None,
                "FrameWidth": None,
                "FrameHeight": None
            },
        },

        "Tower": {

            "location": "towers/tower.png",
            "FramesX": 12,
            "FramesY": 1,
            "AnimationNames": "idle",
            "image": {

                "Animation": None,
                "FrameWidth": None,
                "FrameHeight": None
            },
        }, 

        "Selector": {

            "location": "assets/ui/selector.png",
            "FramesX": 1,
            "FramesY": 1,
            "image": {

                "surface": None,
                "FrameWidth": 64,
                "FrameHeight": 64
            },
        }
}

# All UI stuff, added it here, so all members can acess

def drawGuiSinglePlate(window, position: pygame.Vector2, guiPlate: utils.GuiPlates):

    window.blit(images["guiPlates"]["image"]["surface"], position, getGuiPlatesSrcRect(guiPlate))


def configureguiPlateSelection(x: int, y: int, size: pygame.Vector2, typeGuiPlate: utils.TypeOfGuiPlates):

    if(typeGuiPlate == utils.TypeOfGuiPlates.NORMAL):
        if(y == 0 and x != 0 and x != size.x - 1):
            return getGuiPlatesSrcRect(utils.GuiPlates.TOP_MIDDLE)
        elif(y == 0 and x == size.x - 1):
            return getGuiPlatesSrcRect(utils.GuiPlates.CORNER_TOP_RIGHT)
        elif(y != 0 and x == 0 and y != size.y - 1):
            return getGuiPlatesSrcRect(utils.GuiPlates.MIDDLE_LEFT_SIDE)
        elif(y != 0 and x != 0 and y != size.y - 1 and x != size.x - 1):
            return getGuiPlatesSrcRect(utils.GuiPlates.MIDDLE)
        elif(y != 0 and y != size.y - 1 and x == size.x - 1):
            return getGuiPlatesSrcRect(utils.GuiPlates.MIDDLE_RIGHT_SIDE)
        elif(y == size.y - 1 and x == 0):
            return getGuiPlatesSrcRect(utils.GuiPlates.CORNER_BOTTOM_LEFT)
        elif(y == size.y - 1 and x != 0 and x != size.x - 1):
            return getGuiPlatesSrcRect(utils.GuiPlates.BOTTOM_MIDDLE)

        elif(y == size.y - 1 and x == size.x - 1):
            return getGuiPlatesSrcRect(utils.GuiPlates.CORNER_BOTTOM_RIGHT)

        return getGuiPlatesSrcRect(utils.GuiPlates.CORNER_TOP_LEFT)
    else:

        if(y == 0 and x != 0 and x != size.x - 1):
            return getGuiPlatesSrcRect(utils.GuiPlates.MAR_TOP_MIDDLE)
        elif(y == 0 and x == size.x - 1):
            return getGuiPlatesSrcRect(utils.GuiPlates.MAR_CORNER_TOP_RIGHT)
        elif(y != 0 and x == 0 and y != size.y - 1):
            return getGuiPlatesSrcRect(utils.GuiPlates.MAR_MIDDLE_LEFT_SIDE)
        elif(y != 0 and x != 0 and y != size.y - 1 and x != size.x - 1):
            return getGuiPlatesSrcRect(utils.GuiPlates.MAR_MIDDLE)
        elif(y != 0 and y != size.y - 1 and x == size.x - 1):
            return getGuiPlatesSrcRect(utils.GuiPlates.MAR_MIDDLE_RIGHT_SIDE)
        elif(y == size.y - 1 and x == 0):
            return getGuiPlatesSrcRect(utils.GuiPlates.MAR_CORNER_BOTTOM_LEFT)
        elif(y == size.y - 1 and x != 0 and x != size.x - 1):
            return getGuiPlatesSrcRect(utils.GuiPlates.MAR_BOTTOM_MIDDLE)

        elif(y == size.y - 1 and x == size.x - 1):
            return getGuiPlatesSrcRect(utils.GuiPlates.MAR_CORNER_BOTTOM_RIGHT)

        return getGuiPlatesSrcRect(utils.GuiPlates.MAR_CORNER_TOP_LEFT)

def drawGuiPlates(window, size: pygame.Vector2, position: pygame.Vector2, typeGuiPlate = utils.TypeOfGuiPlates.NORMAL):

    for y in range(int(size.y)):
        for x in range(int(size.x)):

            platePosition = pygame.Vector2(

                images["keys"]["image"]["FrameWidth"] * x + position.x,
                images["keys"]["image"]["FrameHeight"] * y + position.y,
            ) 
                
            srcRect = configureguiPlateSelection(x, y, size, typeGuiPlate)
                
            window.blit(images["guiPlates"]["image"]["surface"], platePosition, srcRect)

def getGuiPlatesSrcRect(guiPlate: utils.GuiPlates):

    if(len(utils.guiPlatesFrameMap[guiPlate]) == 2):
        return pygame.Rect(
            images["guiPlates"]["image"]["FrameWidth"] * float(utils.guiPlatesFrameMap[guiPlate][0]), 
            images["guiPlates"]["image"]["FrameHeight"] * float(utils.guiPlatesFrameMap[guiPlate][1]),
            images["guiPlates"]["image"]["FrameWidth"],
            images["guiPlates"]["image"]["FrameHeight"]
        )
    else:
        return pygame.Rect(
            images["guiPlates"]["image"]["FrameWidth"] * float(utils.guiPlatesFrameMap[guiPlate][0]), 
            images["guiPlates"]["image"]["FrameHeight"] * float(utils.guiPlatesFrameMap[guiPlate][1]),
            images["guiPlates"]["image"]["FrameWidth"] * float(utils.guiPlatesFrameMap[guiPlate][2]),
            images["guiPlates"]["image"]["FrameHeight"] * float(utils.guiPlatesFrameMap[guiPlate][3])
        )