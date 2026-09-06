import classes.utility.utils as utils
import classes.objects.animatedEntity as animatedEntity
import classes.utility.animation as animation
import classes.objects.dropItem as dropItem
import classes.manager.camera as camera
import classes.utility.textures as textures
import pygame
from time import time 

# I know this doesn't iherit from entity, But I don't like inhertiance
# Basic Movement script, so do don't get performance issues
# I burrowed code from other Projects

class Bot(animatedEntity.AnimatedEntity):

    batteryPosForBots = None

    @staticmethod
    def setBatteryPos(batteryPos):
        Bot.batteryPosForBots = batteryPos

    def __init__(self, position: pygame.Vector2, targetPos: pygame.Vector2, type = utils.Bots.DEAFULT):

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
        self.behaviour = utils.BotBehaviour.ANGRY

        self.timeStamp = int(time())

        self.collided = False
        self.stop = False

        self._targetPos = pygame.Vector2(0, 0)
        self.targetPos = targetPos

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

        if self.collided_tile is not None:
            self.muchTile()

    # Object dies and create droppedItem
    # Right now every bot drops an Item, change it if needed

    def muchTile(self):

        # YUMMY! YUM YUM YUM 🍎

        if(int(time()) - self.timeStamp > utils.botCoolDown):

            self.collided_tile.durability -= 1
            self.timeStamp = int(time())


    def __del__(self):

        dropItem.droppedItems.append(dropItem.DropItem(self.position))