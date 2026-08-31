import pygame
import utils
import enum

class imgIndex[Enum]:

    PLAYER_IMG = 0
    TILE_IMG = 1

# This is constant and should not be changed for storing texture data

images = {      

        # Tiles
        "Tiles": {
            "location": "assets/tiles/objects.png",
            "maxFramesX": 2,
            "FramesY": 1,
            "image": {

                "surface": None,
                "FrameWidth": None,
                "FrameHeight": None
            },

            "rotatedImages": {

                utils.RotationType.LEFT: None,
                utils.RotationType.UP: None,
                utils.RotationType.RIGHT: None
            }
        },

        "Battery": {

            "location": "assets/tiles/battery.png",
            "maxFramesX": 6,
            "FramesY": 1,
            "image": {

                "surface": None,
                "FrameWidth": None,
                "FrameHeight": None
            },

        },

        "keys": {

            "location": "assets/ui/keys.png",
            "maxFramesX": 3,
            "FramesY": 1,
            "image": {

                "surface": None,
                "FrameWidth": None,
                "FrameHeight": None
            },
        },

        "guiPlates": {

            "location": "assets/ui/guiPlates.png",
            "FramesX": 3,
            "FramesY": 3,
            "image": {

                "surface": None,
                "FrameWidth": None,
                "FrameHeight": None
            },
        },


}