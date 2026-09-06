import classes.utility.utils as utils
import classes.objects.bullet as bullet
import classes.bots.bot as bot
import random
import pygame

bots = []

class BotManager():

    cameraOffset = pygame.Vector2()

    def __init__(self, cameraOffset):

        self.raidLevel = 1
        self.botCounter = 0
        BotManager.cameraOffset = cameraOffset

    def update(self):

        self.deployBots()

    def deployBots(self):
        pass

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