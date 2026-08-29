import pygame
import utils
from pygame._sdl2 import Window

class Game():

    def __init__(self, width, height, fps):

        
        self.window = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        Window.from_display_module().maximize()

        self.running = True
        self.fps = fps
        self.clock = pygame.time.Clock()

        self.fillColor = (86, 88, 123)
        self.font = pygame.font.Font("assets/fonts/jetbrains.ttf", 30)

    def update(self):

        # This where everything should go e.g player.update()
        pass

    def processEvents(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

    def updateGameLoop(self):

        while(self.running):

            self.processEvents()

            fpsText = self.font.render(str(int(self.clock.get_fps())), True, (255, 0, 0))

            utils.deltaTime = self.clock.tick(self.fps) / 1000

            self.window.fill(self.fillColor)

            self.update()

            # A simple fps toggle to check performance

            key = pygame.key.get_just_pressed()
            
            if(key[pygame.K_e]):

                if(self.fps == 0):
                    self.fps = 60
                else:
                    self.fps = 0

            self.window.blit(fpsText, (100, 100))

            pygame.display.flip()


    def run(self):

        self.updateGameLoop()
        pygame.quit()   