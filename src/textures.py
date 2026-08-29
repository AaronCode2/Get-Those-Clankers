import pygame
import enum

class imgIndex[Enum]:

    PLAYER_IMG = 0
    TILE_IMG = 1

# This is constant and should not be changed for storing texture data

images = {

    [
        # Player
        {

            "location": "assets/player/player.png",
            "maxFramesX": 4, # some frames may have less than 4 frames
            "FramesY": 2,
            "image": {

                "surface": None,
                "FrameWidth": None,
                "FrameHeight": None
            }
        },

        # Tiles
        {
            "location": "assets/tiles/tile.png",
            "maxFramesX": 8,
            "FramesY": 1,

            "image": {

                "surface": None,
                "FrameWidth": None,
                "FrameHeight": None
            }
        }
    ]
}