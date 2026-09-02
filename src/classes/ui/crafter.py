import pygame
import classes.utility.utils as utils
import classes.utility.textures as textures

class Crafter():

    def __init__(self):

        print("Craft system activated")

    def update(self, window):

        self.drawBackgroundOverlay(window)

        # The crafter is split in two sections

        self.drawSectionInfo(window)

    # Crafter symbol: :=: , it looks cool



    def drawSectionInfo(self, window):

        craftButtonPos, craftTextPos, guiPlate = self.getSectionInfoRects()

        textures.drawGuiSinglePlate(window, craftButtonPos, guiPlate)

    def getSectionInfoRects(self):

        utils.dev_updatePositionsAdjuster()

        craftButtonPos = pygame.Vector2(

            utils.screenRect.width - utils.craftButtonAdj.x,
            utils.screenRect.height - utils.craftButtonAdj.y,
        ) 

        craftTextPos = pygame.Vector2(
            utils.screenRect.width - utils.dev_PositionAdjuster.x,
            utils.screenRect.height - utils.dev_PositionAdjuster.y
        ) 

        if(utils.mouseHover(pygame.Rect(
            craftButtonPos.x, craftButtonPos.y, 
            utils.largeButtonSizeWidth, 
            utils.largeButtonSizeHeight
        ))):
            guiPlate = utils.GuiPlates.XL_ORANGE_BUTTON_PRESSED
        else:
            guiPlate = utils.GuiPlates.XL_ORANGE_BUTTON_UNPRESSED

        return craftButtonPos, craftTextPos, guiPlate

    def drawBackgroundOverlay(self, window):

        crafterPosNorPlate, crafterPosMarPlate1, crafterPosMarPlate2 = self.getBackgroundOverlayRect()

        textures.drawGuiPlates(window, pygame.Vector2(10, 13), crafterPosNorPlate)
        textures.drawGuiPlates(window, pygame.Vector2(6, 12), crafterPosMarPlate1, utils.TypeOfGuiPlates.MARGIN)
        textures.drawGuiPlates(window, pygame.Vector2(3, 12), crafterPosMarPlate2, utils.TypeOfGuiPlates.MARGIN)

    def getBackgroundOverlayRect(self):

        crafterPosNorPlate = pygame.Vector2(

            utils.screenRect.width - utils.crafterPosAdj.x,
            utils.screenRect.height - utils.crafterPosAdj.y,
        )

        crafterPosMarPlate1 = pygame.Vector2(

            crafterPosNorPlate.x + utils.crafterPosMarPlatePosAdj1.x,
            crafterPosNorPlate.y + utils.crafterPosMarPlatePosAdj1.y,
        )

        crafterPosMarPlate2 = pygame.Vector2(

            crafterPosNorPlate.x + utils.crafterPosMarPlatePosAdj2.x,
            crafterPosNorPlate.y + utils.crafterPosMarPlatePosAdj2.y,
        )

        return crafterPosNorPlate, crafterPosMarPlate1, crafterPosMarPlate2