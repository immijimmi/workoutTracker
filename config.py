from tracker.boards import BoardController, Actuals, Tips, Schedule, File


class Config:
    STATE_FILENAME = "data.json"
    ICON_FILENAME = r"res/icon.ico"

    INITIAL_BOARDS_VISIBLE = {BoardController, Tips}
    BOARDS_LAYOUT = {  # Row and column must be provided. Rowspan and columnspan are defaulted to 1 if not provided
        BoardController: {"row": 0, "column": 0, "rowspan": 2},
        Actuals: {"row": 0, "column": 1, "columnspan": 5},
        Schedule: {"row": 1, "column": 1, "columnspan": 6},
        Tips: {"row": 2, "column": 1, "columnspan": 5},
        File: {"row": 0, "column": 6}
    }
