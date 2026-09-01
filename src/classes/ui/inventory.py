import pygame
import classes.utility.utils as utils
import classes.utility.textures as textures

Slot = {

    utils.SlotIndex.AMOUNT: 22,
    utils.SlotIndex.TYPE: utils.ItemType.SCRAP_IGNOT
}

class Inventory():

    def __init__(self):

        self.toggle = True
        self.mousepos = pygame.mouse.get_pos()

        # a 5x5 inventory! - 25slots

        self.slots = [

            # Main inventory
            [Slot] * 5,
            [Slot] * 5,
            [Slot] * 5,
            [Slot] * 5,

            # HotBar
            [Slot] * 5,
        ]

        self.configureItemTextures()

    def update(self, window):

        if(self.toggle):
            utils.activateTilePlacer = False
            self.drawInventory(window)
        else:
            utils.activateTilePlacer = True

        self.mousepos = pygame.mouse.get_pos()

        self.draw(window)

    def getSrcRectForButton(self, guiPlate: utils.GuiPlates):

        return pygame.Rect(
                textures.images["guiPlates"]["image"]["FrameWidth"] * float(utils.guiPlatesFrameMap[guiPlate][0]), 
                textures.images["guiPlates"]["image"]["FrameWidth"] * float(utils.guiPlatesFrameMap[guiPlate][1]),
                textures.images["guiPlates"]["image"]["FrameWidth"],
                textures.images["guiPlates"]["image"]["FrameHeight"]
            )

    def drawInventory(self, window):

        for y in range(len(self.slots)):
            for x in range(len(self.slots[0])):

                buttonRect = pygame.Rect(

                    utils.screenRect.width - utils.inventorySlotPosAdj.x + (textures.images["guiPlates"]["image"]["FrameWidth"] * x),
                    utils.screenRect.height - utils.inventorySlotPosAdj.y + (textures.images["guiPlates"]["image"]["FrameHeight"] * y),
                    textures.images["guiPlates"]["image"]["FrameWidth"],
                    textures.images["guiPlates"]["image"]["FrameHeight"]
                )

                itemSrcRect = pygame.Rect(

                    textures.images["Items"]["image"]["FrameWidth"] * self.slots[y][x][utils.SlotIndex.TYPE].value,
                    0,
                    textures.images["Items"]["image"]["FrameWidth"],
                    textures.images["Items"]["image"]["FrameHeight"],
                )

                itemPos = pygame.Vector2(

                    buttonRect.x + utils.itemPosAdj.x,
                    buttonRect.y + utils.itemPosAdj.y,
                )

                textPos = pygame.Vector2(

                    itemPos.x + utils.inventoryTextPos.x,
                    itemPos.y + utils.inventoryTextPos.y
                ) 

                text = utils.smfont.render(str(self.slots[y][x][utils.SlotIndex.AMOUNT]), True, utils.ColorPlattes["Pale White"])

                if(not buttonRect.collidepoint(self.mousepos)):
                    buttonSrcRect = self.getSrcRectForButton(utils.GuiPlates.SMALL_BUTTON_UNPRESSED)
                else:
                    buttonSrcRect = self.getSrcRectForButton(utils.GuiPlates.SMALL_BUTTON_PRESSED)

                window.blit(textures.images["guiPlates"]["image"]["surface"], pygame.Vector2(buttonRect.x, buttonRect.y), buttonSrcRect)
                window.blit(textures.images["Items"]["image"]["surface"], pygame.Vector2(itemPos.x, itemPos.y), itemSrcRect)
                window.blit(text, textPos)



    def drawHotBar(self, window):

        for i in range(5):

            buttonRect = pygame.Rect(

                utils.screenRect.width - 358 + (textures.images["guiPlates"]["image"]["FrameWidth"] * i),
                utils.screenRect.height - 90,
                textures.images["guiPlates"]["image"]["FrameWidth"],
                textures.images["guiPlates"]["image"]["FrameHeight"]
            )

            if(not buttonRect.collidepoint(self.mousepos)):
                buttonSrcRect = self.getSrcRectForButton(utils.GuiPlates.SMALL_BUTTON_UNPRESSED)
            else:
                buttonSrcRect = self.getSrcRectForButton(utils.GuiPlates.SMALL_BUTTON_PRESSED)

            window.blit(textures.images["guiPlates"]["image"]["surface"], pygame.Vector2(buttonRect.x, buttonRect.y), buttonSrcRect)

    def configureItemTextures(self):

        textures.images["Items"]["image"]["surface"] = pygame.image.load(textures.images["Items"]["location"]).convert_alpha()

        textures.images["Items"]["image"]["FrameWidth"] = textures.images["Items"]["image"]["surface"].width / textures.images["Items"]["FramesX"]
        textures.images["Items"]["image"]["FrameHeight"] = textures.images["Items"]["image"]["surface"].height
      
    def draw(self, window):

        self.drawHotBar(window)