import pygame
import classes.utility.textures as textures
import classes.utility.utils as utils
from time import time

class Dialog():

    def __init__(self):

        textures.images["Char"]["image"]["surface"] = pygame.image.load(textures.images["Char"]["location"]).convert_alpha()
        textures.images["Char"]["image"]["surface"] = pygame.transform.scale2x(textures.images["Char"]["image"]["surface"])

        self.textTimeStamp = time()
        self.pauseMoment = int(time())
        self.indexText = 0
        self.toDisplayText = ""
        self.writtendialog = ""

        # self.activateDialog("Hi Julien, Hi Gurujezz! Look I'm a robot")

    def drawText(self, window, writtenText: str):

        writtenTextWords = writtenText.split()

        if(time() - self.textTimeStamp > 0.2):

            if(self.indexText < len(writtenTextWords)):
                self.toDisplayText += " " + writtenTextWords[self.indexText]
                self.indexText += 1
                self.textTimeStamp = time()
                self.pauseMoment = int(time())
                self.done = True

            if(int(time()) - self.pauseMoment > 4 and self.done == True):
                self.writtendialog = ""

        text = utils.smfont.render(self.toDisplayText, True, utils.ColorPlattes["Pale White"])

        utils.dev_updatePositionsAdjuster()

        window.blit(text, utils.dialogTextPos)

    def update(self, window):

        if(self.writtendialog != ""):
            self.draw(window)

    def drawChar(self, window):

        window.blit(textures.images["Char"]["image"]["surface"], utils.charPos)

    def drawBackground(self, window):

        textures.drawGuiPlates(window, pygame.Vector2(14, 2), utils.backgroundDailogPos)
        textures.drawGuiPlates(window, pygame.Vector2(2, 2), utils.backgroundDailogPos, utils.TypeOfGuiPlates.MARGIN)

    def activateDialog(self, text):
        self.writtendialog = text
    
    def draw(self, window):

        self.drawBackground(window)
        self.drawChar(window)
        self.drawText(window, self.writtendialog)