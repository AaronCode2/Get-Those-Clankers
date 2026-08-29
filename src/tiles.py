import pygame
import textures

class Tile:

    def __init__(self, position: pygame.Vector2, type):

        self.position = position
        self.type = type
        self.width = textures.images["Tiles"]["image"]["FrameWidth"]
        self.height = textures.images["Tiles"]["image"]["FrameHeight"]

        self.srcRect = pygame.Rect(
            0, 0,
            self.width, self.height
        )

    def update(self, window):

        self.draw(window)

    def draw(self, window):

        window.blit(textures.images["Tiles"]["image"]["surface"], self.position, self.srcRect)