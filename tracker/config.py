from .boards import Actuals, Schedule


class Config:
    STATE_FILENAME = "data.json"
    ICON_FILENAME = "blank_icon.ico"

    BOARDS = set((Actuals, Schedule))

    BOARDS_COLUMNS = (
        (Actuals, Schedule),
    )
