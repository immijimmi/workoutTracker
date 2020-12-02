from tkComponents.basicComponents import DateStepper, NumberStepper, ToggleButton, Constants as ComponentConstants

from datetime import datetime, timedelta
from tkinter import Label
from functools import partial

from ..constants import Constants as TrackerConstants
from .constants import Constants
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
        def determine_workout_status_color(scheduled_sets, actual_sets):
            if actual_sets > scheduled_sets:
                colour = Constants.COLOURS["green"]
            elif actual_sets == scheduled_sets and actual_sets > 0:
                colour = Constants.COLOURS["blue"]
            elif actual_sets == scheduled_sets:
                colour = Constants.COLOURS["grey"]
            elif actual_sets > 0:
                colour = Constants.COLOURS["yellow"]
            else:
                colour = Constants.COLOURS["orange"]  # Default

            return colour

        def on_change__date_stepper(date_stepper, increment_amount):
            self._date_offset = date_stepper.offset
            self.render()

        def get_data__number_stepper(workout_id, number_stepper):
            date = (datetime.now() + timedelta(days=self._date_offset))
            date_key = date.strftime(TrackerConstants.DATE_KEY_FORMAT)
            date_weekday = date.strftime("%a")

            workout_details = self.state.registered_get("workout_type_details", [workout_id])
            reps = workout_details["single_set_reps"]

            reps_actual = self.state.registered_get("completed_reps_single_entry", [date_key, workout_id])
            sets_scheduled = self.state.registered_get("scheduled_sets_single_entry", [date_weekday, workout_id])
            sets_actual = int(reps_actual / reps)

            number_stepper.text_format = "{0}" + "/{0} sets".format(sets_scheduled)
            colour = determine_workout_status_color(sets_scheduled, sets_actual)

            if "label" in number_stepper.children:
                number_stepper.children["label"].config(bg=colour)

            return sets_actual

        def on_change__number_stepper(workout_id, number_stepper, increment_amount):
            date = (datetime.now() + timedelta(days=self._date_offset))
            date_key = date.strftime(TrackerConstants.DATE_KEY_FORMAT)

            workout_details = self.state.registered_get("workout_type_details", [workout_id])
            reps = workout_details["single_set_reps"]

            reps_actual = self.state.registered_get("completed_reps_single_entry", [date_key, workout_id])
            sets_actual = int(reps_actual / reps)

            sets_actual_difference = number_stepper.value - sets_actual
            reps_actual_difference = sets_actual_difference * reps

            new_workout_reps_actual = reps_actual + reps_actual_difference
            self.state.registered_set(new_workout_reps_actual, "completed_reps_single_entry", [date_key, workout_id])

        def toggle_workout_desc(workout_id, toggle_button):
            if workout_id in self._visible_workout_descriptions:
                self._visible_workout_descriptions.remove(workout_id)
            else:
                self._visible_workout_descriptions.add(workout_id)

            self.render()

        self._apply_frame_stretch(rows=[1], columns=[4])
        self._apply_dividers(rows=[1], columns=[4])

        self._frame.grid_columnconfigure(1, minsize=Constants.WORKOUT_TYPES_SIZE)
        self._frame.grid_columnconfigure(6, minsize=Constants.WORKOUT_SETS_ACTUALS_SIZE)

        button_minsize_x = ComponentConstants.BUTTON_MINSIZES["base_x"] + ComponentConstants.BUTTON_MINSIZES["char_x"]
        self._frame.grid_columnconfigure(0, minsize=button_minsize_x)
        self._frame.grid_columnconfigure(3, minsize=button_minsize_x)
        self._frame.grid_columnconfigure(5, minsize=button_minsize_x)
        self._frame.grid_columnconfigure(7, minsize=button_minsize_x)

        row_index, column_index = 0, 0

        DateStepper(
            self._frame,
            date_text_format="%a %Y/%m/%d",
            get_data=lambda stepper: self._date_offset,
            on_change=on_change__date_stepper,
            update_interval=500,
            styles={
                "label": {
                    "font": Constants.BASE_FONT,
                    "padx": Constants.PAD__SMALL,
                    "borderwidth": Constants.RIDGE_WIDTH__NORMAL,
                    "relief": "ridge"
                },
                "button": {
                    "font": Constants.BASE_FONT
                }
            }
            ).render().grid(row=row_index, column=column_index, columnspan=4, sticky="nswe")
        row_index += 1

        working_date = datetime.now().date() + timedelta(days=self._date_offset)
        working_date_string = working_date.strftime(TrackerConstants.DATE_KEY_FORMAT)

        workout_types = self.state.registered_get("workout_types")

        for workout_type_id in workout_types:
            workout_type_details = self.state.registered_get("workout_type_details", [workout_type_id])
            workout_sets_scheduled = self.state.registered_get("scheduled_sets_single_entry",
                                                               [working_date.strftime("%a"), workout_type_id])
            workout_reps_actual = self.state.registered_get("completed_reps_single_entry",
                                                            [working_date_string, workout_type_id])
            is_workout_disabled = self.state.registered_get("is_workout_disabled", [workout_type_id])

            if self._date_offset == 0:  # Rendering the current date
                if is_workout_disabled:
                    continue  # Ignore workout types that have been disabled
            else:  # Rendering a previous date
                if workout_sets_scheduled == 0 and workout_reps_actual == 0:
                    continue  # Ignore workout types that were not scheduled nor performed on this date

            workout_name = workout_type_details["name"]
            workout_desc = workout_type_details["desc"]
            workout_reps = workout_type_details["single_set_reps"]

            workout_sets_actual = int(workout_reps_actual / workout_reps)
            status_colour = determine_workout_status_color(workout_sets_scheduled, workout_sets_actual)

            column_index = 1
            row_index += 1
            Label(self._frame, text=workout_name, font=Constants.BASE_FONT, padx=Constants.PAD__SMALL
                  ).grid(row=row_index, column=column_index, sticky="nswe")

            column_index += 1
            Label(self._frame, text="x{0}".format(workout_reps), font=Constants.BASE_FONT, padx=Constants.PAD__TINY
                  ).grid(row=row_index, column=column_index, sticky="nsw")

            column_index += 3 if self._date_offset == 0 else 4
            NumberStepper(
                self._frame,
                get_data=partial(get_data__number_stepper, workout_type_id),
                on_change=partial(on_change__number_stepper, workout_type_id),
                update_interval=200,
                text_format="{0}" + "/{0} sets".format(workout_sets_scheduled),
                step_amounts=(1,) if self._date_offset == 0 else (),
                limits=(0, None),
                styles={
                    "label": {
                        "font": Constants.BASE_FONT,
                        "padx": Constants.PAD__SMALL,
                        "bg": status_colour
                    },
                    "button": {
                        "font": Constants.BASE_FONT
                    }
                }
            ).render().grid(row=row_index, column=column_index,
                            columnspan=3 if self._date_offset == 0 else 1, sticky="nswe")

            column_index += 3 if self._date_offset == 0 else 2
            ToggleButton(
                self._frame,
                text_values={True: "Desc", False: "Desc"},
                get_data=partial(lambda button: workout_type_id in self._visible_workout_descriptions),
                on_change=partial(toggle_workout_desc, workout_type_id),
                styles={
                    "button": {
                        "font": Constants.BASE_FONT
                    }
                }
            ).render().grid(row=row_index, column=column_index, sticky="nswe")

            if workout_type_id in self._visible_workout_descriptions:
                row_index += 1
                Label(self._frame,
                      text=workout_desc, font=Constants.SMALL_ITALICS_FONT,
                      borderwidth=Constants.SUNKEN_WIDTH__SMALL, relief="sunken"
                      ).grid(row=row_index, column=0, columnspan=9, sticky="nswe")

        row_index += 1
