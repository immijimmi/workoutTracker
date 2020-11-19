from tkinter import Label, Button
from functools import partial

from ..constants import Constants as TrackerConstants
from .board import Board


class BoardController(Board):
    def __init__(self, parent, root_render_method):
        super().__init__(parent, root_render_method)

        self._frame_stretch["columns"].append(1)
        self._frame_stretch["rows"].append(0)
        self._full_view = True

    @property
    def display_name(self):
        return "Boards"

    @property
    def is_needs_render(self):
        return False

    def update(self):
        # The dropdown button cell should only stretch if the full board is not visible
        self._frame_stretch = {"columns": [1], "rows": []} if self._full_view else {"columns": [0], "rows": [0]}

    def render(self):
        self._refresh_frame(**TrackerConstants.BOARD_FRAME_STYLE)

        Button(self.frame, text="^" if self._full_view else "v",
               command=lambda: self._set_self_var("_full_view", lambda value: not value), font=TrackerConstants.BASE_FONT
               ).grid(sticky="nswe")

        if self._full_view:
            other_boards = [board for board in self.parent.boards if type(board) != BoardController]

            # Header
            row_index = 0
            Label(self.frame, text=self.display_name, font=TrackerConstants.BASE_FONT
                  ).grid(row=row_index, column=1, columnspan=3)

            row_index += 1
            self.frame.grid_rowconfigure(row_index, minsize=TrackerConstants.DIVIDER_SIZE)
            self.frame.grid_columnconfigure(2, minsize=TrackerConstants.DIVIDER_SIZE)
            self.frame.grid_columnconfigure(1, minsize=100)

            row_index += 1
            for board_index, board in enumerate(other_boards):
                board_is_visible = board in self.parent.visible_boards

                Label(self.frame, text=board.display_name, font=TrackerConstants.BASE_FONT
                      ).grid(column=1, row=row_index)
                Button(self.frame, text="Hide" if board_is_visible else "View",
                       command=partial(self._toggle_board_visibility, board),
                       font=TrackerConstants.BASE_FONT
                       ).grid(row=row_index, column=3, sticky="nswe")

                row_index += 1

        return self.frame

    def _toggle_board_visibility(self, board):
        if board in self.parent.visible_boards:
            self.parent.visible_boards.remove(board)
        else:
            self.parent.visible_boards.add(board)

        self._trigger_render()
