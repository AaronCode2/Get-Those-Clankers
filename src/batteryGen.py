import pygame
import textures
import utils

class BatteryGenenator():

    def __init__(self):

        self.position = pygame.Vector2(utils.screenRect.width / 2, utils.screenRect.height / 2)

        # taken as seconds e.g 120seconds = 2mins
        self.timer = 120
        self.level = utils.BatteryLevel.BATTERY_FULL 

        self.loadImage()

        self.srcRect = pygame.Rect(

            textures.images["Battery"]["image"]["FrameWidth"] * self.level.value,
            0,
            textures.images["Battery"]["image"]["FrameWidth"],
            textures.images["Battery"]["image"]["FrameHeight"]
        )

    def loadImage(self):

        textures.images["Battery"]["image"]["surface"] = pygame.image.load(
            textures.images["Battery"]["location"]
        ).convert_alpha()

        textures.images["Battery"]["image"]["surface"] = pygame.transform.scale2x(textures.images["Battery"]["image"]["surface"]).convert_alpha()

        textures.images["Battery"]["image"]["FrameWidth"] = textures.images["Battery"]["image"]["surface"].width / textures.images["Battery"]["maxFramesX"]
        textures.images["Battery"]["image"]["FrameHeight"] = textures.images["Battery"]["image"]["surface"].height / textures.images["Battery"]["FramesY"]


    def update(self, window):

        self.draw(window)

    def draw(self, window):

        window.blit(textures.images["Battery"]["image"]["surface"], self.position, self.srcRect)