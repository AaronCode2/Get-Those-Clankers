import pygame
import classes.utility.utils as utils
import classes.utility.textures as textures

class Tile:

    def __init__(self, position: pygame.Vector2, type: utils.TileType, rotation: utils.RotationType):

        self.position = position
        self.type = type

        if(type != utils.TileType.GREEN_TOWER):

            self.width = textures.images["Tiles"]["image"]["FrameWidth"]
            self.height = textures.images["Tiles"]["image"]["FrameHeight"]
        else:

            self.width = textures.images["Tower"]["image"]["FrameWidth"]
            self.height = textures.images["Tower"]["image"]["FrameHeight"]

        self._hitBox = pygame.Rect(

            self.position.x + utils.hitBoxAdjForTiles[self.type][rotation].x, 
            self.position.y + utils.hitBoxAdjForTiles[self.type][rotation].y, 
            self.width + utils.hitBoxAdjForTiles[self.type][rotation].width, 
            self.height + utils.hitBoxAdjForTiles[self.type][rotation].height
        )

        self.rotation = rotation

        # How long the tower lasts

        self.durability = utils.durabiltyForTile[type]

        print(type)

        self.setSrcRect()

    def getHitBox(self):
        return self._hitBox

    def update(self, window):

        self.draw(window)
        utils.debugDraw(window, self._hitBox)

    # This func only called if the object is a tower!

    def towerFunc(self, bots):
        pass

    # It's an array of bots, 
    # Bots have bot.health
    # You manually destroy the bots e.g if(bot.health == 0): bots.remove(bot)
    # There is no bullet class, you have to create one

    def draw(self, window):

        if(self.type != utils.TileType.GREEN_TOWER):

            if(self.rotation == utils.RotationType.DOWN):
                window.blit(textures.images["Tiles"]["image"]["surface"], self.position, self.srcRect)
            else:
                window.blit(textures.images["Tiles"]["rotatedImages"][self.rotation], self.position, self.srcRect)

        else:

            # Draw Tower!
            
            window.blit(textures.images["Tower"]["image"]["Animation"].current_frame, self.position)

    def setSrcRect(self):

        # Takes care of rotated image and gets that single frame it needs
        # Towers Should not be rotated

        if(self.type == utils.TileType.GREEN_TOWER):
            return

        match(self.rotation):

            case utils.RotationType.DOWN:

                self.srcRect = pygame.Rect(
                    self.width * float(self.type.value), 
                    0,
                    self.width, self.height
                )

            case utils.RotationType.LEFT:

                self.srcRect = pygame.Rect(
                    0, 
                    self.height * ((textures.images["Tiles"]["maxFramesX"] - 1) - float(self.type.value)),
                    self.width, self.height
                )

            case utils.RotationType.UP:

                # Since we flipped it, we have to count backwards to get our frames
                
                self.srcRect = pygame.Rect(
                    self.width * ((textures.images["Tiles"]["maxFramesX"] - 1) - float(self.type.value)),
                    0, 
                    self.width, self.height
                )

            case utils.RotationType.RIGHT:

                self.srcRect = pygame.Rect(
                    0, 
                    self.width * float(self.type.value),
                    self.width, self.height
                )