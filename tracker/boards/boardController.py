from tkinter import Label, Button
from functools import partial

from tracker.boards.board import Board, BoardConstants


class BoardController(Board):
    def __init__(self, parent, root_render_method):
        super().__init__(parent, root_render_method)

        self._full_view = True

    @property
    def display_name(self):
        return "Boards"

    @property
    def is_needs_render(self):
        return False

    def update(self):
        # The dropdown button cell should only stretch if the full board is not visible
        self._frame_stretch = {"columns": [0], "rows": []} if self._full_view else {"columns": [0], "rows": [0]}

    def render(self):
        self._refresh_frame(**BoardConstants.FRAME_STYLE)

        row_index = 0
        Button(self.frame, text=self.display_name,
               command=lambda: self._set_self_var("_full_view", lambda value: not value),
               font=BoardConstants.BASE_FONT
               ).grid(row=row_index, columnspan=3, ipadx=BoardConstants.IPADX_TINY, sticky="nswe")

        if self._full_view:
            other_boards = [board for board in self.parent.boards if type(board) != BoardController]

            self.frame.grid_columnconfigure(1, minsize=BoardConstants.DIVIDER_SIZE)

            row_index += 1
            for board_index, board in enumerate(other_boards):
                board_is_visible = board in self.parent.visible_boards

                Label(self.frame, text=board.display_name, font=BoardConstants.BASE_FONT
                      ).grid(row=row_index, ipadx=BoardConstants.IPADX_NORMAL)
                Button(self.frame, text="Hide" if board_is_visible else "View",
                       command=partial(self._toggle_board_visibility, board),
                       font=BoardConstants.BASE_FONT
                       ).grid(row=row_index, column=2, ipadx=BoardConstants.IPADX_SMALL, sticky="nswe")

                row_index += 1

        return self.frame

    def _toggle_board_visibility(self, board):
        if board in self.parent.visible_boards:
            self.parent.visible_boards.remove(board)
        else:
            self.parent.visible_boards.add(board)

        self._trigger_render()
