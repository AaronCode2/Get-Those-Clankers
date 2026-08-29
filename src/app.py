import pygame
from game import *

def init():

    pygame.display.set_caption("Pygame Window")
    pygame.init()
    pygame.font.init()

    game = Game(1000, 600, 60)
    game.run()