import classes.utility.utils as utils
import classes.objects.bullet as bullet
import classes.bots.bot as bot
import random
import pygame
import time

bots = []

class BotManager():

    cameraOffset = pygame.Vector2()

    def __init__(self, cameraOffset):

        self.raidLevel = 1
        self.botCounter = 0

        self.day = 0
        self.dayTime = 0

        self.isBotToSpawn = False

        self.randomTimerSpawner = int(time.time())

        BotManager.cameraOffset = cameraOffset

    def setStuff(self, newDay, newDayTime):

        if(self.day != newDay):
            self.isBotToSpawn = True

        self.day = newDay
        self.dayTime = newDayTime

    def update(self):

        self.deployBots()

    def deployBots(self):

        if(self.isBotToSpawn):

            amount = 30 * self.day

            self.spawnBot(amount)
            self.isBotToSpawn = False

        if(int(time.time()) - self.randomTimerSpawner > 10):

            chance = random.randint(1, 100)

            if(chance < 25): # 25%
                self.spawnBot(random.randint(1, 10))
            
            self.randomTimerSpawner = int(time.time()) 
        

    def regularSpawns(self):
        pass

    def spawnBot(self, amount: int): 

        for i in range(amount):

            whereBotAppear = utils.BotAppearings(random.randint(0, 3))
            extraSpace = utils.BotsSpaceings

            targetChance = random.randint(0, 100)

            match(whereBotAppear):

                case utils.BotAppearings.SIDE_RIGHT_SCREEN:

                    x = -extraSpace + BotManager.cameraOffset.x
                    y = random.randint(-extraSpace, utils.screenRect.height + extraSpace) + BotManager.cameraOffset.y

                case utils.BotAppearings.SIDE_LEFT_SCREEN:

                    x = utils.screenRect.width + extraSpace + BotManager.cameraOffset.x
                    y = random.randint(-extraSpace, utils.screenRect.height + extraSpace) + BotManager.cameraOffset.y

                case utils.BotAppearings.SIDE_TOP_SCREEN:

                    x = random.randint(-extraSpace, utils.screenRect.width + extraSpace) + BotManager.cameraOffset.x
                    y = -extraSpace + BotManager.cameraOffset.y

                case utils.BotAppearings.SIDE_BOTTOM_SCREEN:

                    x = random.randint(-extraSpace, utils.screenRect.width + extraSpace) + BotManager.cameraOffset.x
                    y = utils.screenRect.height + extraSpace + BotManager.cameraOffset.y

            if(targetChance < 30):
                bots.append(bot.Bot(pygame.Vector2(x, y), utils.BotTarget.PLAYER))
            else:
                bots.append(bot.Bot(pygame.Vector2(x, y), utils.BotTarget.BATTERY))