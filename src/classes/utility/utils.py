import pygame
from enum import Enum

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

class TypeOfGuiPlates(Enum):

    NORMAL = 0
    MARGIN = 1

class Bots(Enum):

    DEAFULT = 0

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

detectBoxAdj = pygame.Vector2(10, -20)

keyGuidesTexts = {

    KeyGuides.CRTL_TO_SNAP: "Snap Mode",
    KeyGuides.WASD_TO_MOVE: "Move",
    KeyGuides.R_TO_ROTATE: "Rotate Object",

    "textOffsets": {

        KeyGuides.CRTL_TO_SNAP: 0,
        KeyGuides.WASD_TO_MOVE: 160,
        KeyGuides.R_TO_ROTATE: 230,
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

def convertToTileType(ItemType: ItemType):

    match(ItemType):

        case ItemType.SOLAR_PANEL:
            return TileType.SOLAR_PANEL

        case ItemType.BARRIER:
            return TileType.BARRIER

        case _:
            return None

screenRect = pygame.Rect()
windowResized = False

hotBarSizeWidth = 64 * 6
hotBarSizeHeight = 64 * 2

activateTilePlacer = True

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

inventoryStackSize = 84

snapdetectAdj = pygame.Vector2(-5, -5)
snapdetect2Adj = pygame.Vector2(-5, -48)
snapdetect3Adj = pygame.Vector2(-2, -10)

defaultImageSizes = 64

scrollWheel = pygame.Vector2(0, 0)
tileMaxFrames = 1.0

batteryIndicatorPos = pygame.Vector2(200, 30)

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

    match (selectedTile.type):

        case TileType.BARRIER:

            if rotationType == RotationType.DOWN or rotationType == RotationType.UP:
                match(snapType):

                    case SnapType.RIGHT_SIDE:

                        return pygame.Rect(
                            selectedTile.position.x + defaultImageSizes + snapdetectAdj.x,
                            selectedTile.position.y,
                            defaultImageSizes, defaultImageSizes
                        )
                    case SnapType.LEFT_SIDE:

                        return pygame.Rect(
                            selectedTile.position.x - defaultImageSizes - snapdetectAdj.x,
                            selectedTile.position.y,
                            defaultImageSizes, defaultImageSizes
                        )
                    case SnapType.DOWN_SIDE:

                        return pygame.Rect(
                            selectedTile.position.x,
                            selectedTile.position.y + defaultImageSizes + snapdetect2Adj.y,
                            defaultImageSizes, defaultImageSizes
                        )
                    case SnapType.UP_SIDE:

                        return pygame.Rect(
                            selectedTile.position.x,
                            selectedTile.position.y - defaultImageSizes - snapdetect2Adj.y,
                            defaultImageSizes, defaultImageSizes
                        )
            else:

                match(snapType):

                    case SnapType.UP_SIDE:

                        return pygame.Rect(
                            selectedTile.position.x,
                            selectedTile.position.y + defaultImageSizes + snapdetectAdj.y,
                            defaultImageSizes, defaultImageSizes
                        )
                    case SnapType.DOWN_SIDE:

                        return pygame.Rect(
                            selectedTile.position.x,
                            selectedTile.position.y - defaultImageSizes - snapdetectAdj.y,
                            defaultImageSizes, defaultImageSizes
                        )
                    case SnapType.RIGHT_SIDE:

                        return pygame.Rect(
                            selectedTile.position.x + defaultImageSizes + snapdetect2Adj.y,
                            selectedTile.position.y,
                            defaultImageSizes, defaultImageSizes
                        )
                    case SnapType.LEFT_SIDE:

                        return pygame.Rect(
                            selectedTile.position.x - defaultImageSizes - snapdetect2Adj.y,
                            selectedTile.position.y,
                            defaultImageSizes, defaultImageSizes
                        )

        case TileType.SOLAR_PANEL:

            if rotationType == RotationType.DOWN or rotationType == RotationType.UP:
                match(snapType):

                    case SnapType.RIGHT_SIDE:

                        return pygame.Rect(
                            selectedTile.position.x + defaultImageSizes + snapdetect3Adj.x,
                            selectedTile.position.y,
                            defaultImageSizes, defaultImageSizes
                        )
                    case SnapType.LEFT_SIDE:

                        return pygame.Rect(
                            selectedTile.position.x - defaultImageSizes - snapdetect3Adj.x,
                            selectedTile.position.y,
                            defaultImageSizes, defaultImageSizes
                        )
                    case SnapType.DOWN_SIDE:

                        return pygame.Rect(
                            selectedTile.position.x,
                            selectedTile.position.y + defaultImageSizes + snapdetect3Adj.y,
                            defaultImageSizes, defaultImageSizes
                        )
                    case SnapType.UP_SIDE:

                        return pygame.Rect(
                            selectedTile.position.x,
                            selectedTile.position.y - defaultImageSizes - snapdetect3Adj.y,
                            defaultImageSizes, defaultImageSizes
                        )
            else:

                match(snapType):

                    case SnapType.UP_SIDE:

                        return pygame.Rect(
                            selectedTile.position.x,
                            selectedTile.position.y + defaultImageSizes,
                            defaultImageSizes, defaultImageSizes
                        )
                    case SnapType.DOWN_SIDE:

                        return pygame.Rect(
                            selectedTile.position.x,
                            selectedTile.position.y - defaultImageSizes,
                            defaultImageSizes, defaultImageSizes
                        )
                    case SnapType.RIGHT_SIDE:

                        return pygame.Rect(
                            selectedTile.position.x + defaultImageSizes + snapdetect3Adj.y,
                            selectedTile.position.y,
                            defaultImageSizes, defaultImageSizes
                        )
                    case SnapType.LEFT_SIDE:

                        return pygame.Rect(
                            selectedTile.position.x - defaultImageSizes - snapdetect3Adj.y,
                            selectedTile.position.y,
                            defaultImageSizes, defaultImageSizes
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

BatteryDisplayHudPositions = {

    "TimeLeft": pygame.Vector2(12, 30),
    "WattsGenerated": pygame.Vector2(13, 65),
    "Day": pygame.Vector2(13, 100)
}

ColorPlattes = {

    "Future Blue": (39, 137, 205),
    "Supreme Yellow": (248, 197, 58),
    "Pale White": (236, 235, 231),
    "Glass Orange": (241, 100, 31),
    "Grey Cloud": (128, 123, 128)
}

def formatToClock(seconds: int):

    clockMins = seconds // 60

    clockSeconds = str(abs((clockMins * 60) - seconds))

    return str(clockMins) + ":" + clockSeconds

def debugDraw(window, destRect: pygame.Rect, color = (255, 0, 0)):

    rect = pygame.Surface((destRect.width, destRect.height))
    rect.set_alpha(100)
    rect.fill(color)
    window.blit(rect, (destRect.x, destRect.y))

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

def convertToItemType(tileType: TileType):

    if(tileType == None):
        return None

    match(tileType):

        case tileType.SOLAR_PANEL:
            return ItemType.SOLAR_PANEL

        case tileType.BARRIER:
            return ItemType.BARRIER

class dirType(Enum):

    HORIZONTAL = 0
    VERTICAL = 1 

def isRightSnapConfig(snapType: SnapType, selectedTile, directionType: dirType, mouseRect: pygame.Rect):

    match(snapType):

        case SnapType.RIGHT_SIDE:

            return (

                (selectedTile.rotation == RotationType.DOWN or selectedTile.rotation == RotationType.UP) and
                    selectedTile.position.x + defaultImageSizes <= mouseRect.x and
                    selectedTile.position.y <= mouseRect.y and
                    selectedTile.position.y + defaultImageSizes >= mouseRect.y
            ) if(directionType == dirType.HORIZONTAL) else (   

                    (selectedTile.rotation == RotationType.LEFT or selectedTile.rotation == RotationType.RIGHT) and
                    selectedTile.position.x + defaultImageSizes < mouseRect.x and 
                    selectedTile.position.y <= mouseRect.y and
                    selectedTile.position.y + defaultImageSizes >= mouseRect.y
                )

        case SnapType.LEFT_SIDE:

            return(

                (selectedTile.rotation == RotationType.DOWN or selectedTile.rotation == RotationType.UP) and
                selectedTile.position.x >= mouseRect.x and 
                selectedTile.position.y <= mouseRect.y and
                selectedTile.position.y + defaultImageSizes >= mouseRect.y
            ) if(directionType == dirType.HORIZONTAL) else (

                (selectedTile.rotation == RotationType.LEFT or selectedTile.rotation == RotationType.RIGHT) and
                selectedTile.position.x > mouseRect.x and
                selectedTile.position.y <= mouseRect.y and
                selectedTile.position.y + defaultImageSizes >= mouseRect.y  
            )

        case SnapType.DOWN_SIDE:

            return (

                (selectedTile.rotation == RotationType.DOWN or selectedTile.rotation == RotationType.UP) and
                selectedTile.position.y + defaultImageSizes + snapdetect2Adj.y <= mouseRect.y and
                selectedTile.position.x <= mouseRect.x and  
                selectedTile.position.x + defaultImageSizes >= mouseRect.x
            ) if(directionType == dirType.HORIZONTAL) else (

                (selectedTile.rotation == RotationType.LEFT or selectedTile.rotation == RotationType.RIGHT) and
                selectedTile.position.y >= mouseRect.y and
                selectedTile.position.x <= mouseRect.x and  
                selectedTile.position.x + defaultImageSizes >= mouseRect.x
            )
            
        case SnapType.UP_SIDE:

            return (

                (selectedTile.rotation == RotationType.DOWN or selectedTile.rotation == RotationType.UP) and
                selectedTile.position.y >= mouseRect.y and
                selectedTile.position.x <= mouseRect.x and  
                selectedTile.position.x + defaultImageSizes >= mouseRect.x
            ) if(directionType == dirType.HORIZONTAL) else (

                (selectedTile.rotation == RotationType.LEFT or selectedTile.rotation == RotationType.RIGHT) and
                selectedTile.position.y + defaultImageSizes <= mouseRect.y and
                selectedTile.position.x <= mouseRect.x and  
                selectedTile.position.x + defaultImageSizes >= mouseRect.x
            )