import pygame
from typing import TypedDict, Callable
from pathlib import Path
from json import dumps, loads

class AnimationData(TypedDict):
    frames: list[pygame.Surface]
    num_frames: int

class AnimationManager:
    def __init__(
            self,
            asset_path: str,
            num_of_animations: int,
            animations_num_frames: list[int],
            animations_names: list[str],
            scale = False
        ):
        """Extracts animations from a sprite sheet .png file and plays them

        :param asset_path: The path to the asset without "assets/" prefix.
        :param num_of_animations: The number of animations contained in this file.
        :param animations_num_frames: The number of frame for each animation from top to bottom.
        :param animations_names: The names of the animation from top to bottom, used to switch between them.
        """
        self.asset_name = Path(asset_path).stem
        self.asset_path = asset_path
        self.animations: dict[str, AnimationData] = {}
        self._current_frame_index: int = 0
        self._current_animation_name: str = ""
        self._timer: float = 0.0
        # in fps
        self._animation_speed: float = 5

        # I did some editing, added a scale property and used .convert_alpha for fast bilting,
        # Make sure when creating images you use .convert_alpha() to get more performance

        sprite_sheet = pygame.image.load(f"assets/{self.asset_path}").convert_alpha()

        if scale:
            sprite_sheet = pygame.transform.scale2x(sprite_sheet).convert_alpha()

        self.max_frames = max(animations_num_frames)
        self.frame_width: int = sprite_sheet.get_width() // self.max_frames
        self.frame_height: int = sprite_sheet.get_height() // num_of_animations

        for i in range(num_of_animations):
            frame_amount: int = animations_num_frames[i]
            animation_name: str = animations_names[i]

            row: pygame.Surface = pygame.Surface(
                (frame_amount * self.frame_width, self.frame_height),
                pygame.SRCALPHA
            )
            pygame.Rect()
            row_rect = pygame.Rect(
                0,
                i * self.frame_height,
                self.frame_width * frame_amount,
                self.frame_height
            )
            row.blit(sprite_sheet, area = row_rect)
            animation: AnimationData = {
                "frames" : self.split_animation(row, frame_amount),
                "num_frames" : frame_amount,
            }
            self.animations[animation_name] = animation


    @property
    def current_animation(self) -> AnimationData:
        if self._current_animation_name == "":
            raise(KeyError("No animation was set, you have to call set_animation(animation_name) to set the played animation"))
        return self.animations[self._current_animation_name]

    @property
    def current_frame(self) -> pygame.Surface:
        return self.current_animation["frames"][self._current_frame_index]

    @property
    def animation_speed(self):
        return self._animation_speed

    @animation_speed.setter
    def animation_speed(self, speed: float):
        if speed < 0:
            print("Warning you are trying to set the animation speed to a negative number")
            self._animation_speed = 0
        else:
            self._animation_speed = speed

    @property
    def animation_frame_delay(self):
        return 1 / self._animation_speed

    @animation_frame_delay.setter
    def animation_frame_delay(self, delay: float):
        self._animation_speed = 1 / delay

    def split_animation(self, animation_sheet : pygame.Surface, num_frames : int) -> list[pygame.Surface]:
        frames: list[pygame.Surface] = []
        for i in range(num_frames):
            frame = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)
            frame.blit(animation_sheet, (i * -self.frame_width, 0))
            frames.append(frame)

        return frames

    def set_animation(self, animation_name: str):
        if animation_name not in self.animations.keys():
            raise(KeyError(f"Animation name: {animation_name}, doesn't exist for {self.asset_name} asset."))
        elif self._current_animation_name != animation_name:
            self._current_animation_name = animation_name
            self._current_frame_index = 0
            self._timer = 0.0

    def update(self, delta_time: float):
        self._timer += delta_time

        last_index = self._current_frame_index
        self._current_frame_index = int(self._timer * self._animation_speed) % self.current_animation["num_frames"]

        if self._current_frame_index == 0 and last_index == self.current_animation["num_frames"] - 1:
            self._timer = (self._timer * self._animation_speed) % self.current_animation["num_frames"]







# if __name__ == "__main__":

#     screen = pygame.display.set_mode((1900, 1000))
#     pygame.init()

#     asset_name = "player"
#     num_of_animation = 2
#     frames_per_animation = [4, 4]
#     animations_names = ["idle", "walking"]
#     anim_test = AnimationManager(
#         asset_name,
#         num_of_animation,
#         frames_per_animation,
#         animations_names
#     )

#     print(anim_test.animations)
#     anim_test.set_animation("walking")

#     clock = pygame.Clock()
#     running = True
#     while running:
#         delta_time = clock.tick() / 1000
#         screen.fill("white")
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#                 break

#         anim_test.update(delta_time)
#         screen.blit(pygame.transform.scale_by(anim_test.current_frame, 10), (0, 0))
#         pygame.display.flip()


