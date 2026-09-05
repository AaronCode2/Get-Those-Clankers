import pygame
import classes.utility.utils as utils
import classes.utility.textures as textures

class dropItem():

    def __init__(self, position: pygame.Vector2, type: utils.ItemType, amount: int):

        self.position = position
        self.type = utils.ItemType,
        self.amount = amount

        self.srcRect = pygame.Rect(

            textures.images["Items"]["image"]["FrameWidth"] * self.type.value
            0, 
            textures.images["Items"]["image"]["FrameWidth"],
            textures.images["Items"]["image"]["FrameHeight"]
        )

    def update(self, window):

        self.draw(window)

    def draw(self, window):

        window.blit(textures.images["Items"]["image"]["surface"], self.position, self.srcRect)