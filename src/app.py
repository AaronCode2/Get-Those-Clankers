from game import *

async def init():

    pygame.display.set_caption("Get Those Clankers!")
    pygame.init()
    pygame.font.init()

    game = Game(1900, 1000, 60)
    await game.run()