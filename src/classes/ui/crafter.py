import pygame
import classes.utility.utils as utils
import classes.utility.textures as textures
import classes.utility.crafterRecipes as crafterRecipes

class Crafter():

    def __init__(self):

        self.isCraftable = True

        print("Craft system activated")

    def update(self, window):

        self.drawBackgroundOverlay(window)

        # The crafter is split in two sections

        self.drawSectionInfo(window)
        self.drawSectionCraftItems(window)

    # Crafter symbol: :=: , it looks cool

    def getSectionCraftItemsRect(self):
        pass

    
    def drawSectionCraftItems(self, window):

        for i in range(len(crafterRecipes.RecipeCrafts)):
            print("a")

            # recipe

    def drawSectionInfo(self, window):

        craftButtonPos, craftTextPos, guiPlate, crafterText, crafterTextColor = self.getSectionInfoRects()

        craftText = utils.font.render(crafterText, True, crafterTextColor)

        textures.drawGuiSinglePlate(window, craftButtonPos, guiPlate)
        window.blit(craftText, craftTextPos)

    def getSectionInfoRects(self):

        utils.dev_updatePositionsAdjuster()

        craftButtonPos = pygame.Vector2(

            utils.screenRect.width - utils.craftButtonAdj.x,
            utils.screenRect.height - utils.craftButtonAdj.y,
        ) 

        craftTextPos = pygame.Vector2(
            utils.screenRect.width - utils.craftButtonTextAdj.x,
            utils.screenRect.height - utils.craftButtonTextAdj.y
        ) 

        if(self.isCraftable):

            crafterText = "CRAFT" 
            crafterTextColor = utils.ColorPlattes["Pale White"]
            
            if(utils.mouseHover(pygame.Rect(
                craftButtonPos.x, craftButtonPos.y, 
                utils.largeButtonSizeWidth, 
                utils.largeButtonSizeHeight
            ))):
                guiPlate = utils.GuiPlates.XL_ORANGE_BUTTON_PRESSED
            else:
                guiPlate = utils.GuiPlates.XL_ORANGE_BUTTON_UNPRESSED
        else:
            guiPlate = utils.GuiPlates.XL_BUTTON_UNPRESSED
            crafterText = ": = :"
            crafterTextColor = utils.ColorPlattes["Grey Cloud"]

        return craftButtonPos, craftTextPos, guiPlate, crafterText, crafterTextColor

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