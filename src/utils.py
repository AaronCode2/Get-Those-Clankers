import pygame
from enum import Enum

# For constants and utility

deltaTime = 0.3

screenRect = pygame.Rect()
windowResized = False

class TileType(Enum):

    BARRIER = 0
    SOLAR_PANEL = 1
    BATTERY = 2