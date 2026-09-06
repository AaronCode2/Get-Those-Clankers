from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import classes.bots.bot as bot

import pygame
import random
from enum import Enum
import classes.manager.camera as camera
import math


# For constants and utility

dev_PositionAdjuster = pygame.Vector2(10, 500)
dev_PositionAdjusterToggle = False

# This for UI stuff

def dev_updatePositionsAdjuster():

    mousePos = pygame.mouse.get_pos()
    key = pygame.key.get_just_pressed()
    global dev_PositionAdjusterToggle

    if(key[pygame.K_p]):
        dev_PositionAdjusterToggle = not dev_PositionAdjusterToggle

    if(dev_PositionAdjusterToggle):
        dev_PositionAdjuster.x = mousePos[0]
        dev_PositionAdjuster.y = mousePos[1]
        print("X:", dev_PositionAdjuster.x, "Y:", dev_PositionAdjuster.y)

font = None
smfont = None
ssmfont = None

colladjust = 0.1


class BotTarget(Enum):
    PLAYER = 0,
    BATTERY = 1

class TypeOfGuiPlates(Enum):

    NORMAL = 0
    MARGIN = 1

class Bots(Enum):

    DEAFULT = 0

class BotBehaviour(Enum):

    ANGRY = 0
    STUIPED = 1
    SCARED = 2
    TELPORTER = 3

class GuiPlates(Enum):

    CORNER_TOP_LEFT = 0
    TOP_MIDDLE = 1
    CORNER_TOP_RIGHT = 2

    MIDDLE_LEFT_SIDE = 3
    MIDDLE = 4
    MIDDLE_RIGHT_SIDE = 5

    CORNER_BOTTOM_LEFT = 6
    BOTTOM_MIDDLE = 7
    CORNER_BOTTOM_RIGHT = 8

    SMALL_BUTTON_UNPRESSED = 9
    SMALL_BUTTON_PRESSED = 10

    LARGE_BUTTON_UNPRESSED = 11
    LARGE_BUTTON_PRESSED = 12

    MAR_CORNER_TOP_LEFT = 13
    MAR_TOP_MIDDLE = 14
    MAR_CORNER_TOP_RIGHT = 15

    MAR_MIDDLE_LEFT_SIDE = 16
    MAR_MIDDLE = 17
    MAR_MIDDLE_RIGHT_SIDE = 18

    MAR_CORNER_BOTTOM_LEFT = 19
    MAR_BOTTOM_MIDDLE = 20
    MAR_CORNER_BOTTOM_RIGHT = 21

    XL_BUTTON_UNPRESSED = 22
    XL_BUTTON_PRESSED = 23

    XL_ORANGE_BUTTON_UNPRESSED = 23
    XL_ORANGE_BUTTON_PRESSED = 24

# The x and y mapped for the guiPlate frames

guiPlatesFrameMap = {

    GuiPlates.CORNER_TOP_LEFT: (0, 0),
    GuiPlates.TOP_MIDDLE: (1, 0),
    GuiPlates.CORNER_TOP_RIGHT: (2, 0),

    GuiPlates.MIDDLE_LEFT_SIDE: (0, 1),
    GuiPlates.MIDDLE: (1, 1),
    GuiPlates.MIDDLE_RIGHT_SIDE: (2, 1),

    GuiPlates.CORNER_BOTTOM_LEFT: (0, 2),
    GuiPlates.BOTTOM_MIDDLE: (1, 2),
    GuiPlates.CORNER_BOTTOM_RIGHT: (2, 2),

    GuiPlates.SMALL_BUTTON_UNPRESSED: (0, 3),
    GuiPlates.SMALL_BUTTON_PRESSED: (1, 3),

    GuiPlates.LARGE_BUTTON_UNPRESSED: (0, 4, 2, 1), 
    GuiPlates.LARGE_BUTTON_PRESSED: (2, 4, 2, 1),

    GuiPlates.MAR_CORNER_TOP_LEFT: (0, 5),
    GuiPlates.MAR_TOP_MIDDLE: (1, 5),
    GuiPlates.MAR_CORNER_TOP_RIGHT: (2, 5),

    GuiPlates.MAR_MIDDLE_LEFT_SIDE: (0, 6),
    GuiPlates.MAR_MIDDLE: (1, 6),
    GuiPlates.MAR_MIDDLE_RIGHT_SIDE: (2, 6),

    GuiPlates.MAR_CORNER_BOTTOM_LEFT: (0, 7),
    GuiPlates.MAR_BOTTOM_MIDDLE: (1, 7),
    GuiPlates.MAR_CORNER_BOTTOM_RIGHT: (2, 7),

    GuiPlates.XL_BUTTON_UNPRESSED: (0, 8, 3, 1),
    GuiPlates.XL_BUTTON_PRESSED: (3, 8, 3, 1),

    GuiPlates.XL_ORANGE_BUTTON_UNPRESSED: (0, 9, 3, 1),
    GuiPlates.XL_ORANGE_BUTTON_PRESSED: (3, 9, 3, 1)
}

