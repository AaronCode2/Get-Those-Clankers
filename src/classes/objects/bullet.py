import classes.utility.utils as utils
import classes.bots.bot as bot
import pygame
from time import time

bullets = []

class Bullet():

    botsToDetect = []

    def __init__(self, position: pygame.Vector2, velocity: pygame.Vector2):

        self.position = position
        self.velocity = velocity
        self.destroyBullet = False
        self.timeStamp = int(time())

    def update(self, window):

        self.move()
        self.checkCollision()
        print("PHEW, PHEW")
        return self.draw(window)

    def checkCollision(self):

        for bot in Bullet.botsToDetect:

            if(bot.rect.collidepoint(self.position)):
                self.destroyBullet = True
                Bullet.botsToDetect.remove(bot)
                break

        if(int(time()) - self.timeStamp > utils.bulletDuration):
            self.destroyBullet = True

    @staticmethod
    def giveBots(bots):
        Bullet.botsToDetect = bots

    def move(self):
        
        self.position += self.velocity * utils.deltaTime
    
    def draw(self, window):

        return utils.getDebugRectItem(window, pygame.Rect(self.position.x, self.position.y, 10, 10), (0, 255, 255))