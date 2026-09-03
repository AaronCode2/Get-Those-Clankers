import pygame
import classes.utility.textures as textures
import classes.utility.utils as utils
import classes.utility.animation as animation
from time import time

class BatteryGenenator():

    def __init__(self):

        self.position = pygame.Vector2(utils.screenRect.width / 2, utils.screenRect.height / 2)

        # taken as seconds e.g 120seconds = 2mins
        self.timeLeftText = None
        self.timeLeft = 120 
        self.level = utils.BatteryLevel.BATTERY_FULL

        # Meaursed in KWatts/hour, 

        self.wattsGenereated = 1
        self.capacity = 60 

        self.timeStamp = int(time())

        self.loadImage()

        self.batteryIndicator = animation.AnimationManager(
            textures.images["batteryIndicator"]["location"],
            textures.images["batteryIndicator"]["FramesY"],
            [textures.images["batteryIndicator"]["FramesX"]] * 6,
            textures.images["batteryIndicator"]["animationNames"],
            True
        )

        self.srcRect = pygame.Rect(

            textures.images["Battery"]["image"]["FrameWidth"] * self.level.value,
            0,
            textures.images["Battery"]["image"]["FrameWidth"],
            textures.images["Battery"]["image"]["FrameHeight"]
        )

        # How many days played

        self.day = "0"
        self.wattsGenerated = "10W"
        self.timeLeftText = 120

        self.batteryIndicator.position = pygame.Vector2(utils.batteryIndicatorPos.x, utils.batteryIndicatorPos.y)
        self.batteryIndicator.level = utils.BatteryLevel.BATTERY_FULL
        self.batteryIndicator.set_animation(textures.images["batteryIndicator"]["animationNames"][self.batteryIndicator.level.value])
        self.batteryIndicator.animation_speed = 1

    # Battery Equation: Time = Load / Battery Capacity

    def drawHud(self, window):

        textures.drawGuiPlates(window, pygame.Vector2(4, 3), pygame.Vector2(10, 10))

        self.timeLeftText = "Time:" + utils.formatToClock(self.timeLeft)
        self.wattsGeneratedText = "Used:" + str(self.wattsGenerated) + "W"
        self.daytext = "Day:" + str(self.day)        

        textTimeLeft = utils.font.render(self.timeLeftText, True, utils.ColorPlattes["Future Blue"])
        textWattsUsed = utils.font.render(self.daytext, True, utils.ColorPlattes["Future Blue"])
        textwattsMade = utils.font.render(self.wattsGeneratedText, True, utils.ColorPlattes["Future Blue"])

        window.blit(textTimeLeft, utils.BatteryDisplayHudPositions["TimeLeft"])
        window.blit(textWattsUsed, utils.BatteryDisplayHudPositions["WattsUsed"])
        window.blit(textwattsMade, utils.BatteryDisplayHudPositions["WattsGenerated"])

        # The utils.deltaTime might be causing this Julien - thanks for fixing it

        self.batteryIndicator.update()
        window.blit(self.batteryIndicator.current_frame, self.batteryIndicator.position)

    def getBatteryduration(load: float):
        pass

    def loadImage(self):

        textures.images["Battery"]["image"]["surface"] = pygame.image.load(
            textures.images["Battery"]["location"]
        ).convert_alpha()

        textures.images["Battery"]["image"]["surface"] = pygame.transform.scale2x(textures.images["Battery"]["image"]["surface"]).convert_alpha()

        textures.images["Battery"]["image"]["FrameWidth"] = textures.images["Battery"]["image"]["surface"].width / textures.images["Battery"]["maxFramesX"]
        textures.images["Battery"]["image"]["FrameHeight"] = textures.images["Battery"]["image"]["surface"].height / textures.images["Battery"]["FramesY"]
        

    def update(self, window, tiles):


        self.batteryDeplation()
        self.draw(window)
        self.drawHud(window)

    def batteryDeplation(self):

        if(time() - int(self.timeStamp) >= self.timeLeft):

            self.timeStamp = time()
            if(self.level != utils.BatteryLevel.BATTERY_EMPTY):

                self.level = utils.BatteryLevel(self.level.value + 1)
                self.srcRect.x = float(textures.images["Battery"]["image"]["FrameWidth"] * self.level.value)
                self.batteryIndicator.set_animation(textures.images["batteryIndicator"]["animationNames"][self.level.value])
            else:
                self.dead = True

    def draw(self, window):

        window.blit(textures.images["Battery"]["image"]["surface"], self.position, self.srcRect)