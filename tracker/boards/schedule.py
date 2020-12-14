from tkComponents.basicComponents import ButtonListBox

from tkinter import PhotoImage

from ..constants import Constants as TrackerConstants
from .board import Board


class Schedule(Board):
    def __init__(self, parent, container):
        super().__init__(parent, container)

    @property
    def display_name(self):
        return "Schedule"

    @property
    def height(self):
        self._frame.update()
        return self._frame.winfo_height()-(2*self._frame["borderwidth"])

    def _render(self):
        def on_change__schedule_picker(_schedule_picker, new_value):
            if new_value is None:
                self.state.registered_set(None, "active_schedule_id")

            else:
                schedules = self.state.registered_get("workout_schedules")
                if new_value not in schedules:
                    raise ValueError

                self.state.registered_set(new_value, "active_schedule_id")

            self.render()

        def get_data__schedule_picker(_schedule_picker):
            result = [{"value": None, "text": "None", "style": {"font": TrackerConstants.BOLD_FONT}}]

            schedules = self.state.registered_get("workout_schedules")
            for schedule_id in schedules:
                result.append({"value": schedule_id, "text": schedules[schedule_id]["name"]})

            return result

        schedule_picker = ButtonListBox(
            self._frame,
            self.state.registered_get("active_schedule_id"),
            lambda: self.height,
            get_data=get_data__schedule_picker,
            on_change=on_change__schedule_picker,
            styles={
                "button": {
                    "font": TrackerConstants.NORMAL_FONT,
                    "fg": TrackerConstants.DEFAULT_STYLE_ARGS["fg"],
                    "bg": TrackerConstants.DEFAULT_STYLE_ARGS["bg"],
                    "pady": TrackerConstants.PAD__TINY,
                    "relief": "raised"
                },
                "button_selected": {
                    "bg": TrackerConstants.COLOURS["scrollbar_trough_grey"],
                    "relief": "sunken"
                },
                "scrollbar": {
                    "width": 14  # <14 Will not look symmetrical
                }
            }
        )
        schedule_picker.render().grid(row=0, column=0, sticky="nswe")

        """
        self._refresh_frame(**TrackerConstants.BOARD_FRAME_STYLE)

        for column_index in ((i*4)+1 for i in range(len(TrackerConstants.WEEKDAY_KEY_STRINGS))):
            self.frame.grid_columnconfigure(column_index, minsize=TrackerConstants.DIVIDER_SIZE)

        # Header Row
        row_index = 0

        for weekday_index, weekday_string in enumerate(TrackerConstants.WEEKDAY_KEY_STRINGS):
            column_index = (weekday_index*4)+2
            Label(self.frame, text=weekday_string, font=TrackerConstants.NORMAL_FONT
                  ).grid(row=row_index, column=column_index, columnspan=3, ipadx=TrackerConstants.IPADX_SMALL)

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
            Label(self.frame, text=workout_name, font=TrackerConstants.NORMAL_FONT
                  ).grid(row=row_index, ipadx=TrackerConstants.IPADX_NORMAL)

            for weekday_index, weekday_string in enumerate(TrackerConstants.WEEKDAY_KEY_STRINGS):
                workout_sets_scheduled = self.state.registered_get("scheduled_sets_single_entry",
                                                                   [weekday_string, workout_type_id])

                column_index = (weekday_index*4)+2
                Button(self.frame, text="-",
                       command=partial(self._increment_workout_sets_scheduled, workout_type_id, weekday_string, -1),
                       font=TrackerConstants.NORMAL_FONT, state="disabled" if workout_sets_scheduled == 0 else "normal"
                       ).grid(row=row_index, column=column_index, ipadx=TrackerConstants.IPADX_TINY, sticky="nswe")

                column_index += 1
                Label(self.frame, text=workout_sets_scheduled, font=TrackerConstants.NORMAL_FONT
                      ).grid(row=row_index, column=column_index, ipadx=TrackerConstants.IPADX_SMALL)

                column_index += 1
                Button(self.frame, text="+",
                       command=partial(self._increment_workout_sets_scheduled, workout_type_id, weekday_string, 1),
                       font=TrackerConstants.NORMAL_FONT
                       ).grid(row=row_index, column=column_index, ipadx=TrackerConstants.IPADX_TINY, sticky="nswe")

        return self.frame
        """
