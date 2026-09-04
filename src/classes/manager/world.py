import pygame
import classes.objects.tiles as tiles
import classes.utility.utils as utils
import classes.bots.bot as bot
import classes.objects.batteryGen as batteryGen
import math
import random
from copy import copy

# Using this temporarly! -> import textures

import classes.utility.textures as textures

class World():

    def __init__(self):

        self.worldPos = pygame.Vector2(0, 0)

        self.tiles = []
        self.bots = []

        self.dev_activateBots = False

        self.initTextures()

        self.currentSelectedSlot = None
        self.currentSelectedSlotIndex = None

        self._addSelectedSlotType = None

        self.batteryGenator = batteryGen.BatteryGenenator()
        self.setupPrieviewTile()
        self.setupObjects()


    def setupObjects(self):

        self.tiles.append(

            tiles.Tile(
                pygame.Vector2(
                300, 200
                ), utils.TileType.SOLAR_PANEL,
                utils.RotationType.DOWN
            )
        )
        self.tiles.append(
            tiles.Tile(
                pygame.Vector2(
                400, 260
                ), utils.TileType.BARRIER,
                utils.RotationType.LEFT
        ))
        self.tiles.append(
            tiles.Tile(
                pygame.Vector2(
                600, 230
                ), utils.TileType.SOLAR_PANEL,
                utils.RotationType.LEFT
        ))

        bot.Bot.setBatteryPos(self.batteryGenator.position)

        self.bots.append(
            bot.Bot(pygame.Vector2(800, 700), self.batteryGenator.position)
        )

    def updateTileSrcRect(self):

        self.previewTile["image"].set_alpha(100)
        self.previewTile["srcRect"] = utils.configureRotatedImageForPreview(
            textures.images["Tiles"]["image"]["FrameWidth"],
            textures.images["Tiles"]["image"]["FrameHeight"],
            self.selectedTileType,
            self.defaultRotation
        )

    def setupPrieviewTile(self):

        self.defaultRotation = utils.RotationType.DOWN
        self.previewTile = {

            "image": textures.images["Tiles"]["image"]["surface"].copy(),
            "srcRect": None
        }
        
        self.selectedTileType = utils.TileType.SOLAR_PANEL

        self.destPreviewRect = pygame.Vector2(0, 0)

    def setCurrentselectedSlot(self, slot):
        self.currentSelectedSlot = slot

    def drawPreviewPlacer(self, window):
        
        window.blit(
            self.previewTile["image"], 
            pygame.Vector2(self.destPreviewRect.x, self.destPreviewRect.y), 
            self.previewTile["srcRect"]
        )

    def handleInputplacer(self):

        mousePos = pygame.mouse.get_pos()
        mouseEvent = pygame.mouse.get_just_pressed()
        keypress = pygame.key.get_just_pressed()
        keypressing = pygame.key.get_pressed()      

        snapMode = False

        # The Left CTRL is support for left-handed keyboards

        if(keypressing[pygame.K_RCTRL] or keypressing[pygame.K_LCTRL]):
            snapMode = True

        # Make them rotate when input and do stuff to get it working right :)

        if(utils.scrollWheel.y != 0 or keypress[pygame.K_r]):
            self.rotationPreviewTile()

        return mouseEvent, mousePos, snapMode

    def rotationPreviewTile(self):

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

    def checkNieghborTileForSnapping(self, detectAreaRange: pygame.Rect, mouseRect: pygame.Rect):

        selectedTile = None
        
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

        return selectedTile

    def activateSnapping(self, window, mouseRect):
        
        detectAreaRange = pygame.Rect(
            (mouseRect.x + utils.adjmousePos.x) - utils.defaultImageSizes / 2, 
            (mouseRect.y + utils.adjmousePos.y) - utils.defaultImageSizes / 2, 
            utils.defaultImageSizes * 2, utils.defaultImageSizes * 2
        )

        utils.debugDraw(window, detectAreaRange)

        selectedTile = self.checkNieghborTileForSnapping(detectAreaRange, mouseRect)
        return self.findSnapSpot(selectedTile, mouseRect, window)

    def findSnapSpot(self, selectedTile, mouseRect, window):

        if(selectedTile != None):

            utils.debugDraw(window, pygame.Rect(selectedTile.position.x, selectedTile.position.y, utils.defaultImageSizes, utils.defaultImageSizes))

            for i in range(utils.SnapType.__len__()):
                for j in range(utils.dirType.__len__()):

                    if(utils.isRightSnapConfig(utils.SnapType(i), selectedTile,utils.dirType(j), mouseRect)):

                        return utils.getSnapConfig(utils.SnapType(i), selectedTile, selectedTile.rotation)
                
        return pygame.Rect(
                mouseRect.x + utils.adjmousePos.x, 
                mouseRect.y + utils.adjmousePos.y, 
                utils.defaultImageSizes, utils.defaultImageSizes
            )

    def getRegularRect(self, mouseRect: pygame.Rect):

        return pygame.Rect(
            mouseRect.x + utils.adjmousePos.x, 
            mouseRect.y + utils.adjmousePos.y, 
            utils.defaultImageSizes, utils.defaultImageSizes
        )

    def handleplacingTiles(self, mouseEvent, mouseRect: pygame.Rect):

        detectBox = pygame.Rect(

            self.destPreviewRect.x + utils.detectBoxAdj.x,
            self.destPreviewRect.y + utils.detectBoxAdj.x,
            self.destPreviewRect.width + utils.detectBoxAdj.y,
            self.destPreviewRect.height + utils.detectBoxAdj.y,
        )

        if(mouseEvent[0] and utils.activateTilePlacer and self.selectedTileType != None):

            isTilePlaceable = True

            if(self.selectedTileType != utils.TileType.BARRIER and len(self.tiles) != 0):
                for tile in self.tiles:

                    if(detectBox.colliderect(utils.getTilesDetectRect(tile.position))):
                        isTilePlaceable = False
                        return
            if(isTilePlaceable):

                if(self.currentSelectedSlot != None):

                    if(self.currentSelectedSlot.amount >= 1):
                        self.currentSelectedSlot.amount -= 1
                    else:
                        self.currentSelectedSlot = None
                        return

                self.tiles.append(tiles.Tile(
                    pygame.Vector2(self.destPreviewRect.x, self.destPreviewRect.y), 
                    self.selectedTileType, self.defaultRotation
                ))

        if(mouseEvent[2]):

            for tile in self.tiles:

                if(utils.getTileRect(tile.position).collidepoint(mouseRect.x, mouseRect.y)):

                    self._addSelectedSlotType = utils.convertToItemType(tile.type)
                    self.tiles.remove(tile)
                    return

    # This communicater func to other classes

    def giveAddSelectedSlotType(self):

        if(self._addSelectedSlotType == None):
            return None

        _copy = copy(self._addSelectedSlotType)
        self._addSelectedSlotType = None

        return _copy

    def updateTilePlacer(self, window):

        if(utils.activateTilePlacer and self.selectedTileType != None):
            self.updateTileSrcRect()

        mouseEvent, mousePos, snapMode = self.handleInputplacer()
        mouseRect = pygame.Rect(mousePos[0], mousePos[1], utils.defaultImageSizes, utils.defaultImageSizes)

        self.destPreviewRect = self.activateSnapping(window, mouseRect) if(snapMode) else self.getRegularRect(mouseRect)
        if(utils.activateTilePlacer and self.selectedTileType != None):      
            self.drawPreviewPlacer(window)

        self.handleplacingTiles(mouseEvent, mouseRect)

    def update(self, window):

        if(self.currentSelectedSlot != None):

            if(self.currentSelectedSlot.amount == 0):
                self.currentSelectedSlot.type = utils.ItemType.NONE

            self.selectedTileType = utils.convertToTileType(self.currentSelectedSlot.type)
        else:
            self.selectedTileType = None


        key = pygame.key.get_just_pressed()

        if(key[pygame.K_b]):
            self.dev_activateBots = not self.dev_activateBots

        self.updateTilePlacer(window)

        for tile in self.tiles:

            tile.update(window)

        self.batteryGenator.update(window, self.tiles)

        if(self.dev_activateBots):
            self.dev_deployBots()


        for bot in self.bots:

            bot.update(window, self.tiles)

    def dev_deployBots(self):

        x = float(random.randint(0, 1000))
        y = float(random.randint(0, 800))

        self.bots.append(bot.Bot(pygame.Vector2(x, y), self.batteryGenator.position))
    
    def initTextures(self):

        # textures.images["Tower"]

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