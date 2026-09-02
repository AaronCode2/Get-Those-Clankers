import pygame
from src.classes.utility.animation import AnimationManager
from src.classes.objects.animatedEntity import AnimatedEntity
import classes.utility.utils as utils

class Player(AnimatedEntity):
    def __init__(self, position: pygame.Vector2):
        animation = AnimationManager("player/player.png", 2, [4, 4], ["walk", "idle"])
        super().__init__(position, animation, (20, 15))
        while True:
            print("hello world")
            


    def update(self):
        super().update()

