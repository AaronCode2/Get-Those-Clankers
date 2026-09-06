import classes.utility.utils as utils
import classes.objects.animatedEntity as animatedEntity
import classes.utility.animation as animation
import classes.objects.dropItem as dropItem
import classes.manager.camera as camera
import classes.utility.textures as textures
import pygame
from time import time
import random

# I know this doesn't iherit from entity, But I don't like inhertiance
# Basic Movement script, so do don't get performance issues
# I burrowed code from other Projects

class Bot(animatedEntity.AnimatedEntity):

    batteryPosForBots = None
    playerPosForBots = None

    @staticmethod
    def setBatteryPos(batteryPos):
        Bot.batteryPosForBots = batteryPos

    @staticmethod
    def setPlayerPos(playerPos):
        Bot.playerPosForBots = playerPos

    def __init__(self, position: pygame.Vector2, botTarget: utils.BotTarget, type = utils.Bots.DEAFULT):

        # It is bad habit to just add numbers with no actual var name - I fixed it
        
        anim = animation.AnimationManager(
            textures.images["Bot"]["location"],
            textures.images["Bot"]["FramesY"],
            textures.images["Bot"]["FramesX"],
            textures.images["Bot"]["AnimationNames"],
            textures.images["Bot"]["Scale"]
        )
        super().__init__(position, anim, (81, 35))

        self.type = type

        self.health = 100
        self.speed = 100
        self.behaviour = utils.BotBehaviour(random.randint(0, 3))

        self.coolDowntimeStamp = int(time())
        self.targetTimeStamp = int(time())

        self.collided = False
        self.stop = False

        self._targetPos = pygame.Vector2(0, 0)
        self.botTarget = botTarget

        if(self.botTarget == utils.BotTarget.PLAYER):
            self._targetPos = Bot.playerPosForBots
        else:
            self._targetPos = Bot.batteryPosForBots

    @property
    def targetPos(self):
        return self._targetPos

    @targetPos.setter
    def targetPos(self, pos: pygame.Vector2):
        self._targetPos = pos
    def update(self, tiles):
        distance = self._targetPos - self.hitbox.center
        self.velocity = (distance).normalize() * self.speed
        if (self.targetPos - self.rect.center).length() < 50:
            self.velocity = pygame.Vector2(0.0, 0.0)
        super().update(collision_tiles=tiles)

        self.activateBehaviour()

        if(self.botTarget == utils.BotTarget.PLAYER):
            self.updateTargetPosForPlayer()

        if self.collided_tile is not None:
            self.munchTile()

    def updateTargetPosForPlayer(self):
        self._targetPos = Bot.playerPosForBots

    def activateBehaviour(self):

        match(self.behaviour):

            case utils.BotBehaviour.STUIPED:

                if(int(time()) - self.targetTimeStamp > 2):
                    self.targetPos = pygame.Vector2(random.randint(-3000, 3000), random.randint(-3000, 3000))
                    self.targetTimeStamp = int(time())

            case utils.BotBehaviour.SCARED:

                self.targetPos = pygame.Vector2(random.randint(-3000, 3000), random.randint(-3000, 3000))

            case utils.BotBehaviour.TELPORTER:

                if(int(time()) - self.targetTimeStamp > 5):
                    self.position = pygame.Vector2(random.randint(-3000, 3000), random.randint(-3000, 3000))
                    self.targetTimeStamp = int(time())

    def munchTile(self):

        # YUMMY! YUM YUM YUM 🍎

        if(int(time()) - self.coolDowntimeStamp > utils.botCoolDown):

            self.collided_tile.durability -= 1
            self.coolDowntimeStamp = int(time())

    # Object dies and create droppedItem
    # Right now every bot drops an Item, change it if needed

    def __del__(self):

        dropItem.droppedItems.append(dropItem.DropItem(self.position))