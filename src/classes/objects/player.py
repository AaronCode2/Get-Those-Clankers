import pygame
from animation import AnimationManager
from animatedEntity import AnimatedEntity
from src.classes.utility import utils
from src.classes.objects.animation import AnimationManager
from src.classes.objects.animatedEntity import AnimatedEntity
import classes.utility.utils as utils

class Player(AnimatedEntity):
    def __init__(self, position: pygame.Vector2):
        animation = AnimationManager("player/palyer.png", 2, [4, 4], ["walk", "idle"])

        super().__init__(position, animation, (20, 15))

    def update(self):
        super().update()

player = Player(pygame.Vector2(1, 1))
player.rect