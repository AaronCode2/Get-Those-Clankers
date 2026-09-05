import pygame
import classes.utility.utils as utils
import classes.utility.textures as textures

droppedItems: list[DropItem] = []

class DropItem():

    def __init__(self, position: pygame.Vector2, type = utils.ItemType.NONE, amount = -1):

        self.position = position
        self.max_speed = 500
        self.magnet_force_scale = 80000000
        self.speed = pygame.Vector2(0.0, 0.0)
        self.magnet_range = 250

        if(amount == -1):
            self._type, self._amount = utils.generateItemForDropItem()
        else:
            self._type = type
            self._amount = amount

        self.srcRect = pygame.Rect(

            textures.images["Items"]["image"]["FrameWidth"] * self._type.value,
            0, 
            textures.images["Items"]["image"]["FrameWidth"],
            textures.images["Items"]["image"]["FrameHeight"]
        )

    def getItem(self):
        return self._type, self._amount

    def update(self, window, playerPos):
        distance = playerPos - self.position
        if distance.length() < self.magnet_range:
            pulling_strength = (1 / (distance.length_squared()) ) * self.magnet_force_scale

            self.speed += (distance).normalize() * pulling_strength * utils.deltaTime * 0.5
            self.speed.clamp_magnitude(self.max_speed)
            self.position += self.speed * utils.deltaTime
            self.speed += (distance).normalize() * pulling_strength * utils.deltaTime * 0.5
            self.speed.clamp_magnitude(self.max_speed)
        else:
            self.speed = pygame.Vector2(0.0, 0.0)
        return self.draw(window)

    def draw(self, window):

        return textures.images["Items"]["image"]["surface"], self.position, self.srcRect, self.position.y + (self.srcRect.height / 2)