class KeyGuides(Enum):

    CRTL_TO_SNAP = 0
    WASD_TO_MOVE = 1
    R_TO_ROTATE = 2
    E_OPEN_INVENTORY = 3
    LEFT_M_PLACE_OR_DRAG_INVENTORY = 4
    RIGHT_M_DELETE_OR_SPLIT_INVENTORY = 5

detectBoxAdj = pygame.Vector2(10, -20)

keyPosAdj = 45

keyGuidesTexts = {

    "onWorld": {

        KeyGuides.CRTL_TO_SNAP: "Snap Mode",
        KeyGuides.WASD_TO_MOVE: "Move",
        KeyGuides.R_TO_ROTATE: "Rotate Object",
        KeyGuides.E_OPEN_INVENTORY: "Inventory",
        KeyGuides.R_TO_ROTATE: "Rotate Object",
        KeyGuides.LEFT_M_PLACE_OR_DRAG_INVENTORY: "Place",
        KeyGuides.RIGHT_M_DELETE_OR_SPLIT_INVENTORY: "Delete",
    },

    "onInventory": {

        KeyGuides.E_OPEN_INVENTORY: "Inventory",
        KeyGuides.LEFT_M_PLACE_OR_DRAG_INVENTORY: "Drag Item",
        KeyGuides.RIGHT_M_DELETE_OR_SPLIT_INVENTORY: "Split"
    },

    "textOffsets": {

        KeyGuides.CRTL_TO_SNAP: 0,
        KeyGuides.WASD_TO_MOVE: 160,
        KeyGuides.R_TO_ROTATE: 230,
        KeyGuides.LEFT_M_PLACE_OR_DRAG_INVENTORY: 400,
        KeyGuides.RIGHT_M_DELETE_OR_SPLIT_INVENTORY: 500,
        KeyGuides.E_OPEN_INVENTORY: 600
    } 
}


class WhichInventory(Enum):

    INVENTORY = 0,
    HOTBAR = 1,

class RotationType(Enum):

    DOWN = 0
    LEFT = 1
    UP = 2
    RIGHT = 3

deltaTime = 0.3
hotBarindex = 5
inventoryCols = 5
clickdelay = 0.005

dialogTextPos = pygame.Vector2(466, 23)

def mouseClickedOnceL(rect: pygame.Rect):

    mouse = pygame.mouse.get_pos()
    mouseButtons = pygame.mouse.get_just_released()

    return rect.collidepoint(pygame.Vector2(mouse[0], mouse[1])) and mouseButtons[0]

def mouseHover(rect: pygame.Rect):

    mouse = pygame.mouse.get_pos()

    return rect.collidepoint(pygame.Vector2(mouse[0], mouse[1]))

def mouseClickedL(rect: pygame.Rect):

    mouse = pygame.mouse.get_pos()
    mouseButtons = pygame.mouse.get_just_pressed()

    return rect.collidepoint(pygame.Vector2(mouse[0], mouse[1])) and mouseButtons[0]

def mouseClickedM(rect: pygame.Rect):

    mouse = pygame.mouse.get_pos()
    mouseButtons = pygame.mouse.get_just_pressed()

    return rect.collidepoint(pygame.Vector2(mouse[0], mouse[1])) and mouseButtons[1]

def mouseClickedR(rect: pygame.Rect):

    mouse = pygame.mouse.get_pos()
    mouseButtons = pygame.mouse.get_just_pressed()

    return rect.collidepoint(pygame.Vector2(mouse[0], mouse[1])) and mouseButtons[2]

