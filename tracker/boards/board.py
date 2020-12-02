from abc import ABC

from tkComponents import Component
from tkComponents.extensions import GridHelper

from .constants import Constants


class Board(Component, ABC):
    def __init__(self, parent, container):
        super().__init__(container, frame_style=Constants.FRAME_STYLE, extensions=[GridHelper])

        self.parent = parent

        self.state = self.parent.state
        self._register_paths()

    @property
    def display_name(self):
        raise NotImplementedError

    def _register_paths(self):
        """
        Any keys registered in subclasses should be prefixed with the class name
        in the format: "class__key_string"
        """
        pass

    def _apply_dividers(self, rows=(), columns=()):
        for row_index in rows:
            self._frame.grid_rowconfigure(row_index, minsize=Constants.DIVIDER_SIZE)
        for column_index in columns:
            self._frame.grid_columnconfigure(column_index, minsize=Constants.DIVIDER_SIZE)
