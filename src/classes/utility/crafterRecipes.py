from enum import Enum
import classes.utility.utils as utils

# All the crafter stuff plus more
# ItemGiven is how much is gotten from crafting that

class RecipeCrafts(Enum):

    CRAFT_SOLAR_PANEL = 0
    CRAFT_BARRIER = 1
    CRAFT_SOFT_STEEL = 2
    CRAFT_BOLT = 3
    CRAFT_SCREW = 4
    CRAFT_SCRAP_INGOT = 5

class RecipeIndex(Enum):

    ItemNeeded = 0,
    ItemTypeGiven = 1
    ItemGiven = 2,
    ItemDescription = 3

# 17 chars per \n @RecipeIndex.ItemDescription

recipes = {

    RecipeCrafts.CRAFT_SOLAR_PANEL: {

        RecipeIndex.ItemGiven: 1,
        RecipeIndex.ItemTypeGiven: utils.ItemType.SOLAR_PANEL,

        RecipeIndex.ItemNeeded: (

            (utils.ItemType.SOFT_STEEL, 1),
            (utils.ItemType.BOLT, 4)
        ),


        RecipeIndex.ItemDescription: "Use to power the\nbatteries and is\nslow,can be placed\non the ground"
    },

    RecipeCrafts.CRAFT_BARRIER: {   

        RecipeIndex.ItemGiven: 5,
        RecipeIndex.ItemTypeGiven: utils.ItemType.BARRIER,

        RecipeIndex.ItemNeeded: (

            (utils.ItemType.RINGED_TIN, 1),
            (utils.ItemType.BOLT, 4)
        ),

        RecipeIndex.ItemDescription: "Make defenses and\nplace them on the\nground"
    },

    RecipeCrafts.CRAFT_SOFT_STEEL: {

        RecipeIndex.ItemGiven: 4,
        RecipeIndex.ItemTypeGiven: utils.ItemType.SOFT_STEEL,

        RecipeIndex.ItemNeeded:(

            (utils.ItemType.RAW_IRON, 4),
        ),

        RecipeIndex.ItemDescription: "Very useful for\ncrafting"
    },

    RecipeCrafts.CRAFT_BOLT: {

        RecipeIndex.ItemGiven: 4,
        RecipeIndex.ItemTypeGiven: utils.ItemType.BOLT,

        RecipeIndex.ItemNeeded:(

            (utils.ItemType.RAW_IRON, 1),
        ),

        RecipeIndex.ItemDescription: "Gives us utils and\ncore ingredient\nfor upgrading"
    },

    RecipeCrafts.CRAFT_SCREW: {

        RecipeIndex.ItemGiven: 4,
        RecipeIndex.ItemTypeGiven: utils.ItemType.SCREW,

        RecipeIndex.ItemNeeded:(

            (utils.ItemType.RAW_IRON, 1),
        ),

        RecipeIndex.ItemDescription: "Can be great to\nhave around"
    },

    RecipeCrafts.CRAFT_SCRAP_INGOT: {

        RecipeIndex.ItemGiven: 1,
        RecipeIndex.ItemTypeGiven: utils.ItemType.SCRAP_IGNOT,

        RecipeIndex.ItemNeeded:(

            (utils.ItemType.RAW_IRON, 1),
        ),

        RecipeIndex.ItemDescription: "Better Iron and\ncheaper steel"
    },
}