class SlotIndex(Enum):

    AMOUNT = 0
    TYPE = 1

class ItemType(Enum):

    NONE = -1
    SCRAP_IGNOT = 0
    RINGED_TIN = 1
    SCREW = 2
    BOLT = 3
    RAW_IRON = 4
    SOFT_STEEL = 5
    SOLAR_PANEL = 6
    BARRIER = 7
    GREEN_TOWER = 8
    STRONG_BARRIER = 9
    STRONGER_BARRIER = 10
    CRATE = 11

def generateItemForDropItem():

    itemPerc = random.randint(0, 100)

    amount = random.randint(1, 15)
    itemType = None

    # Balancing can be adjusted

    if(itemPerc == 1): # 1%
        itemType = ItemType.SOLAR_PANEL
    elif(itemPerc <= 15): # 15%
        itemType = ItemType.RINGED_TIN
    elif(itemPerc > 15 and itemPerc <= 30): # 15%
        itemType = ItemType.BOLT
        amount += 4
    elif(itemPerc > 30 and itemPerc <= 40): # 10%
        itemType = ItemType.SCREW
        amount += 14
    elif(itemPerc > 40 and itemPerc <= 50): # 20%
        itemType = ItemType.SCRAP_IGNOT
        amount += 2
    elif(itemPerc > 50 and itemPerc <= 55): # 5%
        itemType = ItemType.SOFT_STEEL
        amount += 5
    elif(itemPerc > 55 and itemPerc <= 70): # 15%
        itemType = ItemType.BOLT
        amount /= 2
    else: # 30%
        itemType = ItemType.RAW_IRON
        amount *= 2

    return itemType, amount

def convertToTileType(ItemType: ItemType):

    match(ItemType):

        case ItemType.SOLAR_PANEL:
            return TileType.SOLAR_PANEL

        case ItemType.BARRIER:
            return TileType.BARRIER

        case ItemType.STRONG_BARRIER:
            return TileType.STRONG_BARRIER

        case ItemType.STRONGER_BARRIER:
            return TileType.STRONGER_BARRIER

        case ItemType.CRATE:
            return TileType.CRATE

        case ItemType.GREEN_TOWER:
            return TileType.GREEN_TOWER

        case _:
            return None

screenRect = pygame.Rect()
windowResized = False

batteryRectSize = 64

charPos = pygame.Vector2(366, 46)

backgroundDailogPos = pygame.Vector2(332, 11)

hotBarSizeWidth = 64 * 6
hotBarSizeHeight = 64 * 2

activateTilePlacer = True

bulletDuration = 5

inventoryTextPos = pygame.Vector2(10, 10)
itemPosAdj = pygame.Vector2(15, 15)
inventoryPosAdj = pygame.Vector2(382, 480)
HotBarPosAdj = pygame.Vector2(382, 109)
inventorySlotPosAdj = pygame.Vector2(357, 460)
HotBarSlotPosAdj = pygame.Vector2(357, 90)
inventoryOptionPosAdj = pygame.Vector2(382, 590)

solarImportMin = 1
solarImportMax = 4

batterydelateMin = 3
batterydelateMax = 10

smallButtonSize = 64

XLButtonSizeWidth = 192
XLButtonSizeHeight = 64

fullDay = 300

botCoolDown = 5

BulletPlacementPosAdj = pygame.Vector2(16, 15)

# Crafter and craft are two different things! don't get confused

crafterButtonAdj = pygame.Vector2(20, 20)
crafterTextAdj = pygame.Vector2(18, 12)

crafterPosAdj = pygame.Vector2(1010, 590)
crafterPosMarPlatePosAdj1 = pygame.Vector2(10, 20)
crafterPosMarPlatePosAdj2 = pygame.Vector2(400, 20)

craftButtonAdj = pygame.Vector2(612, 116)
craftButtonTextAdj = pygame.Vector2(563, 107)

crafterGridSize = pygame.Vector2(4, 5)
crafterRecipeButtonPosAdj = pygame.Vector2(976, 611)

batteryBackgroundHudPos = pygame.Vector2(10, 10)

itemRequiredPosAdj = pygame.Vector2(598, 373)
itemRequiredTextPosAdj = 40

itemGivenPosAdj = pygame.Vector2(594, 152)
itemGivenTextPosAdj = 37

