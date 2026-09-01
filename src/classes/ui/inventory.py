import pygame
import classes.utility.utils as utils
import classes.utility.textures as textures

Slot = {

    utils.SlotIndex.AMOUNT: 0,
    utils.SlotIndex.TYPE: 0
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

        print(self.slots)

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

                if(not buttonRect.collidepoint(self.mousepos)):
                    buttonSrcRect = self.getSrcRectForButton(utils.GuiPlates.SMALL_BUTTON_UNPRESSED)
                else:
                    buttonSrcRect = self.getSrcRectForButton(utils.GuiPlates.SMALL_BUTTON_PRESSED)

                window.blit(textures.images["guiPlates"]["image"]["surface"], pygame.Vector2(buttonRect.x, buttonRect.y), buttonSrcRect)

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
            

    def draw(self, window):

        self.drawHotBar(window)