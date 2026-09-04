import classes.utility.utils as utils
import classes.utility.animation as animation
import pygame

# I know this doesn't iherit from entity, But I don't like inhertiance

class Bot():

    def __init__(self, position: pygame.Vector2, targetPos: pygame.Vector2, type = utils.Bots.DEAFULT):

        self.type = type
        self.position = position
        self.velocity = pygame.Vector2(0, 0)
        self.width = utils.defaultImageSizes
        self.height = utils.defaultImageSizes

        self.targetPos = targetPos

    def update(self, window, tiles):

        self.move()
        self.draw(window)

    def move(self):

        self.velocity = pygame.Vector2(0, 0)

        if(not pygame.Rect(self.position.x, self.position.y, self.width, self.height).collidepoint(self.targetPos)):
            self.aiPathFinder()

        self.position.x += self.velocity.x
        self.position.y += self.velocity.y

    # Basic Movement script, so do don't get performance issues
    # I burrowed code from other Projects

    def collisionX(self, tiles):

        for tile in tiles:
            pass
            # if(tile)

    def aiPathFinder(self):

        if(self.position.x < self.targetPos.x):
            self.velocity.x = 100 * utils.deltaTime

        if(self.position.x > self.targetPos.x):
            self.velocity.x = -100 * utils.deltaTime

        if(self.position.y > self.targetPos.y):
            self.velocity.y = -100 * utils.deltaTime

        if(self.position.y < self.targetPos.y):
            self.velocity.y = 100 * utils.deltaTime

    def draw(self, window):

        if(
            utils.screenRect.colliderect(
                pygame.Rect(self.position.x, self.position.y, self.width, self.height)
        )):
            utils.debugDraw(window, pygame.Rect(
                self.position.x, self.position.y, 
                self.width, self.height
            ))