stackSize = 84

snapdetectAdj = pygame.Vector2(-5, -5)
snapdetect2Adj = pygame.Vector2(-5, -48)
snapdetect3Adj = pygame.Vector2(-2, -10)

defaultImageSizes = 64

scrollWheel = pygame.Vector2(0, 0)
tileMaxFrames = 4.0

batteryIndicatorPos = pygame.Vector2(240, 30)

descriptionPosAdj = pygame.Vector2(599, 556)

adjmousePos = pygame.Vector2(-24, -24)

class SnapType(Enum):

    RIGHT_SIDE = 0
    LEFT_SIDE = 1
    DOWN_SIDE = 2
    UP_SIDE = 3

def getTileRect(position: pygame.Vector2):
    return pygame.Rect(position.x, position.y, defaultImageSizes, defaultImageSizes)

def getTilesDetectRect(position: pygame.Vector2):

    return pygame.Rect(position.x + 20, position.y + 20, defaultImageSizes - 20, defaultImageSizes - 20)


def getSnapConfig(snapType: SnapType, selectedTile, rotationType: RotationType):


    if rotationType == RotationType.DOWN or rotationType == RotationType.UP:
        match(snapType):

            case SnapType.RIGHT_SIDE:

                return pygame.Rect(
                    selectedTile.getDestRect().x - hitBoxAdjForTiles[selectedTile.type][selectedTile.rotation].x + selectedTile.getDestRect().width,
                    selectedTile.getDestRect().y - hitBoxAdjForTiles[selectedTile.type][selectedTile.rotation].y,
                    selectedTile.getDestRect().width - hitBoxAdjForTiles[selectedTile.type][selectedTile.rotation].width, 
                    selectedTile.getDestRect().height - hitBoxAdjForTiles[selectedTile.type][selectedTile.rotation].height
                )
            case SnapType.LEFT_SIDE:

                return pygame.Rect(
                    selectedTile.getDestRect().x - hitBoxAdjForTiles[selectedTile.type][selectedTile.rotation].x - selectedTile.getDestRect().width,
                    selectedTile.getDestRect().y - hitBoxAdjForTiles[selectedTile.type][selectedTile.rotation].y,
                    selectedTile.getDestRect().width - hitBoxAdjForTiles[selectedTile.type][selectedTile.rotation].width, 
                    selectedTile.getDestRect().height - hitBoxAdjForTiles[selectedTile.type][selectedTile.rotation].height
                )
            case SnapType.DOWN_SIDE:

                return pygame.Rect(
                    selectedTile.getDestRect().x - hitBoxAdjForTiles[selectedTile.type][selectedTile.rotation].x,
                    selectedTile.getDestRect().y - hitBoxAdjForTiles[selectedTile.type][selectedTile.rotation].y + selectedTile.getDestRect().height,
                    selectedTile.getDestRect().width - hitBoxAdjForTiles[selectedTile.type][selectedTile.rotation].width, 
                    selectedTile.getDestRect().height - hitBoxAdjForTiles[selectedTile.type][selectedTile.rotation].height
                )
            case SnapType.UP_SIDE:

                return pygame.Rect(
                    selectedTile.getDestRect().x - hitBoxAdjForTiles[selectedTile.type][selectedTile.rotation].x,
                    selectedTile.getDestRect().y - hitBoxAdjForTiles[selectedTile.type][selectedTile.rotation].y - selectedTile.getDestRect().height,
                    selectedTile.getDestRect().width - hitBoxAdjForTiles[selectedTile.type][selectedTile.rotation].width, 
                    selectedTile.getDestRect().height - hitBoxAdjForTiles[selectedTile.type][selectedTile.rotation].height
                )
    else:

        match(snapType):

            case SnapType.UP_SIDE:

                return pygame.Rect(
                    selectedTile.getDestRect().x - hitBoxAdjForTiles[selectedTile.type][selectedTile.rotation].x,
                    selectedTile.getDestRect().y - hitBoxAdjForTiles[selectedTile.type][selectedTile.rotation].y + selectedTile.getDestRect().height,
                    selectedTile.getDestRect().width - hitBoxAdjForTiles[selectedTile.type][selectedTile.rotation].width, 
                    selectedTile.getDestRect().height - hitBoxAdjForTiles[selectedTile.type][selectedTile.rotation].height
                )
            case SnapType.DOWN_SIDE:

                return pygame.Rect(
                    selectedTile.getDestRect().x - hitBoxAdjForTiles[selectedTile.type][selectedTile.rotation].x,
                    selectedTile.getDestRect().y - hitBoxAdjForTiles[selectedTile.type][selectedTile.rotation].x - selectedTile.getDestRect().height,
                    selectedTile.getDestRect().width - hitBoxAdjForTiles[selectedTile.type][selectedTile.rotation].x, 
                    selectedTile.getDestRect().height - hitBoxAdjForTiles[selectedTile.type][selectedTile.rotation].x
                )
            case SnapType.RIGHT_SIDE:

                return pygame.Rect(
                    selectedTile.getDestRect().x - hitBoxAdjForTiles[selectedTile.type][selectedTile.rotation].x + selectedTile.getDestRect().width,
                    selectedTile.getDestRect().y - hitBoxAdjForTiles[selectedTile.type][selectedTile.rotation].y,
                    selectedTile.getDestRect().width - hitBoxAdjForTiles[selectedTile.type][selectedTile.rotation].width, 
                    selectedTile.getDestRect().height - hitBoxAdjForTiles[selectedTile.type][selectedTile.rotation].height
                )
            case SnapType.LEFT_SIDE:

                return pygame.Rect(
                    selectedTile.getDestRect().x - hitBoxAdjForTiles[selectedTile.type][selectedTile.rotation].x - selectedTile.getDestRect().width,
                    selectedTile.getDestRect().y - hitBoxAdjForTiles[selectedTile.type][selectedTile.rotation].y,
                    selectedTile.getDestRect().width - hitBoxAdjForTiles[selectedTile.type][selectedTile.rotation].width, 
                    selectedTile.getDestRect().height - hitBoxAdjForTiles[selectedTile.type][selectedTile.rotation].height
                )

