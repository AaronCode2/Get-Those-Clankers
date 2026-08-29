import pygame
from typing import TypedDict
from json import dumps, loads


class AnimationData(TypedDict):
    frame_width: int
    frame_height: int
    frames: int
    name: str

class Animation:
    def __init__(self, asset_data_path: str, horizontal_fliped: bool = False):
        self.fliped = horizontal_fliped
        self.frames = []
        self.asset_data_path = asset_data_path
        self.animation_data = self.extract_data()

    def extract_data(self):
        with open(f"assets/{self.asset_data_path}", "r") as data_file:
            data_file.read()
            # WIP
