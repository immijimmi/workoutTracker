from .boards import Actuals, Schedule


class Config:
    STATE_FILENAME = "data.json"
    ICON_FILENAME = "blank_icon.ico"

    BOARDS = {
        (0, 0): Actuals,
        (0, 1): Schedule
    }
