from tracker.boards import *
from tracker.boardHandlers import *


class Config:
    STATE_FILE_PATH = "data.json"
    ICON_FILE_PATH = r"res/icon.ico"

    BOARD_HANDLER = ResponsiveGrid

    # Board Handler Details
    INITIAL_BOARDS_VISIBLE = {BoardController}
    BOARDS_GRID_LAYOUT = {  # Row and column must be provided. rowspan and columnspan are defaulted to 1 if not provided
        BoardController: {"row": 0, "column": 0, "rowspan": 3},
        Actuals: {"row": 0, "column": 1, "rowspan": 2, "columnspan": 7},
        Schedule: {"row": 2, "column": 1, "rowspan": 2, "columnspan": 8},
        Tips: {"row": 4, "column": 1, "columnspan": 5},
        File: {"row": 0, "column": 8, "rowspan": 2, "columnspan": 3},
        ScheduleEditor: {"row": 2, "column": 9, "rowspan": 2, "columnspan": 5}
    }  # Note that boards can end up truncated if not given enough rows or columns
