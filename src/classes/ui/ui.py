import pygame
import classes.utility.utils as utils
import classes.utility.textures as textures
import classes.ui.inventory as inventory
import classes.utility.animation as animation
import classes.ui.crafter as crafter
from time import time

class UI():

    def __init__(self):

        self.configureImages()

        self.timeStamp = time()

        self.inventory = inventory.Inventory()
        self.crafter = crafter.Crafter()

    def update(self, window):

        keypress = pygame.key.get_just_pressed()

        if(keypress[pygame.K_e]):
            self.inventory.toggle = not self.inventory.toggle

        self.draw(window)

    def addStuffToInventory(self, itemType: utils.ItemType, amount: int):

        if(itemType != None):
            self.inventory.addInventoryItem(itemType, amount)

    def draw(self, window):

        self.displayKeyGuides(window)

        if(self.inventory.isCrafterToggled and self.inventory.toggle):
           self.crafter.update(window, self.inventory)

        self.inventory.update(window)

    def displayKeyGuides(self, window):

        for i in range(textures.images["keys"]["maxFramesX"]):

            textguide = utils.font.render(utils.keyGuidesTexts[utils.KeyGuides(i)], True, (0, 0, 0))
            
            position = pygame.Vector2(
                (textures.images["keys"]["image"]["FrameWidth"] * i) + 
                utils.keyGuidesTexts["textOffsets"][utils.KeyGuides(i)] + 5.0,
                (utils.screenRect.height - textures.images["keys"]["image"]["FrameHeight"]), 
            )

            positionText = pygame.Vector2(
                textures.images["keys"]["image"]["FrameWidth"] * i + 
                utils.keyGuidesTexts["textOffsets"][utils.KeyGuides(i)] + 68.0,
                (utils.screenRect.height - textures.images["keys"]["image"]["FrameHeight"] + 5), 
            )

            srcRect = pygame.Rect(
                textures.images["keys"]["image"]["FrameWidth"] * i,
                0,
                textures.images["keys"]["image"]["FrameWidth"],
                textures.images["keys"]["image"]["FrameHeight"] 
            )

            window.blit(textguide, positionText)
            window.blit(textures.images["keys"]["image"]["surface"], position, srcRect)

    def getInventoryHotBarSelectedSlot(self):
        return self.inventory.getSelectedHotBarSlot()
    
    def configureImages(self):

        textures.images["keys"]["image"]["surface"] =  pygame.image.load(textures.images["keys"]["location"]).convert_alpha()
        textures.images["keys"]["image"]["surface"] = pygame.transform.scale2x(textures.images["keys"]["image"]["surface"])

        textures.images["keys"]["image"]["FrameWidth"] = textures.images["keys"]["image"]["surface"].width / textures.images["keys"]["maxFramesX"] 
        textures.images["keys"]["image"]["FrameHeight"] = textures.images["keys"]["image"]["surface"].height

        textures.images["guiPlates"]["image"]["surface"] =  pygame.image.load(textures.images["guiPlates"]["location"]).convert_alpha()
        textures.images["guiPlates"]["image"]["surface"] = pygame.transform.scale2x(textures.images["guiPlates"]["image"]["surface"])

        textures.images["guiPlates"]["image"]["FrameWidth"] = textures.images["guiPlates"]["image"]["surface"].width / textures.images["guiPlates"]["FramesX"] 
        textures.images["guiPlates"]["image"]["FrameHeight"] = textures.images["guiPlates"]["image"]["surface"].height / textures.images["guiPlates"]["FramesY"] 
