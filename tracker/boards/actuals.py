from functools import partial
from datetime import datetime, timedelta
from tkinter import Frame, Label, Button, StringVar

from ..constants import Constants as TrackerConstants
from ..classes import Timer, DateTicker
from .board import WorkoutBoard


class Actuals(WorkoutBoard):
    def __init__(self, parent, root_render_method):
        super().__init__(parent, root_render_method)
        self._timer = Timer()
        self._date_ticker = DateTicker()

        self._latest_datetime = datetime.now()
        self._show_workout_descriptions = set()
        self._historical_actuals_date = self._latest_datetime.date()

        self._weekday_datetime__variable = StringVar()
        self._timer__variable = StringVar()
        self._historical_actuals_date__variable = StringVar()

    @property
    def is_needs_render(self):
        if self._date_ticker.is_tomorrow:
            # If Actuals was displaying the current date, it should continue to do
            current_date = datetime.now().date()
            if self._historical_actuals_date + timedelta(days=1) == current_date:
                self._historical_actuals_date = self._latest_datetime.date()

            return True

    def update(self):
        self._latest_datetime = datetime.now()

        self._weekday_datetime__variable.set(self._latest_datetime.strftime("%a %Y/%m/%d %H:%M:%S"))
        self._timer__variable.set(self._timer.elapsed_string)
        self._historical_actuals_date__variable.set(
            self._historical_actuals_date.strftime("%a %Y/%m/%d (Retrospective)"))

    def render(self):
        if self.frame:
            self.frame.destroy()
        self.frame = Frame(self.parent.frame, borderwidth=TrackerConstants.SUNKEN_BORDER_WIDTH, relief="sunken")

        self.frame.grid_columnconfigure(3, minsize=TrackerConstants.DIVIDER_SIZE)
        self.frame.grid_columnconfigure(9, minsize=TrackerConstants.DIVIDER_SIZE)
        self.frame.grid_rowconfigure(1, minsize=TrackerConstants.DIVIDER_SIZE)

        # Calibrated to ensure the board width does not change when switching date, with minimal spacing
        self.frame.grid_columnconfigure(1, minsize=235)
        self.frame.grid_columnconfigure(6, minsize=77)

        self.frame.grid_columnconfigure(4, minsize=29)
        self.frame.grid_columnconfigure(5, minsize=21)
        self.frame.grid_columnconfigure(7, minsize=21)
        self.frame.grid_columnconfigure(8, minsize=29)

        # Variables
        row_index = 0
        is_rendering_today = self._historical_actuals_date == self._latest_datetime.date()

        lambda_increment_date = lambda: self._increment_class_var(
            "_historical_actuals_date", timedelta(days=1),
            min_value=TrackerConstants.MIN_DATE, max_value=self._latest_datetime.date())
        lambda_decrement_date = lambda: self._increment_class_var(
            "_historical_actuals_date", timedelta(days=-1),
            min_value=TrackerConstants.MIN_DATE, max_value=self._latest_datetime.date())

        workout_types = self.state.registered_get("workout_types")

        if is_rendering_today:
            header_date_var = self._weekday_datetime__variable

            weekday_string = self._latest_datetime.strftime("%a")
            date_string = self._latest_datetime.strftime(TrackerConstants.DATE_KEY_FORMAT)
        else:
            header_date_var = self._historical_actuals_date__variable

            weekday_string = self._historical_actuals_date.strftime("%a")
            date_string = self._historical_actuals_date.strftime(TrackerConstants.DATE_KEY_FORMAT)

        # Header Row
        Button(self.frame, text="<", command=lambda_decrement_date, font=TrackerConstants.BASE_FONT
               ).grid(row=row_index)
        Label(self.frame, textvariable=header_date_var, font=TrackerConstants.BASE_FONT
              ).grid(row=row_index, column=1)
        Button(self.frame, text=">", command=lambda_increment_date, font=TrackerConstants.BASE_FONT
               ).grid(row=row_index, column=2)
        row_index += 1

        # Workout Types
        for workout_type_id in workout_types:
            # Variables and logic to filter displayed elements
            workout_type_details = self.state.registered_get("workout_type_details", [workout_type_id])
            workout_sets_scheduled = self.state.registered_get("scheduled_sets_single_entry",
                                                               [weekday_string, workout_type_id])
            workout_reps_actual = self.state.registered_get("completed_reps_single_entry",
                                                            [date_string, workout_type_id])
            is_workout_disabled = self.state.registered_get("is_workout_disabled", [workout_type_id])

            if is_rendering_today:
                if is_workout_disabled:
                    continue  # Ignore workout types that have been disabled
            else:
                if workout_sets_scheduled == 0 and workout_reps_actual == 0:
                    continue  # Ignore workout types that were not scheduled nor performed on this date

            workout_name = workout_type_details["name"]
            workout_desc = workout_type_details["desc"]
            workout_reps = workout_type_details["single_set_repetitions"]
            workout_sets_actual = int(workout_reps_actual/workout_reps)

            status_colour = self._determine_workout_status_color(workout_sets_scheduled, workout_sets_actual)

            # Generate workout type UI elements
            row_index += 1

            Label(self.frame, text=workout_name, font=TrackerConstants.BASE_FONT
                  ).grid(row=row_index, column=1)
            Label(self.frame, text="{0}/{1} sets".format(workout_sets_actual, workout_sets_scheduled),
                  bg=status_colour, font=TrackerConstants.BASE_FONT
                  ).grid(row=row_index, column=6)

            if is_rendering_today:
                Button(self.frame, text="-5",
                       command=partial(
                           self._increment_workout_reps_completed, workout_type_id, date_string, (workout_reps*-5)),
                       font=TrackerConstants.BASE_FONT
                       ).grid(row=row_index, column=4)
                Button(self.frame, text="-",
                       command=partial(
                           self._increment_workout_reps_completed, workout_type_id, date_string, (workout_reps*-1)),
                       font=TrackerConstants.BASE_FONT
                       ).grid(row=row_index, column=5)
                Button(self.frame, text="+",
                       command=partial(
                           self._increment_workout_reps_completed, workout_type_id, date_string, (workout_reps*1)),
                       font=TrackerConstants.BASE_FONT
                       ).grid(row=row_index, column=7)
                Button(self.frame, text="+5",
                       command=partial(
                           self._increment_workout_reps_completed, workout_type_id, date_string, (workout_reps*5)),
                       font=TrackerConstants.BASE_FONT
                       ).grid(row=row_index, column=8)

            # Description
            Button(self.frame, text="Desc", command=partial(self._toggle_workout_desc, workout_type_id),
                   font=TrackerConstants.BASE_FONT
                   ).grid(row=row_index, column=10)

            if workout_type_id in self._show_workout_descriptions:
                row_index += 1

                Label(self.frame,
                      text="{0}\n\n{1} repetitions of the above completes a single set.".format(
                          workout_desc, workout_reps),
                      font=TrackerConstants.SMALL_ITALICS_FONT,
                      borderwidth=TrackerConstants.SUNKEN_BORDER_WIDTH, relief="sunken"
                      ).grid(row=row_index, column=1)

        # Timer
        row_index += 1

        self.frame.grid_rowconfigure(row_index, minsize=TrackerConstants.DIVIDER_SIZE)
        row_index += 1

        Label(self.frame, text="Timer", font=TrackerConstants.BASE_FONT
              ).grid(row=row_index, column=1)
        Label(self.frame, textvariable=self._timer__variable, font=TrackerConstants.BASE_FONT
              ).grid(row=row_index, column=6)

        if self._timer.is_running:
            Button(self.frame, text="Stop", command=lambda: self._toggle_timer("stop"), font=TrackerConstants.BASE_FONT
                   ).grid(row=row_index, column=7, columnspan=2)
        else:
            Button(self.frame, text="Start", command=lambda: self._toggle_timer("start"),
                   font=TrackerConstants.BASE_FONT
                   ).grid(row=row_index, column=7, columnspan=2)
        Button(self.frame, text="Reset", command=lambda: self._toggle_timer("reset"), font=TrackerConstants.BASE_FONT
               ).grid(row=row_index, column=4, columnspan=2)

        return self.frame

    def _toggle_workout_desc(self, workout_type_id):
        if workout_type_id in self._show_workout_descriptions:
            self._show_workout_descriptions.remove(workout_type_id)
        else:
            self._show_workout_descriptions.add(workout_type_id)

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
        pass

    @staticmethod
    def _determine_workout_status_color(scheduled_sets, actual_sets):
        if actual_sets > scheduled_sets:
            status_colour = TrackerConstants.COLOURS["green"]
        elif actual_sets == scheduled_sets and actual_sets > 0:
            status_colour = TrackerConstants.COLOURS["blue"]
        elif actual_sets == scheduled_sets:
            status_colour = TrackerConstants.COLOURS["grey"]
        elif actual_sets > 0:
            status_colour = TrackerConstants.COLOURS["yellow"]
        else:
            status_colour = TrackerConstants.COLOURS["orange"]  # Default

        return status_colour
