import classes.utility.utils as utils
import classes.utility.animation as animation
import pygame

# I know this doesn't iherit from entity, But I don't like inhertiance

class Bot():

    def __init__(self, type, position, targetPos):

        self.type = type
        self.position = position
        self.velocity = pygame.Vector2(0, 0)
        self.width = utils.defaultImageSizes
        self.height = utils.defaultImageSizes

        self.targetPos = targetPos

    def update(self, window, tiles):

        self.draw(window)

    def move(self):

        self.velocity = pygame.Vector2(0, 0)

        self.position.x += self.velocity.x
        self.position.y += self.velocity.y

    # Basic Movement script, so do don't get performance issues

    def aiPathFinder(self):
        pass

    def draw(self, window):

        utils.debugDraw(window, pygame.Rect(
            self.position.x, self.position.y, 
            self.width, self.height
        ))