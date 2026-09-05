import classes.utility.utils as utils
import classes.utility.animation as animation
import classes.objects.dropItem as dropItem
import classes.manager.camera as camera
import pygame
from time import time 

# I know this doesn't iherit from entity, But I don't like inhertiance
# Basic Movement script, so do don't get performance issues
# I burrowed code from other Projects

class Bot():

    batteryPosForBots = None

    @staticmethod
    def setBatteryPos(batteryPos):
        Bot.batteryPosForBots = batteryPos

    def __init__(self, position: pygame.Vector2, targetPos: pygame.Vector2, type = utils.Bots.DEAFULT):

        self.type = type
        self.position = position
        self.velocity = pygame.Vector2(0, 0)
        self.width = utils.defaultImageSizes
        self.height = utils.defaultImageSizes

        self.health = 100
        self.speed = 100
        self.behaviour = utils.BotBehaviour.ANGRY

        self.timeStamp = int(time())

        self.collided = False
        self.stop = False

        self.targetPos = targetPos

    def update(self, window, tiles):

        self.updateRect()
        self.move(tiles)
        return self.draw(window)

    def updateRect(self):

        self.rect = pygame.Rect(
            self.position.x,
            self.position.y,
            self.width,
            self.height
        )

        self.hitBox = self.rect


    def move(self, tiles):

        self.velocity = pygame.Vector2(0, 0)

        if(not pygame.Rect(self.rect).collidepoint(self.targetPos)):
            self.aiPathFinder()

        if(self.stop):
            self.velocity = pygame.Vector2(0, 0)


        self.position.x += self.velocity.x * utils.deltaTime
        self.collisionX(tiles)


        self.position.y += self.velocity.y * utils.deltaTime
        self.collisionY(tiles)

    def collisionX(self, tiles):

        self.updateRect()

        for tile in tiles:

            if(tile.getHitBox().colliderect(self.rect)):

                match(self.behaviour):

                    case utils.BotBehaviour.TRIED:
                            
                        if(self.velocity.x > 0):
                            
                            offset = self.hitBox.x - self.position.x + self.hitBox.width
                            
                            self.position.x = tile.getHitBox().x - offset - utils.colladjust
                            
                        
                        if(self.velocity.x < 0):
                            
                            offset = self.hitBox.x - self.position.x
                            
                            self.position.x = tile.getHitBox().x + tile.getHitBox().width - offset + utils.colladjust

                        self.velocity.x = 0

                    case utils.BotBehaviour.ANGRY:

                        self.stop = True
                        
                        if(int(time()) - self.timeStamp > 2):

                            if(tile.durability > 0):
                                tile.durability -= 1
                                print("DESTROYING MUCH! MUCH!")
                            else:
                                self.stop = False
                                tiles.remove(tile)
                                print("X-X")

                            self.timeStamp = int(time())

    def collisionY(self, tiles):
        
        self.updateRect()

        self.stop = False

        for tile in tiles:

            if(tile.getHitBox().colliderect(self.rect)):

                match(self.behaviour):

                    case utils.BotBehaviour.TRIED:

                        if(self.velocity.y > 0):
                                
                            offset = self.hitBox.y - self.position.y + self.hitBox.height
                                
                            self.position.y = tile.getHitBox().y - offset - utils.colladjust
                                
                            
                        if(self.velocity.y < 0):
                                
                            offset = self.hitBox.y - self.position.y
                                
                            self.position.y = tile.getHitBox().y + tile.getHitBox().height - offset + utils.colladjust

                        self.velocity.y = 0
                            
                    case utils.BotBehaviour.ANGRY:
                        
                        self.stop = True

                        if(int(time()) - self.timeStamp > 2):

                            if(tile.durability > 0):
                                tile.durability -= 1
                                print("DESTROYING MUCH! MUCH!")
                            else:
                                self.stop = False
                                tiles.remove(tile)
                                print("X-X")

                            self.timeStamp = int(time())

    def aiPathFinder(self):

        self.velocity = (self.targetPos - self.position).normalize() * self.speed


    def draw(self, window):

        # if(utils.screenRect.colliderect(pygame.Rect(self.rect))):
        return utils.getDebugRectItem(window, pygame.Rect(self.rect))

    # Object dies and create droppedItem
    # Right now every bot drops an Item, change it if needed

    def __del__(self):

        dropItem.droppedItems.append(dropItem.DropItem(self.position))