def configureRotatedImageForPreview(width, height, type, rotation):

    match(rotation):

        case RotationType.DOWN:

            srcRect = pygame.Rect(
                width * float(type.value), 
                0,
                width, height
            )

        case RotationType.LEFT:

            srcRect = pygame.Rect(
                0, 
                height * (tileMaxFrames - float(type.value)),
                width, height
            )

        case RotationType.UP:

            srcRect = pygame.Rect(
                width * (tileMaxFrames - float(type.value)),
                0, 
                width, height
            )

        case RotationType.RIGHT:

            srcRect = pygame.Rect(
                0, 
                width * float(type.value),
                width, height
            )

    return srcRect

# The side of screen is where the bots spawn

BotsSpaceings = 100

class BotAppearings(Enum):

    SIDE_RIGHT_SCREEN = 0
    SIDE_LEFT_SCREEN = 1
    SIDE_TOP_SCREEN = 2
    SIDE_BOTTOM_SCREEN = 3

BatteryDisplayHudPositions = {

    "TimeLeft": pygame.Vector2(12, 30),
    "WattsGenerated": pygame.Vector2(13, 65),
    "Day": pygame.Vector2(13, 100)
}

dayShowerPosAdj = pygame.Vector2(-20, -80)

ColorPlattes = {

    "Future Blue": (39, 137, 205),
    "Supreme Yellow": (248, 197, 58),
    "Pale White": (236, 235, 231),
    "Glass Orange": (241, 100, 31),
    "Grey Cloud": (128, 123, 128),
    "Sandy Yellow": (170, 100, 49),
    "Purple Moose": (86, 88, 123)
}

def formatToClock(seconds: int):

    clockMins = seconds // 60

    clockSeconds = str(abs((clockMins * 60) - seconds))

    return str(clockMins) + ":" + clockSeconds

def formatTo24Hourclock(seconds):

    clockMins = seconds // 60

    clockSeconds = str(abs((clockMins * 60) - seconds))

    if(len(clockSeconds) == 1):
        clockSeconds = "0" + clockSeconds

    clockMinsStr = str(clockMins)

    if(len(clockMinsStr) == 1):
        clockMinsStr = "0" + clockMinsStr

    return clockMinsStr + ":" + clockSeconds

