from tracker.boards import Actuals, BoardController


class Config:
    STATE_FILENAME = "data.json"
    ICON_FILENAME = "icon.ico"

    """
    BOARDS = {BoardController, Actuals, Schedule, Tips}

    INITIAL_BOARDS_VISIBLE = {BoardController, Tips}
    BOARDS_COLUMNS = (
        (BoardController,),
        (Actuals, Schedule, Tips)
    )
    """

    BOARDS = {BoardController, Actuals}

    INITIAL_BOARDS_VISIBLE = {BoardController}
    BOARDS_COLUMNS = (
        (BoardController,),
        (Actuals,)
    )
