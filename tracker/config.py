from .boards import Actuals, Schedule, BoardController


class Config:
    STATE_FILENAME = "data.json"
    ICON_FILENAME = "blank_icon.ico"

    BOARDS = set((Actuals, Schedule, BoardController))

    INITIAL_BOARDS_VISIBLE = set((BoardController,))
    BOARDS_COLUMNS = (
        (Actuals, Schedule),
        (BoardController,)
    )
