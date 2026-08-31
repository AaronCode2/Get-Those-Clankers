import pygame
from enum import Enum

# For constants and utility

font = None

class keyGuides(Enum):

    CRTL_TO_SNAP = 0
    WASD_TO_MOVE = 1
    R_TO_ROTATE = 2

keyGuidesTexts = {

    keyGuides.CRTL_TO_SNAP: "Snap Mode",
    keyGuides.WASD_TO_MOVE: "Move",
    keyGuides.R_TO_ROTATE: "Rotate Object",

    "textOffsets": {

        keyGuides.CRTL_TO_SNAP: 0,
        keyGuides.WASD_TO_MOVE: 160,
        keyGuides.R_TO_ROTATE: 230,
    } 
}

class RotationType(Enum):

    DOWN = 0
    LEFT = 1
    UP = 2
    RIGHT = 3

deltaTime = 0.3

screenRect = pygame.Rect()
windowResized = False

snapdetectAdj = pygame.Vector2(-5, -5)
snapdetect2Adj = pygame.Vector2(-5, -48)
snapdetect3Adj = pygame.Vector2(-2, -10)

defaultImageSizes = 64

scrollWheel = pygame.Vector2(0, 0)
tileMaxFrames = 1.0

adjmousePos = pygame.Vector2(-24, -24)

class SnapType(Enum):

    RIGHT_SIDE = 0
    LEFT_SIDE = 1
    DOWN_SIDE = 2
    UP_SIDE = 3

def getTileRect(position: pygame.Vector2):
    return pygame.Rect(position.x, position.y, defaultImageSizes, defaultImageSizes)

def getTilesDetectRect(position: pygame.Vector2):

    return pygame.Rect(position.x - 10, position.y - 10, defaultImageSizes - 10, defaultImageSizes - 10)


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