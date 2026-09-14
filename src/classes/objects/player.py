import pygame
from src.classes.utility.animation import AnimationManager
from src.classes.objects.animatedEntity import AnimatedEntity
import src.classes.objects.tiles as tiles
import src.classes.objects.bullet as bullet
import src.classes.utility.utils as utils


class Player(AnimatedEntity):
    def __init__(self, position: pygame.Vector2):
        animation = AnimationManager(
            asset_path = "player/player.png",
            num_of_animations = 3,
            animations_num_frames = [4, 4, 4],
            animations_names = ["idle", "walk", "hit"],
            scale_factor = 2
        )
        self.movement_speed = 200
        super().__init__(position, animation, (54, 24))

        self.bullets: list[bullet.Bullet] = []
        self.projectile_speed = 500
        self.reload_time = 0.5
        self.reload_timer = 0.0

    def update(self, collision_tiles: list[tiles.Tile]):
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

        super().update(collision_tiles)


    def draw(self, window: pygame.Surface, debug: bool = False):
        returned = super().draw(window, debug)
        returned += self.handle_bullet(window)
        return returned



    def handle_bullet(self, window):
        self.reload_timer += utils.deltaTime
        if self.reload_timer >= self.reload_time:

            mouse_buttons = pygame.mouse.get_pressed()
            key_buttons = pygame.key.get_pressed()

            if mouse_buttons[1] or key_buttons[pygame.K_SPACE] or key_buttons[pygame.K_KP_ENTER]:
                self.shoot_bullet()

        returned = []
        for projectile in self.bullets:
            returned.append(projectile.update(window))

        removed_index = []
        for projectile in self.bullets:
            if projectile.destroyBullet:
                removed_index.append(projectile)

        for bullet_index in removed_index:
            self.bullets.remove(bullet_index)

        return returned


    def shoot_bullet(self):
        self.reload_timer = 0

        direction = (-(self.position - utils.cameraOffset) + pygame.mouse.get_pos()).normalize()
        self.bullets.append(bullet.Bullet(self.rect.center, direction * self.projectile_speed))