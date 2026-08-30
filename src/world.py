import pygame
import tiles
import utils
import batteryGen

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

        self.previewTile["image"].set_alpha(100)
        self.previewTile["srcRect"] = utils.configureRotatedImageForPreview(
                textures.images["Tiles"]["image"]["FrameWidth"],
                textures.images["Tiles"]["image"]["FrameHeight"],
                utils.TileType.BARRIER,
                self.defaultRotation
        )
        self.destPreviewRect = pygame.Vector2(0, 0)

        # self.tiles.append(

        #     tiles.Tile(
        #         pygame.Vector2(
        #         utils.screenRect.width / 2, utils.screenRect.height / 2
        #         ), utils.TileType.BATTERY_FULL,
        #         utils.RotationType.DOWN
        #     )
        # )

    def drawPreviewPlacer(self, mousePos, window):
        
        window.blit(
            self.previewTile["image"], 
            pygame.Vector2(self.destPreviewRect.x, self.destPreviewRect.y), 
            self.previewTile["srcRect"]
        )

    def _devTilePlacer(self, window):

        mousePos = pygame.mouse.get_pos()
        mouseEvent = pygame.mouse.get_just_pressed()
        keypress = pygame.key.get_just_pressed()

        mouseRect = pygame.Rect(mousePos[0], mousePos[1], utils.defaultImageSizes, utils.defaultImageSizes)
        self.drawPreviewPlacer(mousePos, window)

        self.destPreviewRect = pygame.Rect(
            mousePos[0] + utils.adjmousePos.x, 
            mousePos[1] + utils.adjmousePos.y, 
            utils.defaultImageSizes, utils.defaultImageSizes
        )

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
                utils.TileType.BARRIER,
                self.defaultRotation
            )

            utils.scrollWheel = pygame.Vector2(0, 0)

        # placing and deleting tiles

        if(mouseEvent[0]):

            self.tiles.append(tiles.Tile(
                pygame.Vector2(self.destPreviewRect.x, self.destPreviewRect.y), 
                utils.TileType.BARRIER, self.defaultRotation
            ))

        if(mouseEvent[2]):

            for tile in self.tiles:

                if(mouseRect.colliderect(pygame.Rect(
                    tile.position.x, tile.position.y, 
                    utils.defaultImageSizes, utils.defaultImageSizes
                ))):
                    self.tiles.remove(tile)
                    return

    def getScrollwheelInput(self):
        return utils.scrollWheel

    def update(self, window):

        self._devTilePlacer(window)

        for tile in self.tiles:

            tile.update(window)

        self.batteryGenator.update(window)

        # window.blit(textures.images["Tiles"]["image"]["surface"], (200, 200))
    
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
