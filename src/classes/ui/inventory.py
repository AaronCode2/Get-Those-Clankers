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

        self.selectedSlot = None
        self.slotSelectedSrcRect = None
        self.slotSelectedPos = None

        self.configureItemTextures()

    def update(self, window):

        if(self.toggle):
            utils.activateTilePlacer = False
        else:
            utils.activateTilePlacer = True

        self.updateInventory(window)

        self.mousepos = pygame.mouse.get_pos()

        self.draw(window)

    def getSrcRectForButton(self, guiPlate: utils.GuiPlates):

        return pygame.Rect(
                textures.images["guiPlates"]["image"]["FrameWidth"] * float(utils.guiPlatesFrameMap[guiPlate][0]), 
                textures.images["guiPlates"]["image"]["FrameWidth"] * float(utils.guiPlatesFrameMap[guiPlate][1]),
                textures.images["guiPlates"]["image"]["FrameWidth"],
                textures.images["guiPlates"]["image"]["FrameHeight"]
            )

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

        return buttonRect, itemSrcRect, itemPos, textPos

    def updateInventory(self, window):

        mouseKey = pygame.mouse.get_just_released()

        for y in range(len(self.slots)):
            for x in range(len(self.slots[0])):

                if(not self.toggle and y != utils.hotBarindex):
                    continue

                buttonRect, itemSrcRect, itemPos, textPos = self.getInventoryRects(x, y)

                if(not utils.mouseHover(buttonRect)):
                    buttonSrcRect = self.getSrcRectForButton(utils.GuiPlates.SMALL_BUTTON_UNPRESSED)
                else:
                    buttonSrcRect = self.getSrcRectForButton(utils.GuiPlates.SMALL_BUTTON_PRESSED)

                if(utils.mouseClickedL(buttonRect) and self.selectedSlot == None):
                    
                    # We call copy(), so we don't get the change slots set to reset
                    self.doInventoryItemMoving(self.slots[y][x], itemSrcRect, x, y)
                elif(utils.mouseClickedR(buttonRect)):
                    self.doInventorySpilting(self.slots[y][x])

                if(mouseKey[0] and self.selectedSlot != None and utils.mouseHover(buttonRect)):

                    if(self.slots[y][x].type == self.selectedSlot.type):

                        self.slots[y][x].amount += self.selectedSlot.amount
                        self.selectedSlot = None
                    elif(self.slots[y][x].amount == 0):

                        self.slots[y][x] = copy(self.selectedSlot)
                        self.selectedSlot = None

                text = utils.smfont.render(str(self.slots[y][x].amount), True, utils.ColorPlattes["Pale White"])
                window.blit(textures.images["guiPlates"]["image"]["surface"], pygame.Vector2(buttonRect.x, buttonRect.y), buttonSrcRect)

                if(self.slots[y][x].amount != 0):
                    window.blit(textures.images["Items"]["image"]["surface"], pygame.Vector2(itemPos.x, itemPos.y), itemSrcRect)
                    window.blit(text, textPos)
                    
        if(mouseKey[0] and self.selectedSlot != None):
            self.slots[int(self.slotSelectedPos.y)][int(self.slotSelectedPos.x)] = copy(self.selectedSlot)
            self.selectedSlot = None

        self.updateSelectedSlot(window)

    def doInventoryItemMoving(self, slot : Slot, itemSrcRect: pygame.Rect, x, y):
            
        self.getSelectedSlot(copy(self.slots[y][x]), itemSrcRect, pygame.Vector2(x, y))
        self.slots[y][x].reset()

    def doInventorySpilting(self, currentSlot: Slot):

        amountOfslot = currentSlot.amount

        currentSlot.amount = int(currentSlot.amount / 2)

        for y in range(len(self.slots)):
            for x in range(len(self.slots[0])):

                if(self.slots[y][x].amount == 0):
                    self.slots[y][x].set(amountOfslot - currentSlot.amount, currentSlot.type)
                    return


    def configureItemTextures(self):

        textures.images["Items"]["image"]["surface"] = pygame.image.load(textures.images["Items"]["location"]).convert_alpha()

        textures.images["Items"]["image"]["FrameWidth"] = textures.images["Items"]["image"]["surface"].width / textures.images["Items"]["FramesX"]
        textures.images["Items"]["image"]["FrameHeight"] = textures.images["Items"]["image"]["surface"].height
      
    def draw(self, window):
        pass