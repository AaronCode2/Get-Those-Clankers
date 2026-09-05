import pygame
import classes.utility.utils as utils
import classes.utility.textures as textures

droppedItems = []

class DropItem():

    def __init__(self, position: pygame.Vector2, type = utils.ItemType.NONE, amount = -1):

        self.position = position

        if(amount == -1):
            self._type, self._amount = utils.generateItemForDropItem()
        else:
            self._type = type
            self._amount = amount

        self.srcRect = pygame.Rect(

            textures.images["Items"]["image"]["FrameWidth"] * self._type.value,
            0, 
            textures.images["Items"]["image"]["FrameWidth"],
            textures.images["Items"]["image"]["FrameHeight"]
        )

    def getItem(self):
        return self._type, self._amount

    def update(self, window):

        self.draw(window)

    def draw(self, window):

        window.blit(textures.images["Items"]["image"]["surface"], self.position, self.srcRect)