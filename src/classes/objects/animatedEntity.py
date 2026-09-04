import pygame
from classes.objects.entity import Entity
from classes.utility.animation import AnimationManager
import classes.objects.tiles as tiles
import classes.utility.utils as utils


class AnimatedEntity(Entity):
    def __init__(self, position: pygame.Vector2, animation_manager: AnimationManager, hitbox_size : tuple[int, int], starting_animation: str = "idle"):
        self.animation = animation_manager
        self.animation.set_animation(starting_animation)
        self._rect = self.animation.current_frame.get_rect(topleft=position)

        super().__init__(self._rect.midbottom, hitbox_size)

    @property
    def rect(self):
        self._rect.midbottom = self.hitbox.midbottom
        return self._rect

    @property
    def position(self):
        return self.rect.topleft

    @position.setter
    def position(self, new_position: pygame.Vector2):
        self._rect.topleft = new_position
        self.hitbox.midbottom = self._rect.midbottom

    @property
    def surface(self):
        return self.animation.current_frame

    def set_animation(self, animation_name: str):
        self.animation.set_animation(animation_name)

    def update(self, collision_tiles: list[tiles.Tile]):
        self.animation.update()
        super().update(collision_tiles)

    def draw(self, screen: pygame.Surface, debug: bool = False):
        screen.blit(self.surface, self.rect)
        if debug:
            utils.debugDraw(screen, self.hitbox)
