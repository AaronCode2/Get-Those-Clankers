import pygame
import tiles
import utils
import batteryGen
import math

# Using this temporarly! -> import textures

import textures

class World():

    def __init__(self):

        self.worldPos = pygame.Vector2(0, 0)
        self.tiles = []

        self.initTextures()

        self.batteryGenator = batteryGen.BatteryGenenator()

        self.defaultRotation = utils.RotationType.DOWN
        self.previewTile = {

            "image": textures.images["Tiles"]["image"]["surface"].copy(),
            "srcRect": None
        }
        self.selectedTileType = utils.TileType.SOLAR_PANEL

        self.previewTile["image"].set_alpha(100)
        self.previewTile["srcRect"] = utils.configureRotatedImageForPreview(
                textures.images["Tiles"]["image"]["FrameWidth"],
                textures.images["Tiles"]["image"]["FrameHeight"],
                self.selectedTileType,
                self.defaultRotation
        )
        self.destPreviewRect = pygame.Vector2(0, 0)

        self.tiles.append(

            tiles.Tile(
                pygame.Vector2(
                300, 200
                ), utils.TileType.BARRIER,
                utils.RotationType.DOWN
            )
        )

    def drawPreviewPlacer(self, mousePos, window):
        
        window.blit(
            self.previewTile["image"], 
            pygame.Vector2(self.destPreviewRect.x, self.destPreviewRect.y), 
            self.previewTile["srcRect"]
        )

    def handleInputplacer(self, window):

        mousePos = pygame.mouse.get_pos()
        mouseEvent = pygame.mouse.get_just_pressed()
        keypress = pygame.key.get_just_pressed()
        keypressing = pygame.key.get_pressed()      

        snapMode = False

        # The Left CTRL is support for left-handed keyboards

        if(keypressing[pygame.K_RCTRL] or keypressing[pygame.K_LCTRL]):
            snapMode = True

        # Make them rotate when input and do stuff to get it working right :)

        if(self.getScrollwheelInput().y != 0 or keypress[pygame.K_r]):

            if self.defaultRotation != utils.RotationType.RIGHT:
                self.defaultRotation = utils.RotationType((self.defaultRotation.value + 1))
            else:
                self.defaultRotation = utils.RotationType.DOWN

            self.previewTile["image"] = pygame.transform.rotate(
                textures.images["Tiles"]["image"]["surface"], 
                utils.rotations[self.defaultRotation]
            ).convert_alpha()

            self.previewTile["srcRect"] = utils.configureRotatedImageForPreview(
                textures.images["Tiles"]["image"]["FrameWidth"],
                textures.images["Tiles"]["image"]["FrameHeight"],
                self.selectedTileType,
                self.defaultRotation
            )

            utils.scrollWheel = pygame.Vector2(0, 0)

        return mouseEvent, mousePos, snapMode

    def snapModeActivate(self, window, mouseRect):
        
        detectAreaRange = pygame.Rect(
                (mouseRect.x + utils.adjmousePos.x) - utils.defaultImageSizes / 2, 
                (mouseRect.y + utils.adjmousePos.y) - utils.defaultImageSizes / 2, 
                utils.defaultImageSizes * 2, utils.defaultImageSizes * 2
            )

        utils.debugDraw(window, detectAreaRange)

        selectedTile = -1

        closestDistance = 0xffff

        for tile in self.tiles:

            if(
                detectAreaRange.colliderect(
                pygame.Rect(
                tile.position.x, tile.position.y,
                utils.defaultImageSizes, 
                utils.defaultImageSizes
            ))):

                # Pathegorem - find the closest tile to mouse
                
                distance = math.sqrt((tile.position.x - mouseRect.x)**2 + (tile.position.y - mouseRect.y)**2)

                if(distance < closestDistance):
                    closestDistance = distance
                    selectedTile = tile


        if(selectedTile != -1):

            utils.debugDraw(window, pygame.Rect(selectedTile.position.x, selectedTile.position.y, utils.defaultImageSizes, utils.defaultImageSizes))
            # Calcualate snap points , btw this is just for snapping, nothing else. 200 lines for snapping

            #  May need to change defaultImageSize to tile.size

            if(
                (selectedTile.rotation == utils.RotationType.DOWN or selectedTile.rotation == utils.RotationType.UP) and
                selectedTile.position.x + utils.defaultImageSizes <= mouseRect.x and
                selectedTile.position.y <= mouseRect.y and
                selectedTile.position.y + utils.defaultImageSizes >= mouseRect.y
            ):

                #  Right side [=]<!>
                return utils.getSnapConfig(utils.SnapType.RIGHT_SIDE, selectedTile, selectedTile.rotation)
            elif(
                (selectedTile.rotation == utils.RotationType.DOWN or selectedTile.rotation == utils.RotationType.UP) and
                selectedTile.position.x >= mouseRect.x and 
                selectedTile.position.y <= mouseRect.y and
                selectedTile.position.y + utils.defaultImageSizes >= mouseRect.y
            ):

                #  Left side <!>[=]
                return utils.getSnapConfig(utils.SnapType.LEFT_SIDE, selectedTile, selectedTile.rotation)
            elif(
                (selectedTile.rotation == utils.RotationType.DOWN or selectedTile.rotation == utils.RotationType.UP) and
                selectedTile.position.y + utils.defaultImageSizes + utils.snapdetect2Adj.y <= mouseRect.y and
                selectedTile.position.x <= mouseRect.x and  
                selectedTile.position.x + utils.defaultImageSizes >= mouseRect.x
            ):
                # Down side [=]
                #           <!>
                return utils.getSnapConfig(utils.SnapType.DOWN_SIDE, selectedTile, selectedTile.rotation)
            elif(
                (selectedTile.rotation == utils.RotationType.DOWN or selectedTile.rotation == utils.RotationType.UP) and
                selectedTile.position.y >= mouseRect.y and
                selectedTile.position.x <= mouseRect.x and  
                selectedTile.position.x + utils.defaultImageSizes >= mouseRect.x
            ):
                #         <!>
                # Up side [=]
                return utils.getSnapConfig(utils.SnapType.UP_SIDE, selectedTile, selectedTile.rotation)
                
            elif(
                (selectedTile.rotation == utils.RotationType.LEFT or selectedTile.rotation == utils.RotationType.RIGHT) and
                selectedTile.position.y + utils.defaultImageSizes <= mouseRect.y and
                selectedTile.position.x <= mouseRect.x and  
                selectedTile.position.x + utils.defaultImageSizes >= mouseRect.x
            ):
                return utils.getSnapConfig(utils.SnapType.UP_SIDE, selectedTile, selectedTile.rotation)
            elif(
                (selectedTile.rotation == utils.RotationType.LEFT or selectedTile.rotation == utils.RotationType.RIGHT) and
                selectedTile.position.y >= mouseRect.y and
                selectedTile.position.x <= mouseRect.x and  
                selectedTile.position.x + utils.defaultImageSizes >= mouseRect.x
            ):
                return utils.getSnapConfig(utils.SnapType.DOWN_SIDE, selectedTile, selectedTile.rotation)
            elif(

                (selectedTile.rotation == utils.RotationType.LEFT or selectedTile.rotation == utils.RotationType.RIGHT) and
                selectedTile.position.x + utils.defaultImageSizes < mouseRect.x and 
                selectedTile.position.y <= mouseRect.y and
                selectedTile.position.y + utils.defaultImageSizes >= mouseRect.y
            ):
                return utils.getSnapConfig(utils.SnapType.RIGHT_SIDE, selectedTile, selectedTile.rotation)
            elif(

                (selectedTile.rotation == utils.RotationType.LEFT or selectedTile.rotation == utils.RotationType.RIGHT) and
                selectedTile.position.x > mouseRect.x and
                selectedTile.position.y <= mouseRect.y and
                selectedTile.position.y + utils.defaultImageSizes >= mouseRect.y   
            ):
                return utils.getSnapConfig(utils.SnapType.LEFT_SIDE, selectedTile, selectedTile.rotation)                

        return pygame.Rect(
                mouseRect.x + utils.adjmousePos.x, 
                mouseRect.y + utils.adjmousePos.y, 
                utils.defaultImageSizes, utils.defaultImageSizes
            )

    def updateTilePlacer(self, window):

        mouseEvent, mousePos, snapMode = self.handleInputplacer(window)
        mouseRect = pygame.Rect(mousePos[0], mousePos[1], utils.defaultImageSizes, utils.defaultImageSizes)

        if(not snapMode):

            self.destPreviewRect = pygame.Rect(
                mousePos[0] + utils.adjmousePos.x, 
                mousePos[1] + utils.adjmousePos.y, 
                utils.defaultImageSizes, utils.defaultImageSizes
            )
        else:

            self.destPreviewRect = self.snapModeActivate(window, mouseRect)
                    
        self.drawPreviewPlacer(mousePos, window)

        # utils.debugDraw(window,self.destPreviewRect)
        
        # placing and deleting tiles

        
        detectBox = pygame.Rect(

            self.destPreviewRect.x + 10,
            self.destPreviewRect.y + 10,
            self.destPreviewRect.width - 20,
            self.destPreviewRect.height - 20,
        )

        utils.debugDraw(window, detectBox)

        if(mouseEvent[0]):

            isTilePlaceable = True
            
            for tile in self.tiles:

                if(detectBox.colliderect(utils.getTileRect(tile.position))):
                    isTilePlaceable = False
                    return
            if(isTilePlaceable):
                self.tiles.append(tiles.Tile(
                    pygame.Vector2(self.destPreviewRect.x, self.destPreviewRect.y), 
                    self.selectedTileType, self.defaultRotation
                ))

        if(mouseEvent[2]):

            for tile in self.tiles:

                if(utils.getTileRect(tile.position).collidepoint(mouseRect.x, mouseRect.y)):
                    self.tiles.remove(tile)
                    return

    def getScrollwheelInput(self):
        return utils.scrollWheel

    def update(self, window):

        self.updateTilePlacer(window)

        for tile in self.tiles:

            tile.update(window)

        self.batteryGenator.update(window)
    
    def initTextures(self):

        textures.images["Tiles"]["image"]["surface"] =  pygame.image.load(
            textures.images["Tiles"]["location"]).convert_alpha()

        textures.images["Tiles"]["image"]["surface"] = pygame.transform.scale2x(textures.images["Tiles"]["image"]["surface"]).convert_alpha()

        # Get rotated textures

        textures.images["Tiles"]["rotatedImages"][utils.RotationType.LEFT] = pygame.transform.rotate(
            textures.images["Tiles"]["image"]["surface"],
            utils.rotations[utils.RotationType.LEFT]
        )

        textures.images["Tiles"]["rotatedImages"][utils.RotationType.UP] = pygame.transform.rotate(
            textures.images["Tiles"]["image"]["surface"],
            utils.rotations[utils.RotationType.UP]
        )

        textures.images["Tiles"]["rotatedImages"][utils.RotationType.RIGHT] = pygame.transform.rotate(
            textures.images["Tiles"]["image"]["surface"],
            utils.rotations[utils.RotationType.RIGHT]
        )

        textures.images["Tiles"]["image"]["FrameWidth"] = textures.images["Tiles"]["image"]["surface"].width / textures.images["Tiles"]["maxFramesX"]
        textures.images["Tiles"]["image"]["FrameHeight"] = textures.images["Tiles"]["image"]["surface"].height / textures.images["Tiles"]["FramesY"]
