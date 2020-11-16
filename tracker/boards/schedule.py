from tkinter import Frame, Label, Button
from functools import partial

from ..constants import Constants as TrackerConstants
from .board import WorkoutBoard


class Schedule(WorkoutBoard):
    def __init__(self, parent, root_render_method):
        super().__init__(parent, root_render_method)

        self._register_paths()

    @property
    def is_needs_render(self):
        pass

    def update(self):
        pass

    def render(self):
        if self.frame:
            self.frame.destroy()
        self.frame = Frame(self.parent.frame, borderwidth=TrackerConstants.SUNKEN_BORDER_WIDTH, relief="sunken")

        for column_index in ((i*4)+1 for i in range(len(TrackerConstants.WEEKDAY_KEY_STRINGS))):
            self.frame.grid_columnconfigure(column_index, minsize=TrackerConstants.DIVIDER_SIZE)

        # Header Row
        row_index = 0

        for weekday_index, weekday_string in enumerate(TrackerConstants.WEEKDAY_KEY_STRINGS):
            column_index = (weekday_index*4)+2
            Label(self.frame, text=weekday_string, font=TrackerConstants.BASE_FONT
                  ).grid(row=row_index, column=column_index, columnspan=3)

        workout_types = self.state.registered_get("workout_types")

        for workout_type_id in workout_types:
            # Variables and logic to filter displayed elements
            is_workout_disabled = self.state.registered_get("is_workout_disabled", [workout_type_id])
            if is_workout_disabled:
                continue  # Ignore workout types that have been disabled

            row_index += 1
            self.frame.grid_rowconfigure(row_index, minsize=TrackerConstants.DIVIDER_SIZE)

            workout_type_details = self.state.registered_get("workout_type_details", [workout_type_id])
            workout_name = workout_type_details["name"]

            row_index += 1
            Label(self.frame, text=workout_name, font=TrackerConstants.BASE_FONT
                  ).grid(row=row_index, column=0)

            for weekday_index, weekday_string in enumerate(TrackerConstants.WEEKDAY_KEY_STRINGS):
                workout_sets_scheduled = self.state.registered_get("scheduled_sets_single_entry",
                                                                   [weekday_string, workout_type_id])

                column_index = (weekday_index*4)+2
                Button(self.frame, text="-",
                       command=partial(self._increment_workout_sets_scheduled, workout_type_id, weekday_string, -1),
                       font=TrackerConstants.BASE_FONT
                       ).grid(row=row_index, column=column_index)

                column_index += 1
                Label(self.frame, text=workout_sets_scheduled, font=TrackerConstants.BASE_FONT
                      ).grid(row=row_index, column=column_index)

                column_index += 1
                Button(self.frame, text="+",
                       command=partial(self._increment_workout_sets_scheduled, workout_type_id, weekday_string, 1),
                       font=TrackerConstants.BASE_FONT
                       ).grid(row=row_index, column=column_index)

        return self.frame
