from managedState.extensions import KeyQueryFactory


class Constants:
    WEEKDAY_KEY_STRINGS = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")

    PATH_DYNAMIC_KEY = KeyQueryFactory(lambda sub_state, key: key)

    WINDOW_MINSIZE = (255, 33)
    WINDOW_TITLE = "Workout Logger"

    DATE_KEY_FORMAT = "%Y/%m/%d"

    TIP_PLACEHOLDER = "You have not added any tips."

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

    COLOURS = {
        "orange": "#FF9859",
        "yellow": "#FFD800",
        "blue": "#667FFF",
        "green": "#00B211",
        "grey": "#CCCCCC",
        "white": "#FFFFFF",
        "cool_off_white": "#FAFAFF",
        "cool_dark_grey": "#37373C",
        "warm_dark_grey": "#3C3B37",
        "warm_off_white": "#FFFEFA",
    }

    DEFAULT_STYLE_ARGS = {
        "fg": COLOURS["cool_off_white"],
        "bg": COLOURS["cool_dark_grey"]
    }

