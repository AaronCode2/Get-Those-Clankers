import pygame
import classes.utility.utils as utils
import classes.utility.textures as textures

class Slot():

    def __init__(self):

        self.amount = 0
        self.type = utils.ItemType.NONE

    def reset(self):
        self.amount = 0
        self.type = utils.ItemType.NONE

class Inventory():

    def __init__(self):

        self.toggle = True
        self.mousepos = pygame.mouse.get_pos()

        # a 5x5 inventory! - 25slots

        self.slots = [

            # Main inventory
            [Slot() for i in range(5)],
            [Slot() for i in range(5)],
            [Slot() for i in range(5)],
            [Slot() for i in range(5)],

            # HotBar
            [Slot() for i in range(5)],
        ]

        self.slots[2][2].amount = 12
        self.slots[2][2].type = utils.ItemType.SOFT_STEEL

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

                    textures.images["Items"]["image"]["FrameWidth"] * self.slots[y][x].type.value,
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

                text = utils.smfont.render(str(self.slots[y][x].amount), True, utils.ColorPlattes["Pale White"])

                if(not utils.mouseHover(buttonRect)):
                    buttonSrcRect = self.getSrcRectForButton(utils.GuiPlates.SMALL_BUTTON_UNPRESSED)
                else:
                    buttonSrcRect = self.getSrcRectForButton(utils.GuiPlates.SMALL_BUTTON_PRESSED)
                
                if(utils.mouseClickedL(buttonRect)):
                    self.selectedSlotMover(self.slots[y][x], itemPos)
                    self.slots[y][x].reset()

                window.blit(textures.images["guiPlates"]["image"]["surface"], pygame.Vector2(buttonRect.x, buttonRect.y), buttonSrcRect)

                if(self.slots[y][x].amount != 0):
                    window.blit(textures.images["Items"]["image"]["surface"], pygame.Vector2(itemPos.x, itemPos.y), itemSrcRect)
                    window.blit(text, textPos)

    def selectedSlotMover(self, slot: Slot, itemPos):
            pass

    def drawHotBar(self, window):

        for i in range(5):

            buttonRect = pygame.Rect(

                utils.screenRect.width - 358 + (textures.images["guiPlates"]["image"]["FrameWidth"] * i),
                utils.screenRect.height - 90,
                textures.images["guiPlates"]["image"]["FrameWidth"],
                textures.images["guiPlates"]["image"]["FrameHeight"]
            )

            if(not utils.mouseHover(buttonRect)):
                buttonSrcRect = self.getSrcRectForButton(utils.GuiPlates.SMALL_BUTTON_UNPRESSED)
            else:
                buttonSrcRect = self.getSrcRectForButton(utils.GuiPlates.SMALL_BUTTON_PRESSED)

            itemSrcRect = pygame.Rect(

                textures.images["Items"]["image"]["FrameWidth"] * self.slots[utils.hotBarindex][i].type.value,
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

            text = utils.smfont.render(str(self.slots[utils.hotBarindex][i].amount), True, utils.ColorPlattes["Pale White"])

            window.blit(textures.images["guiPlates"]["image"]["surface"], pygame.Vector2(buttonRect.x, buttonRect.y), buttonSrcRect)
            if(self.slots[utils.hotBarindex][i].amount != 0):
                window.blit(textures.images["Items"]["image"]["surface"], pygame.Vector2(itemPos.x, itemPos.y), itemSrcRect)
                window.blit(text, textPos)

    def configureItemTextures(self):

        textures.images["Items"]["image"]["surface"] = pygame.image.load(textures.images["Items"]["location"]).convert_alpha()

        textures.images["Items"]["image"]["FrameWidth"] = textures.images["Items"]["image"]["surface"].width / textures.images["Items"]["FramesX"]
        textures.images["Items"]["image"]["FrameHeight"] = textures.images["Items"]["image"]["surface"].height
      
    def draw(self, window):

        self.drawHotBar(window)