from ..components import ButtonListBox, NumberStepperTable
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

        frame_padding = self.styles["frame"].get("padx", 0)
        frame_borderwidth = self.styles["frame"].get("borderwidth", 0)

        total_height_buffer = (2 * frame_padding) + (2 * frame_borderwidth)

        return self._frame.winfo_height() - total_height_buffer

    def _render(self):
        def on_change__schedule_picker(_schedule_picker, new_value):
            if new_value is None:
                self.state.registered_set(None, "active_schedule_id")

            else:
                schedules = self.state.registered_get("workout_schedules")
                if new_value not in schedules:
                    raise ValueError

                self.state.registered_set(new_value, "active_schedule_id")

            self.parent.render()

        def get_data__schedule_picker(_schedule_picker):
            result = [{"value": None, "text": "None", "style": {"font": TrackerConstants.BOLD_FONT}}]

            schedules = self.state.registered_get("workout_schedules")
            for schedule_id in schedules:
                result.append({"value": schedule_id, "text": schedules[schedule_id]["name"]})

            return result

        def on_change__stepper_table(x_value, y_value, _stepper_table, increment_value):
            active_schedule_id = self.state.registered_get("active_schedule_id")

            if active_schedule_id is None:
                return

            self.state.registered_set(
                _stepper_table.value, "scheduled_sets_single_entry", [active_schedule_id, x_value, y_value])

        def get_data__stepper_table(x_value, y_value, _stepper_table):
            active_schedule_id = self.state.registered_get("active_schedule_id")

            if active_schedule_id is None:
                _stepper_table.min = 0
                _stepper_table.max = 0

                return 0

            else:
                return self.state.registered_get("scheduled_sets_single_entry", [active_schedule_id, x_value, y_value])

        schedule_picker = ButtonListBox(
            self._frame,
            self.state.registered_get("active_schedule_id"),
            lambda: self.height,
            get_data=get_data__schedule_picker,
            on_change=on_change__schedule_picker,
            styles={
                "canvas": {
                    "bg": TrackerConstants.DEFAULT_STYLE_ARGS["bg"]
                },
                "button": {
                    "font": TrackerConstants.NORMAL_FONT,
                    "fg": TrackerConstants.DEFAULT_STYLE_ARGS["fg"],
                    "bg": TrackerConstants.DEFAULT_STYLE_ARGS["bg"],
                    "padx": TrackerConstants.PAD__SMALL,
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

        workout_types = self.state.registered_get("workout_types")
        workout_y_values = workout_types.keys()
        workout_y_labels = [workout_types[workout_type_id]["name"] for workout_type_id in workout_y_values]

        stepper_table = NumberStepperTable(
            self._frame,
            [TrackerConstants.WEEKDAY_KEY_STRINGS, workout_y_labels],
            [TrackerConstants.WEEKDAY_KEY_STRINGS, workout_y_values],
            get_data=get_data__stepper_table,
            on_change=on_change__stepper_table,
            limits=(0, None),
            styles={
                "frame": {
                    "bg": TrackerConstants.DEFAULT_STYLE_ARGS["bg"]
                },
                "x_label": {
                    "font": TrackerConstants.NORMAL_FONT,
                    "bg": TrackerConstants.DEFAULT_STYLE_ARGS["bg"],
                    "fg": TrackerConstants.DEFAULT_STYLE_ARGS["fg"],
                    "relief": "ridge",
                    "borderwidth": TrackerConstants.BORDERWIDTH__SMALL,
                    "width": 3,
                    "padx": TrackerConstants.PAD__SMALL,
                    "pady": TrackerConstants.PAD__SMALL
                },
                "y_label": {
                    "font": TrackerConstants.NORMAL_FONT,
                    "bg": TrackerConstants.DEFAULT_STYLE_ARGS["bg"],
                    "fg": TrackerConstants.DEFAULT_STYLE_ARGS["fg"],
                    "width": max([len(label) for label in workout_y_labels]),
                    "padx": TrackerConstants.PAD__SMALL
                },
                "number_stepper": {
                    "label": {
                        "font": TrackerConstants.NORMAL_FONT,
                        "bg": TrackerConstants.DEFAULT_STYLE_ARGS["bg"],
                        "fg": TrackerConstants.DEFAULT_STYLE_ARGS["fg"],
                        "relief": "ridge",
                        "borderwidth": TrackerConstants.BORDERWIDTH__TINY,
                        "width": 3,
                        "padx": TrackerConstants.PAD__TINY
                    },
                    "button": {
                        "font": TrackerConstants.SYMBOL_FONT,
                        "bg": TrackerConstants.DEFAULT_STYLE_ARGS["bg"],
                        "fg": TrackerConstants.DEFAULT_STYLE_ARGS["fg"],
                        "width": 1,
                        "padx": TrackerConstants.PAD__TINY
                    }
                }
            }
        )
        stepper_table.render().grid(row=0, column=1, sticky="nswe")

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
