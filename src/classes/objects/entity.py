from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import classes.objects.tiles as tiles

import pygame
import classes.utility.utils as utils

class Entity:
    def __init__(
            self,
            midbottom: pygame.Vector2 | tuple[float, float],
            hitbox_size: tuple[int, int],
            mass: float = 1,
            collide_tiles: bool = True
        ):
        self.mass = mass
        self.collide_tiles = collide_tiles

        self.hitbox = pygame.FRect((0, 0), hitbox_size)
        self.hitbox.midbottom = midbottom
        self.velocity = pygame.Vector2(0.0, 0.0)
        self.acceleration = pygame.Vector2(0.0, 0.0)
        self._force = pygame.Vector2(0.0, 0.0)
        self.moving = False
        self.collided = False
        self.collided_tile: tiles.Tile = None

    def apply_force(self, force: pygame.Vector2):
        self._force += force

    def solve_collision(self, collision_tiles: list[tiles.Tile]):
        self.collided = False
        self.collided_tile = None
        # x check
        x_movement: float = self.velocity.x * utils.deltaTime

        x_projected_rect: pygame.FRect = self.hitbox.copy()
        x_projected_rect.x += self.velocity.x * utils.deltaTime

        for tile in collision_tiles:
            hitbox = tile.getHitBox()
            if x_projected_rect.colliderect(hitbox):
                self.collided = True
                if self.collided_tile is None:
                    self.collided_tile = tile
                # positive dir
                if self.velocity.x > 0:
                    x_contact_distance: float = hitbox.left - self.hitbox.right
                    x_movement = min(x_movement, x_contact_distance, key=abs)

                elif self.velocity.x < 0:
                    x_contact_distance: float = hitbox.right - self.hitbox.left
                    x_movement = min(x_movement, x_contact_distance, key=abs)

                else:
                    print("stuck inside a tile, x")
                    pass


        # y check
        y_movement: float = self.velocity.y * utils.deltaTime

        y_projected_rect: pygame.FRect = self.hitbox.copy()
        y_projected_rect.y += self.velocity.y * utils.deltaTime

        for tile in collision_tiles:
            hitbox = tile.getHitBox()
            if y_projected_rect.colliderect(hitbox):
                self.collided = True
                if self.collided_tile is None:
                    self.collided_tile = tile
                # positive dir
                if self.velocity.y > 0:
                    y_contact_distance: float = hitbox.top - self.hitbox.bottom
                    y_movement = min(y_movement, y_contact_distance, key=abs)

                elif self.velocity.y < 0:
                    y_contact_distance: float = hitbox.bottom - self.hitbox.top
                    y_movement = min(y_movement, y_contact_distance, key=abs)

                else:
                    print("stuck inside a tile, y")
                    pass

        return x_movement, y_movement


    def update(self, collision_tiles: list[tiles.Tile]):
        self.velocity += self._force

        # This looks weird I know, but it's acctualy the right way to do it
        self.velocity += self.acceleration * 0.5 * utils.deltaTime
        if self.collide_tiles:
            x_movement, y_movement = self.solve_collision(collision_tiles)
            self.hitbox.x += x_movement
            self.hitbox.y += y_movement
            self.moving = round( x_movement) and round(y_movement)
        else:
            self.hitbox.midbottom += self.velocity * utils.deltaTime
            self.moving = round(self.velocity.x) and round(self.velocity.y)

        self.velocity += self.acceleration * 0.5 * utils.deltaTime
        self._force.x = 0
        self._force.y = 0