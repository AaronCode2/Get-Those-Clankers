import pygame
import classes.utility.utils as utils

# temp
import classes.utility.textures as textures

class Tile:

    def __init__(self, position: pygame.Vector2, type: utils.TileType, rotation: utils.RotationType):

        self.position = position
        self.type = type
        self.width = textures.images["Tiles"]["image"]["FrameWidth"]
        self.height = textures.images["Tiles"]["image"]["FrameHeight"]

        self.hitBox = None

        self.rotation = rotation

        print(type)

        # Get a frame of the whole image

        self.setSrcRect()

    def update(self, window):

        self.draw(window)

    def draw(self, window):

        if(self.rotation == utils.RotationType.DOWN):
            window.blit(textures.images["Tiles"]["image"]["surface"], self.position, self.srcRect)
        else:
            window.blit(textures.images["Tiles"]["rotatedImages"][self.rotation], self.position, self.srcRect)

    def setSrcRect(self):

        # Takes care of rotated image and gets that single frame it needs
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