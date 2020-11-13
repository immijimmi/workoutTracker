from functools import partial
from datetime import datetime
from tkinter import Frame, Label, Button, StringVar

from ..constants import Constants as TrackerConstants
from ..classes import Timer, DateTicker
from .board import Board


class Actuals(Board):
    def __init__(self, state, root_render_method):
        super().__init__(state, root_render_method)

        self._register_paths()

        self._timer = Timer()
        self._date_ticker = DateTicker()

        self.show_workout_descriptions = set()

        self.weekday_datetime__variable = StringVar()
        self.timer__variable = StringVar()

    @property
    def is_needs_render(self):
        if self._date_ticker.is_tomorrow:
            return True

    def update(self):
        current_datetime = datetime.now()

        self.weekday_datetime__variable.set(current_datetime.strftime("%a %Y/%m/%d %H:%M:%S"))
        self.timer__variable.set(self._timer.elapsed_string)

    def render(self, parent):
        if self._frame:
            self._frame.destroy()
        self._frame = Frame(parent)

        row_index = 0

        # Dividers
        self._frame.grid_columnconfigure(1, minsize=TrackerConstants.DIVIDER_SIZE)
        self._frame.grid_columnconfigure(7, minsize=TrackerConstants.DIVIDER_SIZE)
        self._frame.grid_rowconfigure(1, minsize=TrackerConstants.DIVIDER_SIZE)

        # Header
        Label(self._frame, textvariable=self.weekday_datetime__variable, font=TrackerConstants.HEADER_FONT).grid(
            row=row_index, column=0)
        row_index += 1

        # Variables
        current_datetime = datetime.now()
        current_weekday_string = current_datetime.strftime("%a")
        current_date_string = current_datetime.strftime("%Y/%m/%d")

        workout_types = self.state.registered_get("workout_types")

        # Workout Types
        for workout_type_id in workout_types:
            workout_type_details = self.state.registered_get("workout_type", [workout_type_id])
            if workout_type_details["archived"]:  # Ignore workout types that have been archived
                continue

            row_index += 1

            # Get data for current workout type from state
            workout_name = workout_type_details["name"]
            workout_desc = workout_type_details["desc"]
            workout_reps = workout_type_details["single_set_repetitions"]

            workout_sets_scheduled = self.state.registered_get("workout_type_sets_scheduled_single_weekday",
                                                               [current_weekday_string, workout_type_id])
            workout_sets_actual = self.state.registered_get("workout_type_sets_completed_single_date",
                                                            [current_date_string, workout_type_id])

            # Generate workout type UI elements
            Label(self._frame, text=workout_name, font=TrackerConstants.BASE_FONT).grid(
                row=row_index, column=0)
            Button(self._frame, text="-5",
                   command=partial(self._increment_workout_sets_completed, workout_type_id, current_date_string, -5),
                   font=TrackerConstants.BASE_FONT).grid(
                row=row_index, column=2)
            Button(self._frame, text="-",
                   command=partial(self._increment_workout_sets_completed, workout_type_id, current_date_string, -1),
                   font=TrackerConstants.BASE_FONT).grid(
                row=row_index, column=3)
            Label(self._frame, text="{0}/{1} sets".format(workout_sets_actual, workout_sets_scheduled),
                  font=TrackerConstants.BASE_FONT).grid(
                row=row_index, column=4)
            Button(self._frame, text="+",
                   command=partial(self._increment_workout_sets_completed, workout_type_id, current_date_string, 1),
                   font=TrackerConstants.BASE_FONT).grid(
                row=row_index, column=5)
            Button(self._frame, text="+5",
                   command=partial(self._increment_workout_sets_completed, workout_type_id, current_date_string, 5),
                   font=TrackerConstants.BASE_FONT).grid(
                row=row_index, column=6)
            Button(self._frame, text="Desc", command=partial(self._toggle_workout_desc, workout_type_id),
                   font=TrackerConstants.BASE_FONT).grid(
                row=row_index, column=8)

            if workout_type_id in self.show_workout_descriptions:
                row_index += 1

                Label(self._frame,
                      text="{0}\n\n{1} repetitions of the above completes a single set.".format(workout_desc,
                                                                                                workout_reps),
                      font=TrackerConstants.SMALL_ITALICS_FONT, borderwidth=1, relief="sunken").grid(
                    row=row_index, column=0)

        row_index += 1

        # Dividers
        self._frame.grid_rowconfigure(row_index, minsize=TrackerConstants.DIVIDER_SIZE)
        row_index += 1

        # Timer
        Label(self._frame, text="Timer", font=TrackerConstants.BASE_FONT).grid(
            row=row_index, column=0)
        if self._timer.is_running:
            Button(self._frame, text="Stop", command=lambda: self._toggle_timer("stop"), font=TrackerConstants.BASE_FONT).grid(
                row=row_index, column=2, columnspan=2)
        else:
            Button(self._frame, text="Start", command=lambda: self._toggle_timer("start"),
                   font=TrackerConstants.BASE_FONT).grid(
                row=row_index, column=2, columnspan=2)
        Label(self._frame, textvariable=self.timer__variable, font=TrackerConstants.BASE_FONT).grid(
            row=row_index, column=4)
        Button(self._frame, text="Reset", command=lambda: self._toggle_timer("reset"), font=TrackerConstants.BASE_FONT).grid(
            row=row_index, column=5, columnspan=2)

        return self._frame

    def _increment_workout_sets_completed(self, workout_type_id, date_string_key,
                                          increment_amount):  # Increment amount can be negative
        workout_sets_actual = self.state.registered_get("workout_type_sets_completed_single_date",
                                                        [date_string_key, workout_type_id])
        workout_sets_actual = max(workout_sets_actual + increment_amount, 0)

        self.state.registered_set(workout_sets_actual, "workout_type_sets_completed_single_date",
                                  [date_string_key, workout_type_id])
        self._trigger_render()

    def _toggle_workout_desc(self, workout_type_id):
        if workout_type_id in self.show_workout_descriptions:
            self.show_workout_descriptions.remove(workout_type_id)
        else:
            self.show_workout_descriptions.add(workout_type_id)

        self._trigger_render()

    def _toggle_timer(self, method_key):
        if method_key == "start":
            self._timer.start()
        elif method_key == "stop":
            self._timer.stop()
        elif method_key == "reset":
            self._timer.reset()
        else:
            raise ValueError

        self._trigger_render()

    def _register_paths(self):
        self.state.register("workout_types", ["workout_types"], [{}])
        self.state.register("workout_type", ["workout_types", TrackerConstants.PATH_DYNAMIC_KEY], [{}, {}])

        self.state.register(
            "workout_type_sets_scheduled_single_weekday",
            ["workout_schedules", TrackerConstants.PATH_DYNAMIC_KEY, TrackerConstants.PATH_DYNAMIC_KEY],
            [{}, {}, 0])

        self.state.register(
            "workout_type_sets_completed_single_date",
            ["workout_log", TrackerConstants.PATH_DYNAMIC_KEY, TrackerConstants.PATH_DYNAMIC_KEY],
            [{}, {}, 0])