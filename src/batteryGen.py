import pygame
import textures
import utils

class BatteryGenenator():

    def __init__(self):

        self.position = pygame.Vector2(utils.screenRect.width / 2, utils.screenRect.height / 2)

        # taken as seconds e.g 120seconds = 2mins
        self.timer = 120

        self.srcRect = pygame.Rect(

            textures.images["Tile"]
        )