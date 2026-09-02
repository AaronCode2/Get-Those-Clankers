import pygame
import classes.utility.utils as utils
import classes.utility.textures as textures
from copy import copy

class Slot():

    def __init__(self):

        self.amount = 0
        self.type = utils.ItemType.NONE

    def reset(self):
        self.amount = 0
        self.type = utils.ItemType.NONE

    def set(self, amount: int, type: utils.ItemType):
        self.amount = amount
        self.type = type

class Inventory():

    def __init__(self):

        self.toggle = True
        self.mousepos = pygame.mouse.get_pos()

        # a 5x6 inventory! - 30slots

        self.slots = [

            # Main inventory
            [Slot() for i in range(5)],
            [Slot() for i in range(5)],
            [Slot() for i in range(5)],
            [Slot() for i in range(5)],
            [Slot() for i in range(5)],

            # HotBar
            [Slot() for i in range(5)],
        ]

        self.slots[2][2].amount = 12
        self.slots[2][2].type = utils.ItemType.SOFT_STEEL

        self.slots[3][1].amount = 15
        self.slots[3][1].type = utils.ItemType.SCREW

        self.isCrafterToggled = False
        self.selectedSlot = None
        self.slotSelectedSrcRect = None
        self.slotSelectedPos = None

        self.configureItemTextures()

    def update(self, window, craftToggle: bool):

        # So we don't activate that world tile feature when user on inventory!
        
        if(self.toggle):
            utils.activateTilePlacer = False
        else:
            utils.activateTilePlacer = True

        self.drawInventoryBackground(window)
        craftToggle = self.drawInventoryOptions(window)
        self.updateInventory(window)

        self.mousepos = pygame.mouse.get_pos()

    def drawInventoryBackground(self, window):

        inventoryPos = pygame.Vector2(

            utils.screenRect.width - utils.inventoryPosAdj.x,
            utils.screenRect.height - utils.inventoryPosAdj.y,
        )

        textures.drawGuiPlates(window, pygame.Vector2(6, 8), inventoryPos)
        self.drawBackgroundHotBar(window)


    def updateSelectedSlot(self, window):

        if(self.selectedSlot == None):
            return

        mousePos = pygame.mouse.get_pos()

        text = utils.smfont.render(str(self.selectedSlot.amount), True, utils.ColorPlattes["Pale White"])

        textPos = pygame.Vector2(

            mousePos[0] + utils.inventoryTextPos.x,
            mousePos[1] + utils.inventoryTextPos.y
        ) 
        
        window.blit(textures.images["Items"]["image"]["surface"], pygame.Vector2(mousePos[0], mousePos[1]), self.slotSelectedSrcRect)
        window.blit(text, textPos)

    def drawBackgroundHotBar(self, window):

        hotBarPos = pygame.Vector2(

            utils.screenRect.width - utils.HotBarPosAdj.x,
            utils.screenRect.height - utils.HotBarPosAdj.y,
        )

        textures.drawGuiPlates(window, pygame.Vector2(6, 2), hotBarPos)

    def getSelectedSlot(self, slot: Slot, itemSrcRect: pygame.Rect, slotPos: pygame.Vector2):

        self.selectedSlot = slot
        self.slotSelectedSrcRect = itemSrcRect
        self.slotSelectedPos = slotPos

    def getInventoryRects(self, x, y):

        adjuster = utils.inventorySlotPosAdj if(y != len(self.slots) - 1) else utils.HotBarSlotPosAdj

        buttonRect = pygame.Rect(

            utils.screenRect.width - adjuster.x + (textures.images["guiPlates"]["image"]["FrameWidth"] * x),
            utils.screenRect.height - adjuster.y + 
            (textures.images["guiPlates"]["image"]["FrameHeight"] * 
            y if(y != len(self.slots) - 1) else 0),
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

        if(not utils.mouseHover(buttonRect)):
            buttonSrcRect = textures.getGuiPlatesSrcRect(utils.GuiPlates.SMALL_BUTTON_UNPRESSED)
        else:
            buttonSrcRect = textures.getGuiPlatesSrcRect(utils.GuiPlates.SMALL_BUTTON_PRESSED)

        return buttonRect, itemSrcRect, itemPos, textPos, buttonSrcRect

    def updateInventory(self, window):

        mouseKey = pygame.mouse.get_just_released()

        for y in range(len(self.slots)):
            for x in range(len(self.slots[0])):

                if(not self.toggle and y != utils.hotBarindex):
                    continue

                buttonRect, itemSrcRect, itemPos, textPos, buttonSrcRect = self.getInventoryRects(x, y)
                self.handleUserInput(self.slots[y][x], itemSrcRect, x, y, buttonRect, mouseKey)

                window.blit(textures.images["guiPlates"]["image"]["surface"], pygame.Vector2(buttonRect.x, buttonRect.y), buttonSrcRect)

                if(self.slots[y][x].amount != 0):

                    text = utils.smfont.render(str(self.slots[y][x].amount), True, utils.ColorPlattes["Pale White"])
                    window.blit(textures.images["Items"]["image"]["surface"], pygame.Vector2(itemPos.x, itemPos.y), itemSrcRect)
                    window.blit(text, textPos)
                    
        self.handleUserDropFeature(mouseKey)

        self.updateSelectedSlot(window)

    def handleUserDropFeature(self, mouseKey):

        if(mouseKey[0] and self.selectedSlot != None):
            self.slots[int(self.slotSelectedPos.y)][int(self.slotSelectedPos.x)] = copy(self.selectedSlot)
            self.selectedSlot = None

    def handleUserInput(self, slot: Slot, itemSrcRect: pygame.Rect, x, y, buttonRect: pygame.Rect, mouseKey):

        if(utils.mouseClickedL(buttonRect) and self.selectedSlot == None and self.slots[y][x].type ):
            self.doItemMoving(self.slots[y][x], itemSrcRect, x, y)
        elif(utils.mouseClickedR(buttonRect) and self.slots[y][x].type != utils.ItemType.NONE):
            self.doSpilting(self.slots[y][x])

        if(mouseKey[0] and self.selectedSlot != None and utils.mouseHover(buttonRect)):

            if(self.slots[y][x].type == self.selectedSlot.type):

                self.slots[y][x].amount += self.selectedSlot.amount
                self.selectedSlot = None
            elif(self.slots[y][x].amount == 0):

                self.slots[y][x] = copy(self.selectedSlot)
                self.selectedSlot = None

    def doItemMoving(self, slot: Slot, itemSrcRect: pygame.Rect, x, y):

        # We call copy(), so we don't get the change slots set to reset
        self.getSelectedSlot(copy(self.slots[y][x]), itemSrcRect, pygame.Vector2(x, y))
        self.slots[y][x].reset()

    def doSpilting(self, currentSlot: Slot):

        amountOfslot = currentSlot.amount

        currentSlot.amount = int(currentSlot.amount / 2)

        for y in range(len(self.slots)):
            for x in range(len(self.slots[0])):

                if(self.slots[y][x].amount == 0):
                    self.slots[y][x].set(amountOfslot - currentSlot.amount, currentSlot.type)
                    return

    def drawInventoryOptions(self, window):
    
        inventoryOptionsPos, craftbuttonPos, craftTextPos = self.getAllInventoryOptionsRect()
    
        craftButtonState = utils.GuiPlates.LARGE_BUTTON_PRESSED
        color = utils.ColorPlattes["Glass Orange"]
            
        if(utils.mouseClickedL(
            pygame.Rect(
                craftbuttonPos.x, craftbuttonPos.y, 
                textures.images["guiPlates"]["image"]["FrameWidth"] * 2,
                textures.images["guiPlates"]["image"]["FrameHeight"]
        ))):
            self.isCrafterToggled = not self.isCrafterToggled
        elif(not self.isCrafterToggled):
            craftButtonState = utils.GuiPlates.LARGE_BUTTON_UNPRESSED
    
        if(utils.mouseHover(
            pygame.Rect(
                craftbuttonPos.x, craftbuttonPos.y, 
                textures.images["guiPlates"]["image"]["FrameWidth"] * 2,
                textures.images["guiPlates"]["image"]["FrameHeight"]
        ))):
            color = utils.ColorPlattes["Supreme Yellow"]
    
        craftText = utils.smfont.render("Craft", True, color)
    
        textures.drawGuiPlates(window, pygame.Vector2(6, 2), inventoryOptionsPos)
        textures.drawGuiSinglePlate(window, craftbuttonPos, craftButtonState)
        window.blit(craftText, craftTextPos)

    def getAllInventoryOptionsRect(self):

        inventoryOptionsPos = pygame.Vector2(

            utils.screenRect.width - utils.inventoryOptionPosAdj.x,
            utils.screenRect.height - utils.inventoryOptionPosAdj.y
        )

        craftbuttonPos = pygame.Vector2(

            inventoryOptionsPos.x + utils.craftButtonAdj.x,
            inventoryOptionsPos.y + utils.craftButtonAdj.y
        )

        craftTextPos = pygame.Vector2(

            craftbuttonPos.x + utils.craftTextAdj.x,
            craftbuttonPos.y + utils.craftTextAdj.y,
        )

        return inventoryOptionsPos, craftbuttonPos, craftTextPos

    def configureItemTextures(self):

        textures.images["Items"]["image"]["surface"] = pygame.image.load(textures.images["Items"]["location"]).convert_alpha()

        textures.images["Items"]["image"]["FrameWidth"] = textures.images["Items"]["image"]["surface"].width / textures.images["Items"]["FramesX"]
        textures.images["Items"]["image"]["FrameHeight"] = textures.images["Items"]["image"]["surface"].height