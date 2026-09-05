import pygame
import classes.utility.utils as utils
import classes.utility.textures as textures
import classes.manager.camera as camera

class Tile:

    def __init__(self, position: pygame.Vector2, type: utils.TileType, rotation: utils.RotationType):

        self.position = position
        self.type = type
        self.rotation = rotation

        if(type != utils.TileType.GREEN_TOWER):

            self.width = textures.images["Tiles"]["image"]["FrameWidth"]
            self.height = textures.images["Tiles"]["image"]["FrameHeight"]
        else:

            self.rotation = utils.RotationType.UP
            self.width = textures.images["Tower"]["image"]["FrameWidth"]
            self.height = textures.images["Tower"]["image"]["FrameHeight"]

        self._hitBox = pygame.Rect(

            self.position.x + utils.hitBoxAdjForTiles[self.type][self.rotation].x, 
            self.position.y + utils.hitBoxAdjForTiles[self.type][self.rotation].y, 
            self.width + utils.hitBoxAdjForTiles[self.type][self.rotation].width, 
            self.height + utils.hitBoxAdjForTiles[self.type][self.rotation].height
        )


        self.durability = utils.durabiltyForTile[type]

        print(type)

        self.setSrcRect()

    def getHitBox(self):
        return self._hitBox

    def update(self, window) -> list[camera.CameraItem]:

        camera_items = [
            self.draw(window),
            utils.getDebugRectItem(window, self._hitBox)
        ]

        return camera_items

    # This func only called if the object is a tower!

    def towerFunc(self, bots):
        pass

    # It's an array of bots, 
    # Bots have bot.health
    # You manually destroy the bots e.g if(bot.health == 0): bots.remove(bot)
    # There is no bullet class, you have to create one

    def draw(self, window) -> camera.CameraItem:
        item: camera.CameraItem
        if(self.type != utils.TileType.GREEN_TOWER):

            if(self.rotation == utils.RotationType.DOWN):
                item = (textures.images["Tiles"]["image"]["surface"], self.position, self.srcRect, self._hitBox.centery)
            else:
                item = (textures.images["Tiles"]["rotatedImages"][self.rotation], self.position, self.srcRect, self._hitBox.centery)

        else:

            # Draw Tower!
            
            item = (textures.images["Tower"]["image"]["Animation"].current_frame, self.position, None, self._hitBox.centery)
        return item

    def setSrcRect(self):

        # Takes care of rotated image and gets that single frame it needs
        # Towers Should not be rotated

        if(self.type == utils.TileType.GREEN_TOWER):
            return

        match(self.rotation):

            case utils.RotationType.DOWN:

                self.srcRect = pygame.Rect(
                    self.width * float(self.type.value), 
                    0,
                    self.width, self.height
                )

            case utils.RotationType.LEFT:

                self.srcRect = pygame.Rect(
                    0, 
                    self.height * ((textures.images["Tiles"]["maxFramesX"] - 1) - float(self.type.value)),
                    self.width, self.height
                )

            case utils.RotationType.UP:

                # Since we flipped it, we have to count backwards to get our frames
                
                self.srcRect = pygame.Rect(
                    self.width * ((textures.images["Tiles"]["maxFramesX"] - 1) - float(self.type.value)),
                    0, 
                    self.width, self.height
                )

            case utils.RotationType.RIGHT:

                self.srcRect = pygame.Rect(
                    0, 
                    self.width * float(self.type.value),
                    self.width, self.height
                )