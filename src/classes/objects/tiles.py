import pygame
from pygame.examples.go_over_there import target_position

import classes.utility.utils as utils
import classes.utility.textures as textures
import classes.manager.camera as camera
import classes.bots.bot as bot
import classes.objects.bullet as bullet
import math

class Tile:

    def __init__(self, position: pygame.Vector2, type: utils.TileType, rotation: utils.RotationType):

        self.Imageposition = position
        self.position = position
        self.type = type
        self.rotation = rotation

        if(type != utils.TileType.GREEN_TOWER):

            self.width = textures.images["Tiles"]["image"]["FrameWidth"]
            self.height = textures.images["Tiles"]["image"]["FrameHeight"]
        else:
            self.bullets: list[bullet.Bullet] = []
            self.range = 500
            self.projectile_speed = 200
            self.reload_time = 1
            self.cooldown_timer = 0.0
            self.rotation = utils.RotationType.UP
            self.width = textures.images["Tower"]["image"]["FrameWidth"]
            self.height = textures.images["Tower"]["image"]["FrameHeight"]

        self._destRect = pygame.Rect(

            self.Imageposition.x + utils.hitBoxAdjForTiles[self.type][self.rotation].x,
            self.Imageposition.y + utils.hitBoxAdjForTiles[self.type][self.rotation].y,
            self.width + utils.hitBoxAdjForTiles[self.type][self.rotation].width,
            self.height + utils.hitBoxAdjForTiles[self.type][self.rotation].height
        )

        self._hitBox = pygame.Rect(

            self.position.x + utils.hitBoxAdjForTiles[self.type][self.rotation].x, 
            self.position.y + utils.hitBoxAdjForTiles[self.type][self.rotation].y, 
            self.width + utils.hitBoxAdjForTiles[self.type][self.rotation].width, 
            self.height + utils.hitBoxAdjForTiles[self.type][self.rotation].height
        )

        self.durability = utils.durabiltyForTile[type]

        self.setSrcRect()

    def getHitBox(self):
        return self._hitBox

    def updateHitBox(self, offset: pygame.Vector2):

        self._hitBox = pygame.Rect(

            self.position.x + utils.hitBoxAdjForTiles[self.type][self.rotation].x - offset.x,
            self.position.y + utils.hitBoxAdjForTiles[self.type][self.rotation].y - offset.y,
            self.width + utils.hitBoxAdjForTiles[self.type][self.rotation].width,
            self.height + utils.hitBoxAdjForTiles[self.type][self.rotation].height
        )

        # print(self._hitBox)

    def update(self, window, offset):

        camera_items = [
            self.draw(window),
            utils.getDebugRectItem(window, self._destRect)
        ]

        self.updateHitBox(offset)

        if self.type == utils.TileType.GREEN_TOWER:
            removed_indexs = []
            for flying_bullet in self.bullets:
                camera_items.append(flying_bullet.update(window))
                if flying_bullet.destroyBullet:
                    removed_indexs.append(flying_bullet)

            for flying_bullet in removed_indexs:
                self.bullets.remove(flying_bullet)
        return camera_items

    # This func only called if the object is a tower!

    def towerFunc(self, bots):
        bullet.Bullet.giveBots(bots)

        self.cooldown_timer += utils.deltaTime
        if self.cooldown_timer < self.reload_time:
            return
        tower_top = pygame.Vector2(self.Imageposition.y, self.Imageposition.y + (self._destRect.height / 2))

        if len(bots) == 0:
            return

        closest_bot: bot.Bot = min(bots, key=lambda bot: (tower_top - bot.rect.center).length())
        distance = closest_bot.rect.center - tower_top
        if distance.length() <= self.range:
            if closest_bot.moving:
                target_meet_position = utils.calculateMeetPosition(closest_bot, distance, self.projectile_speed)
            else:
                target_meet_position = closest_bot.rect.center
            direction = (target_meet_position - self.Imageposition).normalize()
            velocity = direction * self.projectile_speed
            self.bullets.append(bullet.Bullet(tower_top, velocity))
            self.cooldown_timer = 0






    # It's an array of bots, 
    # Bots have bot.health
    # You manually destroy the bots e.g if(bot.health == 0): bots.remove(bot)
    # There is no bullet class, you have to create one

    def draw(self, window) -> camera.CameraItem:
        item: camera.CameraItem
        if(self.type != utils.TileType.GREEN_TOWER):

            if(self.rotation == utils.RotationType.DOWN):
                item = (textures.images["Tiles"]["image"]["surface"], self.Imageposition, self.srcRect, self._destRect.centery)
            else:
                item = (textures.images["Tiles"]["rotatedImages"][self.rotation], self.Imageposition, self.srcRect, self._destRect.centery)

        else:

            # Draw Tower!
            
            item = (textures.images["Tower"]["image"]["Animation"].current_frame, self.Imageposition, None, self._destRect.centery)
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