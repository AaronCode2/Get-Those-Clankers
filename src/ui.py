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

        self.drawGuiPlates(window, pygame.Vector2(3, 3), pygame.Vector2(300, 400))

    def drawGuiPlates(self, window, size: pygame.Vector2, position: pygame.Vector2):

        # TODO: Get this working

        for y in range(int(size.y)):
            for x in range(int(size.x)):

                srcRect = pygame.Rect(
                    0, 0, 
                    textures.images["keys"]["image"]["FrameWidth"],
                    textures.images["keys"]["image"]["FrameHeight"]
                )

                platePosition = pygame.Vector2(

                    textures.images["keys"]["image"]["FrameWidth"] * x + position.x,
                    textures.images["keys"]["image"]["FrameHeight"] * y + position.y,
                ) 
                
                if(y == 0 and x == 0):
                    srcRect = pygame.Rect(
                        0, 0,
                        textures.images["keys"]["image"]["FrameWidth"],
                        textures.images["keys"]["image"]["FrameHeight"]
                    )
                
                window.blit(textures.images["guiPlates"]["image"]["surface"], platePosition, srcRect)

    def displayKeyGuides(self, window):

        for i in range(textures.images["keys"]["maxFramesX"]):

            textguide = utils.font.render(utils.keyGuidesTexts[utils.KeyGuides(i)], True, (0, 0, 0))
            
            position = pygame.Vector2(
                (textures.images["keys"]["image"]["FrameWidth"] * i) + 
                utils.keyGuidesTexts["textOffsets"][utils.KeyGuides(i)] + 5.0,
                (utils.screenRect.height - textures.images["keys"]["image"]["FrameHeight"]), 
            )

            positionText = pygame.Vector2(
                textures.images["keys"]["image"]["FrameWidth"] * i + 
                utils.keyGuidesTexts["textOffsets"][utils.KeyGuides(i)] + 68.0,
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

        textures.images["guiPlates"]["image"]["surface"] =  pygame.image.load(textures.images["guiPlates"]["location"]).convert_alpha()
        textures.images["guiPlates"]["image"]["surface"] = pygame.transform.scale2x(textures.images["guiPlates"]["image"]["surface"])

        textures.images["guiPlates"]["image"]["FrameWidth"] = textures.images["guiPlates"]["image"]["surface"].width / textures.images["guiPlates"]["FramesX"] 
        textures.images["guiPlates"]["image"]["FrameHeight"] = textures.images["guiPlates"]["image"]["surface"].height / textures.images["guiPlates"]["FramesY"] 
