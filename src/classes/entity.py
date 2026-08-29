import pygame

class Entity:
    def __init__(self, surface: pygame.Surface, position: pygame.Vector2, mass: float = 1):
        self.mass = mass

        self.surface = surface
        self.position = position
        self.rect: pygame.Rect = self.surface.get_rect(topleft = self.position)
        self.velocity = pygame.Vector2(0.0, 0.0)
        self.acceleration = pygame.Vector2(0.0, 0.0)

    def apply_force(self, force: pygame.Vector2):
        self.acceleration += force

    def update(self, delta_time: float):
        # This looks weird I know but it's acctualy the right way to do it
        self.velocity += self.acceleration * delta_time * 0.5
        self.position += self.velocity * delta_time
        self.velocity += self.acceleration * delta_time * 0.5