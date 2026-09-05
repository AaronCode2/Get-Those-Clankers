import pygame
import classes.utility.textures as textures
import classes.utility.utils as utils
import classes.utility.animation as animation
import random
import math
from time import time

class BatteryGenenator():

    def __init__(self):

        self.position = pygame.Vector2(utils.screenRect.width / 2, utils.screenRect.height / 2)

        # taken as seconds e.g 120seconds = 2mins
        self.timeLeftText = None
        self.timeLeft = 2 
        self.level = utils.BatteryLevel.BATTERY_FULL

        # How many

        self.updateDelay = 1
        self.batteryLevel = utils.BatteryLevel.BATTERY_FULL
        # Meaursed in KWatts/hour, 

        self.wattsGenerated = 106
        self.capacity = 106 
        self.day = 0
        self.timeLeftText = 120

        self.dayTime = 0
        self.daytimeStamp = time()

        self.updateTimeStamp = int(time())
        self.deplateTimeStamp = int(time())

        # Do this, so get rid of milliseconds

        self.updateTimeStamp = int(time())
        self.deplateTimeStamp = int(time())

        self.loadImage()
        self.setupBatteryIndicator()
    # Battery Equation: Time = Load / Battery Capacity

    def setupBatteryIndicator(self):

        self.batteryIndicator = animation.AnimationManager(
            textures.images["batteryIndicator"]["location"],
            textures.images["batteryIndicator"]["FramesY"],
            [textures.images["batteryIndicator"]["FramesX"]] * 6,
            textures.images["batteryIndicator"]["animationNames"],
            2
        )

        self.srcRect = pygame.Rect(

            textures.images["Battery"]["image"]["FrameWidth"] * self.level.value,
            0,
            textures.images["Battery"]["image"]["FrameWidth"],
            textures.images["Battery"]["image"]["FrameHeight"]
        )

        self.batteryIndicator.position = pygame.Vector2(utils.batteryIndicatorPos.x, utils.batteryIndicatorPos.y)
        self.batteryIndicator.level = utils.BatteryLevel.BATTERY_FULL
        self.batteryIndicator.set_animation(textures.images["batteryIndicator"]["animationNames"][self.batteryIndicator.level.value])
        self.batteryIndicator.animation_speed = 1

    def drawHud(self, window):

        textures.drawGuiPlates(window, pygame.Vector2(5, 3), utils.batteryBackgroundHudPos)

        self.timeLeftText = "Time:" + utils.formatToClock(self.timeLeft)
        self.wattsGeneratedText = "Made:" + str(self.wattsGenerated) + "W"
        self.daytext = "Day:" + str(self.day) +"(" + utils.formatTo24Hourclock(self.dayTime) + ")"         

        textTimeLeft = utils.font.render(self.timeLeftText, True, utils.ColorPlattes["Future Blue"])
        textday = utils.font.render(self.daytext, True, utils.ColorPlattes["Future Blue"])
        textwattsMade = utils.font.render(self.wattsGeneratedText, True, utils.ColorPlattes["Future Blue"])

        window.blit(textTimeLeft, utils.BatteryDisplayHudPositions["TimeLeft"])
        window.blit(textday, utils.BatteryDisplayHudPositions["Day"])
        window.blit(textwattsMade, utils.BatteryDisplayHudPositions["WattsGenerated"])

        self.batteryIndicator.update()
        window.blit(self.batteryIndicator.current_frame, self.batteryIndicator.position)

    def update(self, window, tiles, playerVelocity):

        self.updateStatus(tiles, playerVelocity)
        self.updateDay()

        self.batteryDeplation()

        self.drawHud(window)
        return self.draw(window)

    def updateDay(self):

        if(time() - self.daytimeStamp > 0.5):

            self.dayTime += 1
            self.daytimeStamp = time()

        # A day is 600 seconds or 10mins, I didn't test if it works

        if(self.dayTime >= utils.fullDay):

            self.day += 1
            self.dayTime = 0

    def handleGridImports(self, tiles):

        generatedImports = 0

        for tile in tiles:

            if(tile.type == utils.TileType.SOLAR_PANEL):
                generatedImports += random.randint(utils.solarImportMin, utils.solarImportMax)

        if(self.wattsGenerated + generatedImports <= self.capacity):
            self.wattsGenerated += generatedImports

    def updateStatus(self, tiles, playerVelocity):

        if(int(time()) - self.updateTimeStamp >= self.updateDelay):

            self.handleGridExports(tiles, playerVelocity)
            self.handleGridImports(tiles)
            self.updateTimeStamp = int(time())

    def batteryDeplation(self):

        self.timeLeft = math.ceil((self.wattsGenerated) * utils.batteryStages)

        percentage = math.ceil((self.wattsGenerated / self.capacity) * 100) 

        #! There is Battery Animation Bug! [BUG]

        for i in range(utils.batteryStages):

            if(percentage >= i * 20 and utils.BatteryLevel(utils.batteryStages - i) != self.batteryLevel):
                self.setBatteryLevel(utils.BatteryLevel(utils.batteryStages - i))
        # if(time() - int(self.timeStamp) >= self.timeLeft):

        #     self.timeStamp = time()
        #     if(self.level != utils.BatteryLevel.BATTERY_EMPTY):

        #         self.level = utils.BatteryLevel(self.level.value + 1)
        #         self.srcRect.x = float(textures.images["Battery"]["image"]["FrameWidth"] * self.level.value)
        #         self.batteryIndicator.set_animation(textures.images["batteryIndicator"]["animationNames"][self.level.value])
        #     else:
        #         self.dead = True

    def setBatteryLevel(self, batteryLevel):

        self.batteryLevel = batteryLevel
        self.srcRect.x = float(textures.images["Battery"]["image"]["FrameWidth"] * batteryLevel.value)
        self.batteryIndicator.set_animation(textures.images["batteryIndicator"]["animationNames"][batteryLevel.value])

    def handleGridExports(self, tiles, playerVelocity):

        for tile in tiles:

            if (tile.type == utils.TileType.GREEN_TOWER):
                self.wattsGenerated -= random.randint(10, 80)

        if (playerVelocity != pygame.Vector2(0, 0)):
            self.wattsGenerated -= 1

        self.wattsGenerated -= random.randint(utils.batterydelateMin, utils.batterydelateMax)

    def draw(self, window):

        return textures.images["Battery"]["image"]["surface"], self.position, self.srcRect, self.position.y + (self.srcRect.height/2)

    def loadImage(self):

        textures.images["Battery"]["image"]["surface"] = pygame.image.load(
            textures.images["Battery"]["location"]
        ).convert_alpha()

        textures.images["Battery"]["image"]["surface"] = pygame.transform.scale2x(textures.images["Battery"]["image"]["surface"]).convert_alpha()

        textures.images["Battery"]["image"]["FrameWidth"] = textures.images["Battery"]["image"]["surface"].width / textures.images["Battery"]["maxFramesX"]
        textures.images["Battery"]["image"]["FrameHeight"] = textures.images["Battery"]["image"]["surface"].height / textures.images["Battery"]["FramesY"]
        