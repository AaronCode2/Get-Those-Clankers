import pygame
from classes.utility.animation import AnimationManager
from classes.objects.animatedEntity import AnimatedEntity
import classes.utility.utils as utils

class Player(AnimatedEntity):
    def __init__(self, position: pygame.Vector2):
        animation = AnimationManager(
            "player/player.png",
            2,
            [4, 4],
            ["idle", "walk"],
            2
        )
        self.movement_speed = 200
        super().__init__(position, animation, (20, 15))

    def update(self):
        keys = pygame.key.get_pressed()

        movement_direction = pygame.Vector2(0, 0)
        if keys[pygame.K_w]:
            movement_direction.y -= 1
        if keys[pygame.K_s]:
            movement_direction.y += 1
        if keys[pygame.K_a]:
            movement_direction.x -= 1
        if keys[pygame.K_d]:
            movement_direction.x += 1


        if movement_direction.length() != 0:
            movement_direction.normalize_ip()
            self.set_animation("walk")
            self.animation.animation_speed = 5
        else:
            self.set_animation("idle")
            self.animation.animation_speed = 1

        if movement_direction.x < 0:
            self.animation.flipped = True
        elif movement_direction.x > 0:
            self.animation.flipped = False


        self.velocity = movement_direction * self.movement_speed
        super().update()

