import pygame
import asyncio
import pygame
import classes.utility.utils as utils
import classes.manager.world as world
import classes.manager.camera as camera
import classes.ui.ui as ui
import classes.objects.player as player
import asyncio

async def init():

    # game = Game(1000, 600, 60)
    # asyncio.run(game.updateGameLoop())

            # pygame.display.set_caption("Get Those Clankers!")

    width = 1000
    height = 600

    running = True
    fps = 60
    clock = None

    fillColor = utils.ColorPlattes["Purple Moose"]

    pygame.init()

    window = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    pygame.font.init()

    utils.font = pygame.font.Font("assets/fonts/jetbrains.ttf", 30)
    utils.smfont = pygame.font.Font("assets/fonts/jetbrains.ttf", 24)
    utils.ssmfont = pygame.font.Font("assets/fonts/jetbrains.ttf", 15)

    utils.screenRect = pygame.Rect(0, 0, window.width, window.height)

    gameWorld = world.World()
    gameUI = ui.UI()

    while(running):

        fpsText = utils.font.render(str(int(clock.get_fps())), True, (255, 0, 0))

        utils.deltaTime = clock.tick(fps) / 1000

        utils.windowResized = False

        if(utils.screenRect.width != window.width or utils.screenRect.height != window.height):
            utils.screenRect.width = window.width
            utils.screenRect.height = window.height
            utils.windowResized = True

        window.fill(fillColor)

         # This where everything should go e.g player.update()
        
        
        # We need to convert Item To Tile, since their diffrenet Enums

        gameUI.addStuffToInventory(gameWorld.giveAddSelectedSlotType(), 1)

        if(gameWorld.pickedDroppedItem != None):

            pickedItem = gameWorld.givePickedDroppedItem()

            gameUI.addStuffToInventory(
                pickedItem[0], 
                pickedItem[1]
            )

        #! DrawLayer BUG [BUG]

        gameWorld.setCurrentselectedSlot(gameUI.getInventoryHotBarSelectedSlot())
        gameWorld.update(window)
        gameUI.update(window)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEWHEEL:

                utils.scrollWheel = pygame.Vector2(event.x, event.y)

            # A simple fps toggle to check performance

        key = pygame.key.get_just_pressed()
        
        if(key[pygame.K_z] and utils.ActiveDebug):

            if(fps == 0):
                fps = 60
            else:
                fps = 0

        window.blit(fpsText, (utils.screenRect.width - 300, 100))

        pygame.display.flip()
        await asyncio.sleep(0)

    pygame.quit() 