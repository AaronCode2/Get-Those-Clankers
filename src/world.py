import pygame
import tiles
import utils

# Using this temporarly!

import textures

class World():

    def __init__(self):

        self.worldPos = pygame.Vector2(0, 0)
        self.tiles = []

        textures.images["Tiles"]["image"]["surface"] =  pygame.image.load(
            textures.images["Tiles"]["location"])

        textures.images["Tiles"]["image"]["surface"] = pygame.transform.scale2x(textures.images["Tiles"]["image"]["surface"])

        textures.images["Tiles"]["image"]["FrameWidth"] = textures.images["Tiles"]["image"]["surface"].width / textures.images["Tiles"]["maxFramesX"]
        textures.images["Tiles"]["image"]["FrameHeight"] = textures.images["Tiles"]["image"]["surface"].height / textures.images["Tiles"]["FramesY"]

        self.tiles.append(tiles.Tile(pygame.Vector2(200, 200), utils.TileType.BARRIER))

    def update(self, window):

        for tile in self.tiles:

            tile.update(window)

        # window.blit(textures.images["Tiles"]["image"]["surface"], (200, 200))