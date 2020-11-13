from managedState import State, KeyQuery
from managedState.registrar import Registrar, KeyQueryFactory
from managedState.listeners import Listeners

import json
import logging
from abc import ABC
from datetime import datetime, timedelta
from functools import partial
from tkinter import Tk, Frame, Label, Button, StringVar


class Constants:
    STATE_FILENAME = "data.json"
    ICON_FILENAME = "blank_icon.ico"
    
    PATH_DYNAMIC_KEY = KeyQueryFactory(lambda sub_state, key: key)

    WINDOW_MINSIZE = (270,80)
    DIVIDER_SIZE = 3

    BASE_FONT = ("Verdana", 10)
    HEADER_FONT = ("Verdana", 10, "bold")
    SMALL_ITALICS_FONT = ("Verdana", 9, "normal", "italic")

    FRAME_UPDATE_DELAY = 250


class Timer:
    def __init__(self):
        self.reset()

    @property
    def is_running(self):
        return self._nodes and len(self._nodes[-1]) < 2

    @property
    def time_elapsed(self):
        result = timedelta(0)
        nodes_working = list(self._nodes)
        
        if self.is_running:
            result += datetime.now() - nodes_working.pop()[0]

        for start_stop_pair in nodes_working:
            result += start_stop_pair[1] - start_stop_pair[0]

        return result

    @property
    def elapsed_string(self):  # Ignores days
        current_elapsed = self.time_elapsed

        hours, rem = divmod(current_elapsed.seconds, 3600)
        mins, seconds = divmod(rem, 60)

        return "{0}:{1}:{2}".format(str(hours).zfill(2), str(mins).zfill(2), str(seconds).zfill(2))

    def reset(self):
        self._nodes = []

    def start(self):
        if self.is_running:
            return

        self._nodes.append([datetime.now()])

    def stop(self):
        if not self.is_running:
            return

        self._nodes[-1].append(datetime.now())


class DateTicker:
    def __init__(self):
        self._date_reference = datetime.now().date()

    @property
    def is_tomorrow(self):
        new_date = datetime.now().date()

        if new_date != self._date_reference:
            self._date_reference = new_date
            return True


class FrameHandler(ABC):
    def __init__(self, state, root_render_method):
        self.state = state
        self._trigger_render = root_render_method  # Should be used when render needs to happen immediately, e.g. on button click

        self._frame = None
    
    @property
    def is_needs_render(self):
        """
        Whenever this property returns True, continue under the assumption that
        the render will then be carried out as a result.
        """
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def render(self, parent):
        """
        All _render methods should return the rendered frame.
        The parent handler should then be responsible for slotting the returned frame into its parent element.
        """
        raise NotImplementedError


class GUI:
    def __init__(self, subhandlers=[]):
        self._window = Tk()
        self._window.title("Workout Logger")
        self._window.minsize(*Constants.WINDOW_MINSIZE)
        self._window.iconbitmap(Constants.ICON_FILENAME)

        self.state = State(extensions=[Registrar, Listeners])
        self._load_state()
        self.state.add_listener("set", lambda metadata: self._save_state())
        """
        Render on state set disabled for the time being due to a bug that it appears to cause in managedState.
        In the meantime, render method will injected into subhandlers so that they can manually trigger it in methods that edit the state.
        """
        # self.state.add_listener("set", lambda metadata: self._render())

        self._frame = None
        self._subhandlers = [subhandler(self.state, self._render) for subhandler in subhandlers]

        self._render()
        self._window.mainloop()

    @property
    def _is_needs_render(self):
        return any([subhandler.is_needs_render for subhandler in self._subhandlers])

    def _update(self):
        if self._is_needs_render:
            self._render()

        else:
            for subhandler in self._subhandlers:
                subhandler.update()

            self._frame.after(Constants.FRAME_UPDATE_DELAY, self._update)

    def _render(self):
        if self._frame:
            self._frame.destroy()
        self._frame = Frame(self._window)

        self._update()
        
        for subhandler in self._subhandlers:
            subhandler.render(self._frame).pack()

        self._frame.pack()

    def _load_state(self):
        try:
            with open(Constants.STATE_FILENAME, "r") as data_file:
                self.state.set(json.loads(data_file.read()))

        except (FileNotFoundError, json.decoder.JSONDecodeError) as ex:
            logging.warning("Unable to load application state from file: {0}".format(ex))

    def _save_state(self):
        with open(Constants.STATE_FILENAME, "w") as data_file:
            data_file.write(json.dumps(self.state.get()))