def debugDraw(window, destRect: pygame.Rect, color = (255, 0, 0)):

    rect = pygame.Surface((destRect.width, destRect.height))
    rect.set_alpha(100)
    rect.fill(color)
    window.blit(rect, (destRect.x, destRect.y))

def getDebugRectItem(window, destRect: pygame.Rect, color = (255, 0, 0)) -> camera.CameraItem:

    rect = pygame.Surface((destRect.width, destRect.height))
    rect.set_alpha(100)
    rect.fill(color)
    return rect, destRect.topleft, None, destRect.centery

def calculateMeetPosition(entity: bot.Bot, distance, projectile_speed):
    a = entity.velocity.length() ** 2 - projectile_speed ** 2
    b = 2 * (distance.dot(entity.velocity))
    c = distance.length_squared()
    delta = (b ** 2) - (4 * a * c)

    solutions: list[float] = []

    if delta < 0:
        return
    elif delta == 0:
        solutions.append((b) / (2 * a))
    else:
        root_part = math.sqrt(delta)

        solutions.append((b - root_part) / (2 * a))
        solutions.append((b + root_part) / (2 * a))

    smallest_time = float("inf")
    for solution in solutions:
        if solution >= 0:
            smallest_time = min(smallest_time, solution)

    if smallest_time == float("inf"):
        print("couldn't shot the enemy")
        # tower can't hit ennemy
        return

    target_meet_position = entity.rect.center + smallest_time * entity.velocity
    return target_meet_position

rotations = {

    RotationType.DOWN: 0,
    RotationType.LEFT: 90,
    RotationType.UP: 180,
    RotationType.RIGHT: 270
}

batteryStages = 5

class BatteryLevel(Enum):

    BATTERY_FULL = 0
    BATTERY_DRAIN_1 = 1
    BATTERY_DRAIN_2 = 2
    BATTERY_DRAIN_3 = 3
    BATTERY_DRAIN_4 = 4
    BATTERY_EMPTY = 5

class TileType(Enum):

    BARRIER = 0
    SOLAR_PANEL = 1
    STRONG_BARRIER = 2
    STRONGER_BARRIER = 3
    CRATE = 4
    GREEN_TOWER = 5

durabiltyForTile = {

    TileType.SOLAR_PANEL: 15,
    TileType.BARRIER: 8,
    TileType.STRONG_BARRIER: 20,
    TileType.STRONGER_BARRIER: 32,
    TileType.CRATE: 4,
    TileType.GREEN_TOWER: 40
}

hitBoxAdjForTiles = {

    TileType.BARRIER: {

        RotationType.UP: pygame.Rect(2, 2, -4, -4),
        RotationType.DOWN: pygame.Rect(2, 2, -4, -4),
        RotationType.LEFT: pygame.Rect(2, 2, -4, -4),
        RotationType.RIGHT: pygame.Rect(2, 2, -4, -4),
    },

    TileType.STRONG_BARRIER: {

        RotationType.UP: pygame.Rect(2, 2, -4, -4),
        RotationType.DOWN: pygame.Rect(2, 2, -4, -4),
        RotationType.LEFT: pygame.Rect(2, 2, -4, -4),
        RotationType.RIGHT: pygame.Rect(2, 2, -4, -4),
    },

    TileType.STRONGER_BARRIER: {

        RotationType.UP: pygame.Rect(2, 2, -4, -4),
        RotationType.DOWN: pygame.Rect(2, 2, -4, -4),
        RotationType.LEFT: pygame.Rect(2, 2, -4, -4),
        RotationType.RIGHT: pygame.Rect(2, 2, -4, -4),
    },

    TileType.CRATE: {

        RotationType.UP: pygame.Rect(2, 2, -4, -4),
        RotationType.DOWN: pygame.Rect(2, 2, -4, -4),
        RotationType.LEFT: pygame.Rect(2, 2, -4, -4),
        RotationType.RIGHT: pygame.Rect(2, 2, -4, -4),
    },

    TileType.SOLAR_PANEL: {

        RotationType.UP: pygame.Rect(0, 6, -2, -10),
        RotationType.DOWN: pygame.Rect(0, 6, -2, -10),
        RotationType.LEFT: pygame.Rect(5, 1, -11, -4),
        RotationType.RIGHT: pygame.Rect(5, 1, -11, -4),
    },

    TileType.GREEN_TOWER: {

        RotationType.UP: pygame.Rect(0, 64, 0, -64),
        RotationType.DOWN: pygame.Rect(0, 64, 0, -64),
    }
}

