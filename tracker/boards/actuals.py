from tkComponents.basicComponents import DateStepper, NumberStepper, ToggleButton

from datetime import datetime, timedelta
from tkinter import Label
from functools import partial

from ..constants import Constants as TrackerConstants
from .board import Board


class Actuals(Board):
    def __init__(self, parent, container):
        super().__init__(parent, container)

        self._date_offset = 0

        self._visible_workout_descriptions = set()

    @property
    def display_name(self):
        return "Actuals"

    def _render(self):
        def get_workout_stepper_label_format(_workout_sets_scheduled):
            return "{0}" + "/{0} sets".format(_workout_sets_scheduled)

        def determine_workout_status_color(_workout_sets_actual, _workout_sets_scheduled):
            if _workout_sets_actual > _workout_sets_scheduled:
                return TrackerConstants.COLOURS["green"]
            elif _workout_sets_actual == _workout_sets_scheduled and _workout_sets_actual > 0:
                return TrackerConstants.COLOURS["blue"]
            elif _workout_sets_actual == _workout_sets_scheduled:
                return TrackerConstants.DEFAULT_STYLE_ARGS["fg"]
            elif _workout_sets_actual > 0:
                return TrackerConstants.COLOURS["yellow"]
            else:
                return TrackerConstants.COLOURS["orange"]

        def on_change__date_stepper(_date_stepper, increment_amount):
            self._date_offset = _date_stepper.offset
            self.render()

        def get_data__number_stepper(_workout_type_id, _number_stepper):
            _working_date = (datetime.now() + timedelta(days=self._date_offset))
            _working_date_key = _working_date.strftime(TrackerConstants.DATE_KEY_FORMAT)
            _working_date_weekday = _working_date.strftime("%a")

            _workout_type_details = self.state.registered_get("workout_type_details", [_workout_type_id])
            _workout_reps = _workout_type_details["single_set_reps"]

            _workout_reps_actual = self.state.registered_get(
                "completed_reps_single_entry", [_working_date_key, _workout_type_id])
            _workout_sets_actual = int(_workout_reps_actual / _workout_reps)

            _active_schedule_id = self.state.registered_get("active_schedule_id")
            _workout_sets_scheduled = self.state.registered_get(
                "scheduled_sets_single_entry", [_active_schedule_id, _working_date_weekday, _workout_type_id])

            _number_stepper.text_format = get_workout_stepper_label_format(_workout_sets_scheduled)
            _status_colour = determine_workout_status_color(_workout_sets_actual, _workout_sets_scheduled)

            if "label" in _number_stepper.children:  # The first time this is run, the label will not yet be rendered
                _number_stepper.children["label"].config(bg=_status_colour)

            return _workout_sets_actual

        def on_change__number_stepper(_workout_type_id, _number_stepper, increment_amount):
            _working_date = (datetime.now() + timedelta(days=self._date_offset))
            _working_date_key = _working_date.strftime(TrackerConstants.DATE_KEY_FORMAT)

            _workout_type_details = self.state.registered_get("workout_type_details", [_workout_type_id])
            _workout_reps = _workout_type_details["single_set_reps"]

            _workout_reps_actual = self.state.registered_get(
                "completed_reps_single_entry", [_working_date_key, _workout_type_id])
            _workout_sets_actual = int(_workout_reps_actual / _workout_reps)

            sets_actual_difference = _number_stepper.value - _workout_sets_actual
            reps_actual_difference = sets_actual_difference * _workout_reps
            new_workout_reps_actual = _workout_reps_actual + reps_actual_difference

            self.state.registered_set(
                new_workout_reps_actual, "completed_reps_single_entry", [_working_date_key, _workout_type_id])

        def toggle_workout_desc(_workout_type_id, toggle_button):
            if _workout_type_id in self._visible_workout_descriptions:
                self._visible_workout_descriptions.remove(_workout_type_id)
            else:
                self._visible_workout_descriptions.add(_workout_type_id)

            self.render()

        self._apply_frame_stretch(rows=[1], columns=[4])

        row_index = 0

        date_stepper = DateStepper(
            self._frame,
            date_text_format="%a %Y/%m/%d",
            get_data=lambda stepper: self._date_offset,
            on_change=on_change__date_stepper,
            update_interval=500,
            styles={
                "label": {
                    "font": TrackerConstants.NORMAL_FONT,
                    "width": 14,
                    "padx": TrackerConstants.PAD__SMALL,
                    "borderwidth": TrackerConstants.BORDERWIDTH__SMALL,
                    "relief": "ridge",
                    "fg": TrackerConstants.DEFAULT_STYLE_ARGS["fg"],
                    "bg": TrackerConstants.DEFAULT_STYLE_ARGS["bg"]
                },
                "button": {
                    "font": TrackerConstants.SYMBOL_FONT,
                    "width": 1,
                    "padx": TrackerConstants.PAD__SMALL,
                    "fg": TrackerConstants.DEFAULT_STYLE_ARGS["fg"],
                    "bg": TrackerConstants.DEFAULT_STYLE_ARGS["bg"]
                }
            }
        )
        date_stepper.render().grid(row=row_index, column=0, columnspan=4, sticky="nswe")
        row_index += 1

        date_stepper_back_button_width = date_stepper.children["back_button"].winfo_reqwidth()
        date_stepper_forward_button_width = date_stepper.children["forward_button"].winfo_reqwidth()
        self._frame.grid_columnconfigure(0, minsize=date_stepper_back_button_width)
        self._frame.grid_columnconfigure(3, minsize=date_stepper_forward_button_width)

        working_date = datetime.now().date() + timedelta(days=self._date_offset)
        working_date_key = working_date.strftime(TrackerConstants.DATE_KEY_FORMAT)

        active_schedule_id = self.state.registered_get("active_schedule_id")
        workout_types = self.state.registered_get("workout_types")

        is_date_empty = True
        for workout_type_id in workout_types:
            workout_type_details = self.state.registered_get("workout_type_details", [workout_type_id])
            workout_reps_actual = self.state.registered_get("completed_reps_single_entry",
                                                            [working_date_key, workout_type_id])
            workout_sets_scheduled = self.state.registered_get(
                "scheduled_sets_single_entry", [active_schedule_id, working_date.strftime("%a"), workout_type_id])
            is_workout_disabled = self.state.registered_get("is_workout_disabled", [workout_type_id])

            if self._date_offset == 0:  # Rendering the current date
                if is_workout_disabled:
                    continue  # Ignore workout types that have been disabled
            else:  # Rendering a previous date
                if workout_sets_scheduled == 0 and workout_reps_actual == 0:
                    continue  # Ignore workout types that were not scheduled nor performed on this date
            is_date_empty = False

            workout_name = workout_type_details["name"]
            workout_desc = workout_type_details["desc"]
            workout_reps = workout_type_details["single_set_reps"]

            workout_sets_actual = int(workout_reps_actual / workout_reps)
            status_colour = determine_workout_status_color(workout_sets_actual, workout_sets_scheduled)

            column_index = 1
            row_index += 1
            Label(self._frame, text=workout_name, font=TrackerConstants.NORMAL_FONT,
                  width=len(workout_name), padx=TrackerConstants.PAD__NORMAL,
                  fg=TrackerConstants.DEFAULT_STYLE_ARGS["fg"],
                  bg=TrackerConstants.DEFAULT_STYLE_ARGS["bg"]
                  ).grid(row=row_index, column=column_index, sticky="nswe")

            column_index += 1

            workout_reps_text = "x{0}".format(workout_reps)
            Label(self._frame, text=workout_reps_text, font=TrackerConstants.NORMAL_FONT,
                  width=len(workout_reps_text), padx=TrackerConstants.PAD__SMALL,
                  fg=TrackerConstants.DEFAULT_STYLE_ARGS["fg"],
                  bg=TrackerConstants.DEFAULT_STYLE_ARGS["bg"]
                  ).grid(row=row_index, column=column_index, sticky="nsw")

            column_index += 3 if self._date_offset == 0 else 4
            sets_actual_text_format = get_workout_stepper_label_format(workout_sets_scheduled)
            number_stepper = NumberStepper(
                self._frame,
                get_data=partial(get_data__number_stepper, workout_type_id),
                on_change=partial(on_change__number_stepper, workout_type_id),
                update_interval=200,
                text_format=sets_actual_text_format,
                step_amounts=(1,) if self._date_offset == 0 else (),
                limits=(0, None),
                styles={
                    "label": {
                        "font": TrackerConstants.NORMAL_FONT,
                        "width": len(sets_actual_text_format)-2,  # Format string has 3 chars per inserted int - {0}
                        "padx": TrackerConstants.PAD__SMALL,
                        "bg": status_colour,
                        "fg": TrackerConstants.COLOURS["cool_dark_grey"]
                    },
                    "button": {
                        "font": TrackerConstants.SYMBOL_FONT,
                        "width": 1,
                        "padx": TrackerConstants.PAD__SMALL,
                        "fg": TrackerConstants.DEFAULT_STYLE_ARGS["fg"],
                        "bg": TrackerConstants.DEFAULT_STYLE_ARGS["bg"]
                    }
                }
            )
            number_stepper.render().grid(row=row_index, column=column_index,
                                         columnspan=3 if self._date_offset == 0 else 1, sticky="nswe")

            column_index += 3 if self._date_offset == 0 else 2
            ToggleButton(
                self._frame,
                text_values={True: "Desc", False: "Desc"},
                on_change=partial(toggle_workout_desc, workout_type_id),
                styles={
                    "button": {
                        "font": TrackerConstants.NORMAL_FONT,
                        "width": 4,
                        "padx": TrackerConstants.PAD__SMALL,
                        "fg": TrackerConstants.DEFAULT_STYLE_ARGS["fg"],
                        "bg": TrackerConstants.DEFAULT_STYLE_ARGS["bg"]
                    }
                }
            ).render().grid(row=row_index, column=column_index, sticky="nswe")

            if workout_type_id in self._visible_workout_descriptions:
                row_index += 1
                Label(self._frame,
                      text=workout_desc, font=TrackerConstants.SMALL_ITALICS_FONT,
                      borderwidth=TrackerConstants.BORDERWIDTH__TINY, relief="sunken",
                      fg=TrackerConstants.DEFAULT_STYLE_ARGS["fg"],
                      bg=TrackerConstants.DEFAULT_STYLE_ARGS["bg"]
                      ).grid(row=row_index, column=0, columnspan=9, sticky="nswe")

        row_index += 1

        if not is_date_empty:
            self._apply_dividers(rows=[1], columns=[4])

            number_stepper_label_width = number_stepper.children["label"].winfo_reqwidth()
            self._frame.grid_columnconfigure(6, minsize=number_stepper_label_width)

            if self._date_offset == 0:
                number_stepper_minus_button_width = number_stepper.children["minus_buttons"][0].winfo_reqwidth()
                number_stepper_plus_button_width = number_stepper.children["plus_buttons"][0].winfo_reqwidth()
                self._frame.grid_columnconfigure(5, minsize=number_stepper_minus_button_width)
                self._frame.grid_columnconfigure(7, minsize=number_stepper_plus_button_width)
