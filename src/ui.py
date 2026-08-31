import pygame
import utils
import textures

class UI():

    def __init__(self):

        self.configureImages()

    def update(self, window):

        self.draw(window)

    def draw(self, window):

        self.displayKeyGuides(window)

    def displayKeyGuides(self, window):

        for i in range(textures.images["keys"]["maxFramesX"]):

            textguide = utils.font.render(utils.keyGuidesTexts[utils.keyGuides(i)], True, (0, 0, 0))
            
            position = pygame.Vector2(
                (textures.images["keys"]["image"]["FrameWidth"] * i) + 
                utils.keyGuidesTexts["textOffsets"][utils.keyGuides(i)] + 5.0,
                (utils.screenRect.height - textures.images["keys"]["image"]["FrameHeight"]), 
            )

            positionText = pygame.Vector2(
                textures.images["keys"]["image"]["FrameWidth"] * i + 
                utils.keyGuidesTexts["textOffsets"][utils.keyGuides(i)] + 68.0,
                (utils.screenRect.height - textures.images["keys"]["image"]["FrameHeight"] + 5), 
            )

            srcRect = pygame.Rect(
                textures.images["keys"]["image"]["FrameWidth"] * i,
                0,
                textures.images["keys"]["image"]["FrameWidth"],
                textures.images["keys"]["image"]["FrameHeight"] 
            )

            window.blit(textguide, positionText)
            window.blit(textures.images["keys"]["image"]["surface"], position, srcRect)
    
    def configureImages(self):

        textures.images["keys"]["image"]["surface"] =  pygame.image.load(textures.images["keys"]["location"]).convert_alpha()
        textures.images["keys"]["image"]["surface"] = pygame.transform.scale2x(textures.images["keys"]["image"]["surface"])

        textures.images["keys"]["image"]["FrameWidth"] = textures.images["keys"]["image"]["surface"].width / textures.images["keys"]["maxFramesX"] 
        textures.images["keys"]["image"]["FrameHeight"] = textures.images["keys"]["image"]["surface"].height 