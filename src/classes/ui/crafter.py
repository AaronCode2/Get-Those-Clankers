import pygame
import classes.utility.utils as utils
import classes.utility.textures as textures
import classes.utility.crafterRecipes as crafterRecipes

class Crafter():

    def __init__(self):

        self.isCraftable = True
        self.selectedRecipe = None

        print("Craft system activated")

    def update(self, window, inventory):

        self.drawBackgroundOverlay(window)

        # The crafter is split in two sections

        self.drawSectionInfo(window, inventory)
        self.drawSectionCraftItems(window, inventory)

    # Crafter symbol: :=: , it looks cool

    def getSectionCraftItemsRect(self):
        pass

    
    def drawSectionCraftItems(self, window, inventory):

        utils.dev_updatePositionsAdjuster()
        y = 0

        for i in range(len(crafterRecipes.RecipeCrafts)):

            index = i

            if(i % 5 == 0): 
                y += 1
                i = 0 

            crafterRecipeButtonPos = pygame.Vector2(

                utils.screenRect.width - utils.crafterRecipeButtonPosAdj.x + (utils.smallButtonSize * i),
                utils.screenRect.height - utils.crafterRecipeButtonPosAdj.y + (utils.smallButtonSize * y),
            )

            itemType = crafterRecipes.recipes[crafterRecipes.RecipeCrafts(index)][crafterRecipes.RecipeIndex.ItemTypeGiven]

            itemSrcRect = pygame.Rect(

                textures.images["Items"]["image"]["FrameWidth"] * itemType.value,
                0,
                textures.images["Items"]["image"]["FrameWidth"],
                textures.images["Items"]["image"]["FrameHeight"],
            )

            itemPos = pygame.Vector2(

                crafterRecipeButtonPos.x + utils.itemPosAdj.x,
                crafterRecipeButtonPos.y + utils.itemPosAdj.y,
            )

            if(utils.mouseClickedL(pygame.Rect(
                crafterRecipeButtonPos.x, crafterRecipeButtonPos.y, 
                utils.smallButtonSize, utils.smallButtonSize 
            ))):
                if(self.selectedRecipe != crafterRecipes.recipes[crafterRecipes.RecipeCrafts(index)]):

                    self.isCraftable = True
                    
                    for i in range(len(
                        crafterRecipes.recipes[crafterRecipes.RecipeCrafts(index)][crafterRecipes.RecipeIndex.ItemNeeded]
                    )):

                        if(not inventory.inventoryHasItem(
                            crafterRecipes.recipes[crafterRecipes.RecipeCrafts(index)][crafterRecipes.RecipeIndex.ItemNeeded][i][0],
                            crafterRecipes.recipes[crafterRecipes.RecipeCrafts(index)][crafterRecipes.RecipeIndex.ItemNeeded][i][1]
                        )):
                            self.isCraftable = False
                            break

                    self.selectedRecipe =  crafterRecipes.recipes[crafterRecipes.RecipeCrafts(index)]
                else:
                    self.selectedRecipe = None

            if(self.selectedRecipe == crafterRecipes.recipes[crafterRecipes.RecipeCrafts(index)]):
                guiPlateButton = utils.GuiPlates.SMALL_BUTTON_PRESSED
            else:
                guiPlateButton = utils.GuiPlates.SMALL_BUTTON_UNPRESSED


            textures.drawGuiSinglePlate(window, crafterRecipeButtonPos, guiPlateButton)
            window.blit(textures.images["Items"]["image"]["surface"], itemPos, itemSrcRect)
            
    def drawSectionInfo(self, window, inventory):

        craftButtonPos, craftTextPos, guiPlate, crafterText, crafterTextColor, descriptionPos = self.getSectionInfoRects(inventory)

        craftText = utils.font.render(crafterText, True, crafterTextColor)

        textures.drawGuiSinglePlate(window, craftButtonPos, guiPlate)
        window.blit(craftText, craftTextPos)

        if(self.selectedRecipe != None):

            descriptionText = utils.ssmfont.render(
                self.selectedRecipe[crafterRecipes.RecipeIndex.ItemDescription], 
                True, utils.ColorPlattes["Pale White"]
            )

            for i in range(len(self.selectedRecipe[crafterRecipes.RecipeIndex.ItemNeeded])):

                itemRequiredSrcRect = pygame.Rect(

                    textures.images["Items"]["image"]["FrameWidth"] 
                    * self.selectedRecipe[crafterRecipes.RecipeIndex.ItemNeeded][utils.ItemType(i).value][0].value,
                    0,
                    textures.images["Items"]["image"]["FrameWidth"],
                    textures.images["Items"]["image"]["FrameHeight"],
                )

                itemGivenSrcRect = pygame.Rect(

                    textures.images["Items"]["image"]["FrameWidth"] 
                    * self.selectedRecipe[crafterRecipes.RecipeIndex.ItemTypeGiven].value,
                    0,
                    textures.images["Items"]["image"]["FrameWidth"],
                    textures.images["Items"]["image"]["FrameHeight"],
                )

                itemGivenPos = pygame.Vector2(

                    utils.screenRect.width - utils.itemGivenPosAdj.x,
                    utils.screenRect.height - utils.itemGivenPosAdj.y
                )

                itemGivenTextPos = pygame.Vector2(

                    itemGivenPos.x + utils.itemGivenTextPosAdj,
                    itemGivenPos.y
                )

                itemGivenText = utils.smfont.render(
                    "+" + str(self.selectedRecipe[crafterRecipes.RecipeIndex.ItemGiven]),
                    True,
                    utils.ColorPlattes["Pale White"]
                )

                itemRequiredPos = pygame.Vector2(

                    utils.screenRect.width - utils.itemRequiredPosAdj.x,
                    utils.screenRect.height - utils.itemRequiredPosAdj.y + (textures.images["Items"]["image"]["FrameHeight"] * i)
                )

                itemRequiredTextPos = pygame.Vector2(

                    itemRequiredPos.x + utils.itemRequiredTextPosAdj,
                    itemRequiredPos.y
                )

                itemRequiredTextPos = pygame.Vector2(

                    itemRequiredPos.x + utils.itemRequiredTextPosAdj,
                    itemRequiredPos.y
                )

                itemRequiredText = utils.smfont.render(
                    "x" + str(self.selectedRecipe[crafterRecipes.RecipeIndex.ItemNeeded][utils.ItemType(i).value][1]),
                    True,
                    utils.ColorPlattes["Pale White"]
                )

                window.blit(textures.images["Items"]["image"]["surface"], itemGivenPos, itemGivenSrcRect)
                window.blit(itemGivenText, itemGivenTextPos)

                window.blit(itemRequiredText, itemRequiredTextPos)
                window.blit(textures.images["Items"]["image"]["surface"], itemRequiredPos, itemRequiredSrcRect)

            window.blit(descriptionText, descriptionPos)
        
    def getSectionInfoRects(self, inventory):

        utils.dev_updatePositionsAdjuster()

        craftButtonPos = pygame.Vector2(

            utils.screenRect.width - utils.craftButtonAdj.x,
            utils.screenRect.height - utils.craftButtonAdj.y,
        ) 

        craftTextPos = pygame.Vector2(
            utils.screenRect.width - utils.craftButtonTextAdj.x,
            utils.screenRect.height - utils.craftButtonTextAdj.y
        ) 

        utils.dev_updatePositionsAdjuster()

        descriptionPos = pygame.Vector2(

            utils.screenRect.width - utils.descriptionPosAdj.x,
            utils.screenRect.height - utils.descriptionPosAdj.y
        )

        if(self.isCraftable and self.selectedRecipe != None):

            crafterText = "CRAFT" 
            crafterTextColor = utils.ColorPlattes["Pale White"]
            for i in range(len(self.selectedRecipe[crafterRecipes.RecipeIndex.ItemNeeded])):

                if(self.selectedRecipe != None and not inventory.inventoryHasItem(
                    self.selectedRecipe[crafterRecipes.RecipeIndex.ItemNeeded][i][0],
                    self.selectedRecipe[crafterRecipes.RecipeIndex.ItemNeeded][i][1]
                )):
                    self.selectedRecipe = None
                    self.isCraftable = False
            
            if(self.isCraftable and utils.mouseClickedL(pygame.Rect(
                craftButtonPos.x, craftButtonPos.y, 
                utils.XLButtonSizeWidth, 
                utils.XLButtonSizeHeight
            ))):

                for i in range(len(self.selectedRecipe[crafterRecipes.RecipeIndex.ItemNeeded])):

                    self.selectedRecipe[crafterRecipes.RecipeIndex.ItemNeeded][i][0],
                    self.selectedRecipe[crafterRecipes.RecipeIndex.ItemNeeded][i][1]
                    
                    inventory.removeInventoryItem(
                        self.selectedRecipe[crafterRecipes.RecipeIndex.ItemNeeded][i][0],
                        self.selectedRecipe[crafterRecipes.RecipeIndex.ItemNeeded][i][1],
                    )

                if(self.selectedRecipe != None):
                    inventory.addInventoryItem(
                        self.selectedRecipe[crafterRecipes.RecipeIndex.ItemTypeGiven],
                        self.selectedRecipe[crafterRecipes.RecipeIndex.ItemGiven]
                    )
                
                guiPlate = utils.GuiPlates.XL_ORANGE_BUTTON_PRESSED
            else:
                guiPlate = utils.GuiPlates.XL_ORANGE_BUTTON_UNPRESSED
        else:
            guiPlate = utils.GuiPlates.XL_BUTTON_UNPRESSED
            crafterText = ": = :"
            crafterTextColor = utils.ColorPlattes["Grey Cloud"]

        return craftButtonPos, craftTextPos, guiPlate, crafterText, crafterTextColor, descriptionPos

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