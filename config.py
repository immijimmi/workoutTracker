from tracker.boards import BoardController, Actuals, Tips, Schedule, File


class Config:
    STATE_FILENAME = "data.json"
    ICON_FILENAME = r"res/icon.ico"

    """
    BOARDS = {BoardController, Actuals, Schedule, Tips}

    INITIAL_BOARDS_VISIBLE = {BoardController, Tips}
    BOARDS_COLUMNS = (
        (BoardController,),
        (Actuals, Schedule, Tips)
    )
    """

    BOARDS = {BoardController, Actuals, Tips, Schedule, File}

    INITIAL_BOARDS_VISIBLE = {BoardController, Tips}
    BOARDS_COLUMNS = (
        (BoardController, File),
        (Actuals, Schedule, Tips)
    )
