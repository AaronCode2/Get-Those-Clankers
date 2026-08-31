import pygame
from entity import Entity
from classes.animation import AnimationManager


class AnimatedEntity(Entity):
    def __init__(self, position: pygame.Vector2, animation_manager: AnimationManager, hitbox_size : tuple[int, int]):
        self.animation = animation_manager
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

    def update(self, delta_time: float):
        self.animation.update(delta_time)
        super().update(delta_time)

    def draw(self, screen: pygame.Surface):
        screen.blit(self.surface, self.rect)
