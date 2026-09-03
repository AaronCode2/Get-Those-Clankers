from enum import Enum
import classes.utility.utils as utils

# All the crafter stuff plus more
# ItemGiven is how much is gotten from crafting that

class RecipeCrafts(Enum):

    CRAFT_SOLAR_PANEL = 0
    CRAFT_BARRIER = 1
    CRAFT_SOFT_STEEL = 2

class RecipeIndex(Enum):

    ItemNeeded = 0,
    ItemGiven = 1,
    ItemDescription = 2

recipes = {

    RecipeCrafts.CRAFT_SOLAR_PANEL: {

        RecipeIndex.ItemGiven: 1,

        RecipeIndex.ItemNeeded: (

            (utils.ItemType.SOFT_STEEL, 1),
            (utils.ItemType.BOLT, 4)
        ),

        RecipeIndex.ItemDescription: "Makes stuff!"
    },

    RecipeCrafts.CRAFT_BARRIER: {   

        RecipeIndex.ItemGiven: 5,

        RecipeIndex.ItemNeeded: (

            (utils.ItemType.RINGED_TIN, 1),
            (utils.ItemType.BOLT, 4)
        ),

        RecipeIndex.ItemDescription: "Makes stuff!"
    },

    RecipeCrafts.CRAFT_SOFT_STEEL: {

        RecipeIndex.ItemGiven: 4,

        RecipeIndex.ItemNeeded:(

            (utils.ItemType.RAW_IRON, 4),
        ),

        RecipeIndex.ItemDescription: "Makes stuff!"
    },
}