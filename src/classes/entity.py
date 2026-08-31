import pygame

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
        self.acceleration = pygame.Vector2(0.0, 0.0)

    def apply_force(self, force: pygame.Vector2):
        self.acceleration += force

    def update(self, delta_time: float):
        # This looks weird I know, but it's acctualy the right way to do it
        self.velocity += self.acceleration * delta_time * 0.5
        self.hitbox.midbottom += self.velocity * delta_time
        self.velocity += self.acceleration * delta_time * 0.5

        self.acceleration = 0