class Dashboard(FrameHandler):
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
        self._frame.grid_columnconfigure(1, minsize=Constants.DIVIDER_SIZE)
        self._frame.grid_columnconfigure(7, minsize=Constants.DIVIDER_SIZE)
        self._frame.grid_rowconfigure(1, minsize=Constants.DIVIDER_SIZE)

        # Header
        Label(self._frame, textvariable=self.weekday_datetime__variable, font=Constants.HEADER_FONT).grid(
            row=row_index, column=0)
        row_index += 1
    
        # Variables
        current_datetime = datetime.now()
        current_weekday_string = current_datetime.strftime("%a")
        current_date_string = current_datetime.strftime("%Y/%m/%d")
        
        workout_types = self.state.registered_get("workout_types")

        #Workout Types
        for workout_type_id in workout_types:
            workout_type_details = self.state.registered_get("workout_type", [workout_type_id])
            if workout_type_details["archived"]:  # Ignore workout types that have been archived
                continue

            row_index += 1

            # Get data for current workout type from state
            workout_name = workout_type_details["name"]
            workout_desc = workout_type_details["desc"]
            workout_reps = workout_type_details["single_set_repetitions"]

            workout_sets_scheduled = self.state.registered_get("workout_type_sets_scheduled_single_weekday", [current_weekday_string, workout_type_id])
            workout_sets_actual = self.state.registered_get("workout_type_sets_completed_single_date", [current_date_string, workout_type_id])

            # Generate workout type UI elements
            Label(self._frame, text=workout_name, font=Constants.BASE_FONT).grid(
                row=row_index, column=0)
            Button(self._frame, text="-5", command=partial(self._increment_workout_sets_completed, workout_type_id, current_date_string, -5), font=Constants.BASE_FONT).grid(
                row=row_index, column=2)
            Button(self._frame, text="-", command=partial(self._increment_workout_sets_completed, workout_type_id, current_date_string, -1), font=Constants.BASE_FONT).grid(
                row=row_index, column=3)
            Label(self._frame, text="{0}/{1} sets".format(workout_sets_actual, workout_sets_scheduled), font=Constants.BASE_FONT).grid(
                row=row_index, column=4)
            Button(self._frame, text="+", command=partial(self._increment_workout_sets_completed, workout_type_id, current_date_string, 1), font=Constants.BASE_FONT).grid(
                row=row_index, column=5)
            Button(self._frame, text="+5", command=partial(self._increment_workout_sets_completed, workout_type_id, current_date_string, 5), font=Constants.BASE_FONT).grid(
                row=row_index, column=6)
            Button(self._frame, text="Desc", command=partial(self._toggle_workout_desc, workout_type_id), font=Constants.BASE_FONT).grid(
                row=row_index, column=8)
            
            if workout_type_id in self.show_workout_descriptions:
                row_index += 1
                
                Label(self._frame, text="{0}\n\n{1} repetitions of the above completes a single set.".format(workout_desc, workout_reps), font=Constants.SMALL_ITALICS_FONT, borderwidth=1, relief="sunken").grid(
                    row=row_index, column=0)

        row_index += 1
        
        # Dividers
        self._frame.grid_rowconfigure(row_index, minsize=Constants.DIVIDER_SIZE)
        row_index += 1

        # Timer
        Label(self._frame, text="Timer", font=Constants.BASE_FONT).grid(
                row=row_index, column=0)
        if self._timer.is_running:
            Button(self._frame, text="Stop", command=lambda: self._toggle_timer("stop"), font=Constants.BASE_FONT).grid(
                row=row_index, column=2, columnspan=2)
        else:
            Button(self._frame, text="Start", command=lambda: self._toggle_timer("start"), font=Constants.BASE_FONT).grid(
                row=row_index, column=2, columnspan=2)
        Label(self._frame, textvariable=self.timer__variable, font=Constants.BASE_FONT).grid(
            row=row_index, column=4)
        Button(self._frame, text="Reset", command=lambda: self._toggle_timer("reset"), font=Constants.BASE_FONT).grid(
                row=row_index, column=5, columnspan=2)

        return self._frame

    def _increment_workout_sets_completed(self, workout_type_id, date_string_key, increment_amount):  # Increment amount can be negative
        workout_sets_actual = self.state.registered_get("workout_type_sets_completed_single_date", [date_string_key, workout_type_id])
        workout_sets_actual = max(workout_sets_actual + increment_amount, 0)

        self.state.registered_set(workout_sets_actual, "workout_type_sets_completed_single_date", [date_string_key, workout_type_id])
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
        self.state.register("workout_type", ["workout_types", Constants.PATH_DYNAMIC_KEY], [{}, {}])

        self.state.register(
            "workout_type_sets_scheduled_single_weekday",
            ["workout_schedules", Constants.PATH_DYNAMIC_KEY, Constants.PATH_DYNAMIC_KEY],
            [{}, {}, 0])

        self.state.register(
            "workout_type_sets_completed_single_date",
            ["workout_log", Constants.PATH_DYNAMIC_KEY, Constants.PATH_DYNAMIC_KEY],
            [{}, {}, 0])
