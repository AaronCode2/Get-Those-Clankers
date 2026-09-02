import pygame
import classes.utility.utils as utils
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
            "FramesX": 4,
            "FramesY": 8,
            "image": {

                "surface": None,
                "FrameWidth": None,
                "FrameHeight": None
            },
        },

        "batteryIndicator": {

            "location": "ui/battery_indicator.png",
            "FramesX": 2,
            "FramesY": 6,

            "animationNames": [
                "BATTERY_FULL", "BATTERY_DRAIN_1", 
                "BATTERY_DRAIN_2", "BATTERY_DRAIN_3",
                "BATTERY_DRAIN_4", "BATTERY_EMPTY"
            ]
        },

        "Items": {

            "location": "assets/ui/items.png",
            "FramesX": 8,
            "FramesY": 1,
            "image": {

                "surface": None,
                "FrameWidth": None,
                "FrameHeight": None
            },
        }
}