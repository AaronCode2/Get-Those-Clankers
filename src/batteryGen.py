import pygame
import textures
import utils
from time import time

class BatteryGenenator():

    def __init__(self):

        self.position = pygame.Vector2(utils.screenRect.width / 2, utils.screenRect.height / 2)

        # taken as seconds e.g 120seconds = 2mins
        self.timeLeft = 30
        self.level = utils.BatteryLevel.BATTERY_FULL

        # Meaursed in KWatts/hour, 

        self.wattsUsed = 12 
        self.wattsGenereated = 1
        self.capacity = 60 

        self.timeStamp = int(time())

        self.loadImage()

        self.srcRect = pygame.Rect(

            textures.images["Battery"]["image"]["FrameWidth"] * self.level.value,
            0,
            textures.images["Battery"]["image"]["FrameWidth"],
            textures.images["Battery"]["image"]["FrameHeight"]
        )

    # Battery Equation: Time = Load / Battery Capacity

    def getBatteryduration(load: float):
        pass

    def loadImage(self):

        textures.images["Battery"]["image"]["surface"] = pygame.image.load(
            textures.images["Battery"]["location"]
        ).convert_alpha()

        textures.images["Battery"]["image"]["surface"] = pygame.transform.scale2x(textures.images["Battery"]["image"]["surface"]).convert_alpha()

        textures.images["Battery"]["image"]["FrameWidth"] = textures.images["Battery"]["image"]["surface"].width / textures.images["Battery"]["maxFramesX"]
        textures.images["Battery"]["image"]["FrameHeight"] = textures.images["Battery"]["image"]["surface"].height / textures.images["Battery"]["FramesY"]
        


    def update(self, window):

        # self.srcRect.x = 10
        
        if(time() - int(self.timeStamp) >= self.timeLeft):

            self.timeStamp = time()
            if(self.level != utils.BatteryLevel.BATTERY_EMPTY):

                self.level = utils.BatteryLevel(self.level.value + 1)
                self.srcRect.x = float(textures.images["Battery"]["image"]["FrameWidth"] * self.level.value)
            else:
                self.dead = True

        self.draw(window)

    def draw(self, window):

        window.blit(textures.images["Battery"]["image"]["surface"], self.position, self.srcRect)