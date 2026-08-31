import pygame
import classes.utility.utils as utils

Slot = {

    utils.SlotIndex.AMOUNT: 0,
    utils.SlotIndex.TYPE: 0
}

class Inventory():

    def __init__(self):

        self.toggle = False

        # a 5x5 inventory! - 25slots

        self.slots = [

            # Main inventory
            [Slot] * 5,
            [Slot] * 5,
            [Slot] * 5,
            [Slot] * 5,

            # HotBar
            [Slot] * 5,
        ]

        print(self.slots)

    def update(self, window):

        self.draw(window)

    def drawHotBar(self, window):
        pass
        # for i in range(self.slots[4]):
            # 

    def draw(self, window):
        pass