from abc import ABC

from ..components import Component, GridHelper
from ..constants import Constants as TrackerConstants


class Board(Component.with_extensions(GridHelper), ABC):
    def __init__(self, parent, container, update_interval=None):
        super().__init__(container, update_interval=update_interval, styles={
            "frame": {
                "borderwidth": TrackerConstants.BORDERWIDTH__TINY,
                "relief": "sunken",
                "bg": TrackerConstants.DEFAULT_STYLE_ARGS["bg"],
                "padx": TrackerConstants.PAD__SMALL,
                "pady": TrackerConstants.PAD__SMALL
            }
        })

        self.parent = parent

        self.state = self.parent.state

    @property
    def display_name(self):
        raise NotImplementedError

    def _apply_dividers(self, rows=(), columns=()):
        for row_index in rows:
            self._frame.grid_rowconfigure(row_index, minsize=TrackerConstants.DIVIDER_SIZE)
        for column_index in columns:
            self._frame.grid_columnconfigure(column_index, minsize=TrackerConstants.DIVIDER_SIZE)
