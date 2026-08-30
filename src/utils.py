import pygame
from enum import Enum

# For constants and utility

deltaTime = 0.3

screenRect = pygame.Rect()
windowResized = False

snapdetectAdj = pygame.Vector2(-5, -5)
snapdetect2Adj = pygame.Vector2(-5, -48)

defaultImageSizes = 64

scrollWheel = pygame.Vector2(0, 0)
tileMaxFrames = 1.0

adjmousePos = pygame.Vector2(-24, -24)

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

class RotationType(Enum):

    DOWN = 0
    LEFT = 1
    UP = 2
    RIGHT = 3

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