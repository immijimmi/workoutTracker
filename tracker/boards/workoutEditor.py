from tkinter import StringVar

from ..constants import Constants as TrackerConstants
from tracker.boards.board import WorkoutBoard


class WorkoutEditor(WorkoutBoard):
    def __init__(self, parent, root_render_method):
        super().__init__(parent, root_render_method)

        self._workout_type = -1
        self._unsaved_changes = False

        self._name__var = StringVar()
        self._desc__var = StringVar()
        self._reps__var = StringVar()

    @property
    def display_name(self):
        return "Editor"

    @property
    def is_needs_render(self):
        return False

    def update(self):
        pass

    def render(self):
        self._refresh_frame(**TrackerConstants.BOARD_FRAME_STYLE)

        if not self._workout_type

        return self.frame
