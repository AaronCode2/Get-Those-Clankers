from enum import Enum

# All the crafter stuff plus more

class itemsIndex(Enum):

    SCRAP_IGNOT = 0
    RINGED_TIN = 1
    SCREW = 2
    BOLT = 3
    RAW_IRON = 4
    SOFT_STEEL = 5
    SOLAR_PANEL = 6
    BARRIER = 7

# ItemGiven is how much is gotten from crafting that

class RecipeIndex(Enum):

    ItemNeeded = 0,
    ItemGiven = 1,
    ItemDescription = 2

recipes = {

    itemsIndex.SOLAR_PANEL: {

        RecipeIndex.ItemGiven: 1,

        RecipeIndex.ItemNeeded: (
            (
                (itemsIndex.SOFT_STEEL, 1),
                (itemsIndex.BOLT, 4)
            )
        ),

        RecipeIndex.ItemDescription: "Makes stuff!"
    },

    itemsIndex.BARRIER: {   

        RecipeIndex.ItemGiven: 5,

        RecipeIndex.ItemNeeded: (
            (
                (itemsIndex.RINGED_TIN, 1),
                (itemsIndex.BOLT, 4)
            )
        ),

        RecipeIndex.ItemDescription: "Makes stuff!"
    },

    itemsIndex.SOFT_STEEL: {

        RecipeIndex.ItemGiven: 4,

        RecipeIndex.ItemNeeded: (
            (
                (itemsIndex.RAW_IRON, 4),
            )
        ),

        RecipeIndex.ItemDescription: "Makes stuff!"
    },
}