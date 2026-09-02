import pygame
import classes.utility.utils as utils

class Entity:
    def __init__(
            self,
            midbottom: pygame.Vector2 | tuple[float, float],
            hitbox_size: tuple[int, int],
            mass: float = 1
        ):
        self.mass = mass

        self.hitbox = pygame.FRect((0, 0), hitbox_size)
        self.hitbox.midbottom = midbottom
        self.velocity = pygame.Vector2(0.0, 0.0)
        self._acceleration = pygame.Vector2(0.0, 0.0)

    def apply_force(self, force: pygame.Vector2):
        self._acceleration += force

    def update(self):
        # This looks weird I know, but it's acctualy the right way to do it
        self.velocity += self._acceleration * (utils.deltaTime * 0.5)
        self.hitbox.midbottom += self.velocity * utils.deltaTime
        self.velocity += self._acceleration * utils.deltaTime * 0.5

        self._acceleration.x = 0
        self._acceleration.y = 0