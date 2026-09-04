import pygame
import classes.utility.utils as utils
import classes.manager.world as world
import classes.ui.ui as ui
from pygame._sdl2 import Window

class Game():

    def __init__(self, width, height, fps):

        
        self.window = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        Window.from_display_module().maximize()

        self.running = True
        self.fps = fps
        self.clock = pygame.time.Clock()

        self.fillColor = (86, 88, 123)
        utils.font = pygame.font.Font("assets/fonts/jetbrains.ttf", 30)
        utils.smfont = pygame.font.Font("assets/fonts/jetbrains.ttf", 24)
        utils.ssmfont = pygame.font.Font("assets/fonts/jetbrains.ttf", 15)

        utils.screenRect = pygame.Rect(0, 0, self.window.width, self.window.height)

        self.world = world.World()
        self.ui = ui.UI()

    def update(self):

        # This where everything should go e.g player.update()
        self.world.update(self.window)

        # We need to convert Item To Tile, since their diffrenet classes

        self.ui.addStuffToInventory(self.world.giveAddSelectedSlotType(), 1)
        self.ui.update(self.window)

    def processEvents(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEWHEEL:

                utils.scrollWheel = pygame.Vector2(event.x, event.y)

    def updateGameLoop(self):

        while(self.running):

            self.processEvents()

            fpsText = utils.font.render(str(int(self.clock.get_fps())), True, (255, 0, 0))

            utils.deltaTime = self.clock.tick(self.fps) / 1000

            utils.windowResized = False

            if(utils.screenRect.width != self.window.width or utils.screenRect.height != self.window.height):
                utils.screenRect.width = self.window.width
                utils.screenRect.height = self.window.height
                utils.windowResized = True

            self.window.fill(self.fillColor)

            self.update()

            # A simple fps toggle to check performance

            key = pygame.key.get_just_pressed()
            
            if(key[pygame.K_z]):

                if(self.fps == 0):
                    self.fps = 60
                else:
                    self.fps = 0

            self.window.blit(fpsText, (utils.screenRect.width - 300, 100))

            pygame.display.flip()

    def run(self):

        self.updateGameLoop()
        pygame.quit()   