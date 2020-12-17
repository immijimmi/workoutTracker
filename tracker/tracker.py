from managedState import State
from managedState.extensions import Registrar, Listeners

from random import shuffle
import json
import logging

from .components import Component, GridHelper
from .constants import Constants


class Tracker(Component):
    def __init__(self, container, config):
        super().__init__(container, styles={
            "frame": {"bg": Constants.DEFAULT_STYLE_ARGS["bg"]}
        }, extensions=[GridHelper])

        self._config = config

        self.state_filename = self._config.STATE_FILENAME
        self.visible_boards = set(self._config.INITIAL_BOARDS_VISIBLE)

        self.state = State(extensions=[Registrar, Listeners])
        self.load_state(self.state_filename, catch=True)
        self.state.add_listener("set", lambda metadata: self.save_state(self.state_filename, catch=True))
        self._register_paths()

        # Board-specific temporary variables
        self.tips = self.state.registered_get("workout_tips")
        shuffle(self.tips)
        self.tips_index = 0

    def _render(self):
        self.boards = [BoardClass(self, self._frame) for BoardClass in self._config.BOARDS]

        self._arrange_boards()

    def _arrange_boards(self):
        boards_lookup = {type(board): board for board in self.boards}
        board_frames_grid_layout = []

        for boards_column in self._config.BOARDS_COLUMNS:
            frames_column = []

            for BoardClass in boards_column:
                board = boards_lookup[BoardClass]

                if BoardClass in self.visible_boards:  # Filter out non-visible boards
                    frame = board.render()
                    frames_column.append(frame)

            board_frames_grid_layout.append(frames_column)

        # Remove empty columns
        board_frames_grid_layout = [column for column in board_frames_grid_layout if column]

        for column_index, frames_column in enumerate(board_frames_grid_layout):
            for row_index, frame in enumerate(frames_column):
                self._apply_frame_stretch(rows=[row_index], columns=[column_index])
                frame.grid(row=row_index, column=column_index, sticky="nswe")

    def load_state(self, filename, catch=False):
        try:
            with open(filename, "r") as data_file:
                self.state.set(json.loads(data_file.read()))
        except (FileNotFoundError, json.decoder.JSONDecodeError) as ex:
            if not catch:
                raise ex

            logging.warning("Unable to load application state from file: {0}".format(ex))

    def save_state(self, filename, catch=False):
        try:
            with open(filename, "w") as data_file:
                data_file.write(json.dumps(self.state.get()))
        except (FileNotFoundError, TypeError) as ex:
            if not catch:
                raise ex

            logging.warning("Unable to save application state to file: {0}".format(ex))

    def _register_paths(self):
        self.state.register("settings", ["settings"], [{}])
        self.state.register("active_schedule_id", ["settings", "active_schedule_id"], [{}, None])

        self.state.register("workout_tips", ["workout_tips"], [[Constants.TIP_PLACEHOLDER]])

        self.state.register("workout_types", ["workout_types"], [{}])
        self.state.register("workout_type_details", ["workout_types", Constants.PATH_DYNAMIC_KEY], [{}, {}])
        self.state.register(
            "is_workout_disabled", ["workout_types", Constants.PATH_DYNAMIC_KEY, "disabled"], [{}, {}, False])

        self.state.register("workout_schedules", ["workout_schedules"], [{}])
        self.state.register(
            "workout_schedule", ["workout_schedules", Constants.PATH_DYNAMIC_KEY], [{}, {}])
        self.state.register(
            "scheduled_sets_single_entry",
            ["workout_schedules", Constants.PATH_DYNAMIC_KEY, "schedule", Constants.PATH_DYNAMIC_KEY, Constants.PATH_DYNAMIC_KEY],
            [{}, {}, {}, {}, 0])
        self.state.register(
            "completed_reps_single_entry",
            ["workout_log", Constants.PATH_DYNAMIC_KEY, Constants.PATH_DYNAMIC_KEY],
            [{}, {}, 0])
