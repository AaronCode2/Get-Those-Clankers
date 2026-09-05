import pygame
import classes.objects.tiles as tiles
import classes.utility.utils as utils
import classes.bots.bot as bot
import classes.utility.animation as animation
import classes.objects.batteryGen as batteryGen
import classes.objects.bullet as bullet
import classes.objects.player as player
import classes.manager.camera as camera
import math
import random
from copy import copy
import classes.utility.textures as textures
import classes.objects.dropItem as dropItem

class World():

    def __init__(self):

        self.worldPos = pygame.Vector2(0, 0)

        self.tiles = []
        self.bots = []
        self.player = player.Player(pygame.Vector2(500, 500))
        self.camera = camera.Camera()

        self.dev_activateBots = False
        self.dev_destroyBots = False

        bullet.Bullet.giveBots(self.bots)

        self.initTextures()

        self.currentSelectedSlot = None
        self.currentSelectedSlotIndex = None

        self._addSelectedSlotType = None
        self.pickedDroppedItem = None

        self.batteryGenator = batteryGen.BatteryGenenator()
        self.setupPrieviewTile()
        self.setupObjects()

    def setupObjects(self):

        bullet.bullets.append(bullet.Bullet(pygame.Vector2(300, 200), pygame.Vector2(400, 400)))

        self.tiles.append(

            tiles.Tile(
                pygame.Vector2(
                300, 200
                ), utils.TileType.GREEN_TOWER,
                utils.RotationType.DOWN
            )
        )
        self.tiles.append(
            tiles.Tile(
                pygame.Vector2(
                400, 260
                ), utils.TileType.STRONG_BARRIER,
                utils.RotationType.LEFT
        ))
        self.tiles.append(
            tiles.Tile(
                pygame.Vector2(
                600, 230
                ), utils.TileType.STRONGER_BARRIER,
                utils.RotationType.UP
        ))

        bot.Bot.setBatteryPos(self.batteryGenator.position)

    def updateTileSrcRect(self):

        if(self.selectedTileType != None):

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

        if(self.selectedTileType != utils.TileType.GREEN_TOWER):
        
            window.blit(
                self.previewTile["image"], 
                pygame.Vector2(self.destPreviewRect.x, self.destPreviewRect.y), 
                self.previewTile["srcRect"]
            )
        else:

            window.blit(
                textures.images["Tower"]["image"]["Animation"].current_frame, 
                pygame.Vector2(self.destPreviewRect.x, self.destPreviewRect.y), 
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

        # selectedTileType is The tile that is selected in inventory

        if(self.selectedTileType != None):

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

            if(len(self.tiles) != 0):
                for tile in self.tiles:

                    if(detectBox.colliderect(tile.getHitBox())):
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

        # Update The towers
        camera_items: list[camera.CameraItem] = []

        textures.images["Tower"]["image"]["Animation"].update()

        if(self.currentSelectedSlot != None):

            if(self.currentSelectedSlot.amount == 0):
                self.currentSelectedSlot.type = utils.ItemType.NONE

            self.selectedTileType = utils.convertToTileType(self.currentSelectedSlot.type)
        else:
            self.selectedTileType = None


        key = pygame.key.get_just_pressed()

        if(key[pygame.K_b]):
            self.dev_activateBots = not self.dev_activateBots
        elif(key[pygame.K_k]):
            self.dev_destroyBots = not self.dev_destroyBots

        self.updateTilePlacer(window)

        for tile in self.tiles:

            camera_items += tile.update(window)

            if(tile.type == utils.TileType.GREEN_TOWER):
                tile.towerFunc(self.bots)


        camera_items.append(self.batteryGenator.update(window, self.tiles, self.player.velocity))

        if(self.dev_activateBots):
            self.dev_deployBots()

        if(self.dev_destroyBots):
            self.bots = []

        # When player touches drop Item, it added to inventory

        camera_items += self.updateDroppedItems(window)

        self.player.update(self.tiles)
        camera_items += self.player.draw(window, debug=True)

        for bot in self.bots:
            bot.update(self.tiles)
            camera_items += bot.draw(window, debug=True)

        for singleBullet in bullet.bullets:

            if(singleBullet.destroyBullet):
                bullet.bullets.remove(singleBullet)

            singleBullet.update(window)

        self.camera.draw(camera_items, self.player.hitbox.midbottom, window)

    def updateDroppedItems(self, window):
        camera_items: list[camera.CameraItem] = []
        for droppedItem in dropItem.droppedItems:

            camera_items.append(droppedItem.update(window, self.player.hitbox.center))

            if(self.player.rect.colliderect(pygame.Rect(
                droppedItem.position.x,
                droppedItem.position.y,
                textures.images["Items"]["image"]["FrameWidth"],
                textures.images["Items"]["image"]["FrameHeight"]
            ))):

                self.pickedDroppedItem = (droppedItem.getItem())
                dropItem.droppedItems.remove(droppedItem)
        return camera_items

    def dev_deployBots(self):

        whereBotAppear = utils.BotAppearings(random.randint(0, 3))
        extraSpace = utils.BotsSpaceings

        match(whereBotAppear):

            case utils.BotAppearings.SIDE_RIGHT_SCREEN:

                x = -extraSpace
                y = random.randint(-extraSpace, utils.screenRect.height + extraSpace)

            case utils.BotAppearings.SIDE_LEFT_SCREEN:

                x = utils.screenRect.width + extraSpace
                y = random.randint(-extraSpace, utils.screenRect.height + extraSpace)

            case utils.BotAppearings.SIDE_TOP_SCREEN:

                x = random.randint(-extraSpace, utils.screenRect.width + extraSpace)
                y = -extraSpace

            case utils.BotAppearings.SIDE_BOTTOM_SCREEN:

                x = random.randint(-extraSpace, utils.screenRect.width + extraSpace)
                y = utils.screenRect.height + extraSpace

        self.bots.append(bot.Bot(pygame.Vector2(x, y), self.batteryGenator.position))

    def givePickedDroppedItem(self):

        currentpickedItem = self.pickedDroppedItem

        self.pickedDroppedItem = None
        return currentpickedItem

    def initTextures(self):


        textures.images["Items"]["image"]["surface"] = pygame.image.load(textures.images["Items"]["location"]).convert_alpha()

        textures.images["Items"]["image"]["FrameWidth"] = textures.images["Items"]["image"]["surface"].width / textures.images["Items"]["FramesX"]
        textures.images["Items"]["image"]["FrameHeight"] = textures.images["Items"]["image"]["surface"].height

        textures.images["Tower"]["image"]["Animation"] = animation.AnimationManager(

            textures.images["Tower"]["location"],
            textures.images["Tower"]["FramesY"],
            [textures.images["Tower"]["FramesX"]],
            [textures.images["Tower"]["AnimationNames"]],
            2
        )

        textures.images["Tower"]["image"]["Animation"].set_animation(textures.images["Tower"]["AnimationNames"])
        textures.images["Tower"]["image"]["FrameWidth"] = textures.images["Tower"]["image"]["Animation"].frame_width
        textures.images["Tower"]["image"]["FrameHeight"] = textures.images["Tower"]["image"]["Animation"].frame_height
        textures.images["Tower"]["image"]["Animation"].animation_speed = 10
        
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