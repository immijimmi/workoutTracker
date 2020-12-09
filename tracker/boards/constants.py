from ..constants import Constants as TrackerConstants


class Constants:
    # Padding
    PAD__TINY = 2
    PAD__SMALL = 4
    PAD__NORMAL = 6

    # Min Sizes
    DIVIDER_SIZE = 4
    WORKOUT_TYPES_SIZE = 180
    WORKOUT_SETS_ACTUALS_SIZE = 80

    # Border Sizes
    BORDERWIDTH__TINY = 1
    BORDERWIDTH__SMALL = 2

    # Fonts
    NORMAL_FONT = ("Bahnschrift", 10)
    BOLD_FONT = ("Bahnschrift", 10, "bold")
    SYMBOL_FONT = ("Bahnschrift", 9, "bold")
    SMALL_ITALICS_FONT = ("Bahnschrift", 9, "italic")

    # Misc
    FRAME_STYLE = {
        "borderwidth": BORDERWIDTH__TINY,
        "relief": "sunken",
        "bg": TrackerConstants.DEFAULT_STYLE_ARGS["bg"]
    }
