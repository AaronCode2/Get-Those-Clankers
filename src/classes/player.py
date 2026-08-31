import pygame
from entity import Entity
from animation import AnimationManager
from animatedEntity import AnimatedEntity

class Player(AnimatedEntity):
    def __init__(self, position: pygame.Vector2):
        animation = AnimationManager("player/palyer.png", 2, [4, 4], ["walk", "idle"])

        super().__init__(position, animation, (20, 15))