import pygame
import classes.utility.utils as utils
import classes.utility.textures as textures
import classes.ui.inventory as inventory
import classes.utility.animation as animation

class UI():

    def __init__(self):

        self.configureImages()

        self.batteryIndicator = animation.AnimationManager(
            textures.images["batteryIndicator"]["location"],
            textures.images["batteryIndicator"]["FramesY"],
            [textures.images["batteryIndicator"]["FramesX"]] * 6,
            textures.images["batteryIndicator"]["animationNames"],
            True
        )

        self.wattsUsed = "10W"
        self.wattsGenerated = "10W"
        self.timeLeft = 120

        self.inventory = inventory.Inventory()

        self.batteryIndicator.position = pygame.Vector2(utils.batteryIndicatorPos.x, utils.batteryIndicatorPos.y)
        self.batteryIndicator.level = utils.BatteryLevel.BATTERY_FULL
        self.batteryIndicator.set_animation(textures.images["batteryIndicator"]["animationNames"][self.batteryIndicator.level.value])
        self.batteryIndicator.animation_speed = 1


    def setBatteryStuff(self, batteryLevel, timeLeft, wattsUsed, wattsGenerated):

        self.timeLeft = "Time:" + utils.formatToClock(timeLeft)
        self.wattsUsed = "Used:" + str(wattsUsed) + "W"
        self.wattsGenerated = "Made:" + str(wattsGenerated) + "W"

        if(self.batteryIndicator.level != batteryLevel):
            self.batteryIndicator.level = batteryLevel
            self.batteryIndicator.set_animation(textures.images["batteryIndicator"]["animationNames"][self.batteryIndicator.level.value])

    def update(self, window):

        keypress = pygame.key.get_just_pressed()

        if(keypress[pygame.K_e]):
            self.inventory.toggle = not self.inventory.toggle

        self.draw(window)

    def draw(self, window):

        self.displayKeyGuides(window)
        self.drawBatteryDisplayHud(window)

        if(self.inventory.toggle):
            self.drawInventory(window)

        self.drawHotBar(window)

    def drawInventory(self, window):

        inventoryPos = pygame.Vector2(

            utils.screenRect.width - utils.inventoryPosAdj.x,
            utils.screenRect.height - utils.inventoryPosAdj.y,
        )

        self.drawGuiPlates(window, pygame.Vector2(6, 8), inventoryPos)

    def drawHotBar(self, window):

        hotBarPos = pygame.Vector2(

            utils.screenRect.width - utils.HotBarPosAdj.x,
            utils.screenRect.height - utils.HotBarPosAdj.y,
        )

        self.drawGuiPlates(window, pygame.Vector2(6, 2), hotBarPos)
        self.inventory.update(window)

    def drawBatteryDisplayHud(self, window):

        self.drawGuiPlates(window, pygame.Vector2(4, 3), pygame.Vector2(10, 10))

        textTimeLeft = utils.font.render(self.timeLeft, True, utils.ColorPlattes["Future Blue"])
        textWattsUsed = utils.font.render(self.wattsUsed, True, utils.ColorPlattes["Future Blue"])
        textwattsMade = utils.font.render(self.wattsGenerated, True, utils.ColorPlattes["Future Blue"])

        window.blit(textTimeLeft, utils.BatteryDisplayHudPositions["TimeLeft"])
        window.blit(textWattsUsed, utils.BatteryDisplayHudPositions["WattsUsed"])
        window.blit(textwattsMade, utils.BatteryDisplayHudPositions["WattsGenerated"])

        # The utils.deltaTime might be causing this Julien

        self.batteryIndicator.update(utils.deltaTime)
        window.blit(self.batteryIndicator.current_frame, self.batteryIndicator.position)


    def drawGuiPlates(self, window, size: pygame.Vector2, position: pygame.Vector2):

        for y in range(int(size.y)):
            for x in range(int(size.x)):

                platePosition = pygame.Vector2(

                    textures.images["keys"]["image"]["FrameWidth"] * x + position.x,
                    textures.images["keys"]["image"]["FrameHeight"] * y + position.y,
                ) 
                
                srcRect = self.configureguiPlateSelection(x, y, size)
                
                window.blit(textures.images["guiPlates"]["image"]["surface"], platePosition, srcRect)

    def configureguiPlateSelection(self, x: int, y: int, size: pygame.Vector2):

        if(y == 0 and x != 0 and x != size.x - 1):
                return pygame.Rect(
                    textures.images["guiPlates"]["image"]["FrameWidth"] * float(utils.guiPlatesFrameMap[utils.GuiPlates.TOP_MIDDLE][0]), 
                    0,
                    textures.images["guiPlates"]["image"]["FrameWidth"],
                    textures.images["guiPlates"]["image"]["FrameHeight"]
                )
        elif(y == 0 and x == size.x - 1):
            return pygame.Rect(
                textures.images["guiPlates"]["image"]["FrameWidth"] * float(utils.guiPlatesFrameMap[utils.GuiPlates.CORNER_TOP_RIGHT][0]), 
                0,
                textures.images["guiPlates"]["image"]["FrameWidth"],
                textures.images["guiPlates"]["image"]["FrameHeight"]
            )
        elif(y != 0 and x == 0 and y != size.y - 1):
            return pygame.Rect(
                textures.images["guiPlates"]["image"]["FrameWidth"] * float(utils.guiPlatesFrameMap[utils.GuiPlates.MIDDLE_LEFT_SIDE][0]), 
                textures.images["guiPlates"]["image"]["FrameHeight"] * float(utils.guiPlatesFrameMap[utils.GuiPlates.MIDDLE_LEFT_SIDE][1]),
                textures.images["guiPlates"]["image"]["FrameWidth"],
                textures.images["guiPlates"]["image"]["FrameHeight"]
            )
        elif(y != 0 and x != 0 and y != size.y - 1 and x != size.x - 1):
            return pygame.Rect(
                textures.images["guiPlates"]["image"]["FrameWidth"] * float(utils.guiPlatesFrameMap[utils.GuiPlates.MIDDLE][0]), 
                textures.images["guiPlates"]["image"]["FrameHeight"] * float(utils.guiPlatesFrameMap[utils.GuiPlates.MIDDLE][1]),
                textures.images["guiPlates"]["image"]["FrameWidth"],
                textures.images["guiPlates"]["image"]["FrameHeight"]
            )
        elif(y != 0 and y != size.y - 1 and x == size.x - 1):
            return pygame.Rect(
                textures.images["guiPlates"]["image"]["FrameWidth"] * float(utils.guiPlatesFrameMap[utils.GuiPlates.MIDDLE_RIGHT_SIDE][0]), 
                textures.images["guiPlates"]["image"]["FrameHeight"] * float(utils.guiPlatesFrameMap[utils.GuiPlates.MIDDLE_RIGHT_SIDE][1]),
                textures.images["guiPlates"]["image"]["FrameWidth"],
                textures.images["guiPlates"]["image"]["FrameHeight"]
            )
        elif(y == size.y - 1 and x == 0):
            return pygame.Rect(
                textures.images["guiPlates"]["image"]["FrameWidth"] * float(utils.guiPlatesFrameMap[utils.GuiPlates.CORNER_BOTTOM_LEFT][0]), 
                textures.images["guiPlates"]["image"]["FrameHeight"] * float(utils.guiPlatesFrameMap[utils.GuiPlates.CORNER_BOTTOM_LEFT][1]),
                textures.images["guiPlates"]["image"]["FrameWidth"],
                textures.images["guiPlates"]["image"]["FrameHeight"]
            )
        elif(y == size.y - 1 and x != 0 and x != size.x - 1):
            return pygame.Rect(
                textures.images["guiPlates"]["image"]["FrameWidth"] * float(utils.guiPlatesFrameMap[utils.GuiPlates.BOTTOM_MIDDLE][0]), 
                textures.images["guiPlates"]["image"]["FrameHeight"] * float(utils.guiPlatesFrameMap[utils.GuiPlates.BOTTOM_MIDDLE][1]),
                textures.images["guiPlates"]["image"]["FrameWidth"],
                textures.images["guiPlates"]["image"]["FrameHeight"]
            )
        elif(y == size.y - 1 and x == size.x - 1):
            return pygame.Rect(
                textures.images["guiPlates"]["image"]["FrameWidth"] * float(utils.guiPlatesFrameMap[utils.GuiPlates.CORNER_BOTTOM_RIGHT][0]), 
                textures.images["guiPlates"]["image"]["FrameHeight"] * float(utils.guiPlatesFrameMap[utils.GuiPlates.CORNER_BOTTOM_RIGHT][1]),
                textures.images["guiPlates"]["image"]["FrameWidth"],
                textures.images["guiPlates"]["image"]["FrameHeight"]
            )

        return pygame.Rect(
            0, 0, 
            textures.images["keys"]["image"]["FrameWidth"],
            textures.images["keys"]["image"]["FrameHeight"]
        )

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
