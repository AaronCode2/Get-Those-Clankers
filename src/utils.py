import pygame
from enum import Enum

# For constants and utility

deltaTime = 0.3

screenRect = pygame.Rect()
windowResized = False

class TileType(Enum):

    BARRIER = 0
    SOLAR_PANEL = 1
    BATTERY_FULL = 2
    BATTERY_DRAIN_1 = 3
    BATTERY_DRAIN_2 = 4
    BATTERY_DRAIN_3 = 5
    BATTERY_DRAIN_4 = 6
    BATTERY_EMPTY = 7