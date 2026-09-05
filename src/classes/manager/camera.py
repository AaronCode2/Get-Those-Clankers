import pygame

# (surface, dest, area, hitbox_center_y)
CameraItem = tuple[pygame.Surface, tuple[float] | pygame.Vector2, pygame.Rect | None, float]

class Camera:
    def __init__(self):
        self.offset = pygame.Vector2(0.0, 0.0)

    def draw(self, items: list[CameraItem], focused_position: pygame.Vector2, window: pygame.Surface):
        print(focused_position)
        self.offset.x = focused_position[0] - (window.size[0] / 2)
        self.offset.y = focused_position[1] - (window.size[1] / 2)

        ordered_items: list[CameraItem] = sorted(items, key = lambda item : item[3])

        for (surface, dest, area, _)  in ordered_items:
            window.blit(surface, -self.offset + dest, area)