def convertToItemType(tileType: TileType):

    if(tileType == None):
        return None

    match(tileType):

        case tileType.SOLAR_PANEL:
            return ItemType.SOLAR_PANEL

        case tileType.BARRIER:
            return ItemType.BARRIER

        case tileType.STRONG_BARRIER:
            return ItemType.STRONG_BARRIER

        case tileType.STRONGER_BARRIER:
            return ItemType.STRONGER_BARRIER

        case tileType.CRATE:
            return ItemType.CRATE

        case tileType.GREEN_TOWER:
            return ItemType.GREEN_TOWER

class dirType(Enum):

    HORIZONTAL = 0
    VERTICAL = 1 

def isRightSnapConfig(snapType: SnapType, selectedTile, directionType: dirType, mouseRect: pygame.Rect):

    match(snapType):

        case SnapType.RIGHT_SIDE:

            return (

                (selectedTile.rotation == RotationType.DOWN or selectedTile.rotation == RotationType.UP) and
                    selectedTile.getDestRect().x + selectedTile.getDestRect().width <= mouseRect.x and
                    selectedTile.getDestRect().y <= mouseRect.y and
                    selectedTile.getDestRect().y + selectedTile.getDestRect().height >= mouseRect.y
            ) if(directionType == dirType.HORIZONTAL) else (   

                    (selectedTile.rotation == RotationType.LEFT or selectedTile.rotation == RotationType.RIGHT) and
                    selectedTile.getDestRect().x + selectedTile.getDestRect().width < mouseRect.x and 
                    selectedTile.getDestRect().y <= mouseRect.y and
                    selectedTile.getDestRect().y + selectedTile.getDestRect().height >= mouseRect.y
                )

        case SnapType.LEFT_SIDE:

            return(

                (selectedTile.rotation == RotationType.DOWN or selectedTile.rotation == RotationType.UP) and
                selectedTile.getDestRect().x >= mouseRect.x and 
                selectedTile.getDestRect().y <= mouseRect.y and
                selectedTile.getDestRect().y + selectedTile.height >= mouseRect.y
            ) if(directionType == dirType.HORIZONTAL) else (

                (selectedTile.rotation == RotationType.LEFT or selectedTile.rotation == RotationType.RIGHT) and
                selectedTile.getDestRect().x > mouseRect.x and
                selectedTile.getDestRect().y <= mouseRect.y and
                selectedTile.getDestRect().y + selectedTile.getDestRect().height >= mouseRect.y  
            )

        case SnapType.DOWN_SIDE:

            return (

                (selectedTile.rotation == RotationType.DOWN or selectedTile.rotation == RotationType.UP) and
                selectedTile.getDestRect().y + selectedTile.getDestRect().height + snapdetect2Adj.y <= mouseRect.y and
                selectedTile.getDestRect().x <= mouseRect.x and  
                selectedTile.getDestRect().x + selectedTile.getDestRect().width >= mouseRect.x
            ) if(directionType == dirType.HORIZONTAL) else (

                (selectedTile.rotation == RotationType.LEFT or selectedTile.rotation == RotationType.RIGHT) and
                selectedTile.getDestRect().y >= mouseRect.y and
                selectedTile.getDestRect().x <= mouseRect.x and  
                selectedTile.getDestRect().x + selectedTile.getDestRect().width >= mouseRect.x
            )
            
        case SnapType.UP_SIDE:

            return (

                (selectedTile.rotation == RotationType.DOWN or selectedTile.rotation == RotationType.UP) and
                selectedTile.getDestRect().y >= mouseRect.y and
                selectedTile.getDestRect().x <= mouseRect.x and  
                selectedTile.getDestRect().x + selectedTile.getDestRect().width >= mouseRect.x
            ) if(directionType == dirType.HORIZONTAL) else (

                (selectedTile.rotation == RotationType.LEFT or selectedTile.rotation == RotationType.RIGHT) and
                selectedTile.getDestRect().y + selectedTile.getDestRect().height <= mouseRect.y and
                selectedTile.getDestRect().x <= mouseRect.x and  
                selectedTile.getDestRect().x + selectedTile.getDestRect().width >= mouseRect.x
            )