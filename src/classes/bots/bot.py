import classes.utility.utils as utils
import classes.objects.animatedEntity as animatedEntity
import classes.utility.animation as animation
import classes.objects.dropItem as dropItem
import classes.manager.camera as camera
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
        anim = animation.AnimationManager(
            asset_path = "player/player.png",
            num_of_animations = 3,
            animations_num_frames = [4, 4, 4],
            animations_names = ["idle", "walk", "hit"],
            scale_factor = 3
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
        self.velocity = (self._targetPos - self.hitbox.center).normalize() * self.speed

    def update(self, tiles):
        if self.rect.collidepoint(self.targetPos.x, self.targetPos.y):
            self.velocity = pygame.Vector2(0.0, 0.0)
        super().update(collision_tiles=tiles)
    # Object dies and create droppedItem
    # Right now every bot drops an Item, change it if needed

    def __del__(self):

        dropItem.droppedItems.append(dropItem.DropItem(self.position))