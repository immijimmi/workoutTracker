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
        def can_move_board(layout, coords_list_lookup, _board_class, offset):
            new_coords_list = [
                (_coords[0]+offset[0], _coords[1]+offset[1]) for _coords in coords_list_lookup[_board_class]
            ]

            for _coords in new_coords_list:
                if _coords[0] < 0 or _coords[1] < 0 or layout[_coords[0]][_coords[1]] not in (None, _board_class):
                    return False

            return True

        def move_board(layout, coords_list_lookup, _board_class, offset):
            new_coords_list = [
                (_coords[0]+offset[0], _coords[1]+offset[1]) for _coords in coords_list_lookup[_board_class]
            ]

            for _coords in coords_list_lookup[_board_class]:
                layout[_coords[0]][_coords[1]] = None

            coords_list_lookup[_board_class] = new_coords_list
            for _coords in coords_list_lookup[_board_class]:
                layout[_coords[0]][_coords[1]] = _board_class

        def get_layout_from_coords_list(_coords_list):
            columns = [_coords[0] for _coords in _coords_list]
            rows = [_coords[1] for _coords in _coords_list]

            return {
                "row": min(rows),
                "column": min(columns),
                "rowspan": (max(rows)-min(rows))+1,
                "columnspan": (max(columns)-min(columns))+1
            }

        # Initialise all boards
        self.boards = [board_class(self, self._frame) for board_class in self._config.BOARDS_LAYOUT]

        # Create structures to represent boards layout in grid form
        row_count = max([
            layout["row"]+layout.get("rowspan", 1) for layout in self._config.BOARDS_LAYOUT.values()
        ])
        column_count = max([
            layout["column"]+layout.get("columnspan", 1) for layout in self._config.BOARDS_LAYOUT.values()
        ])
        grid_layout = [[None for i in range(row_count)] for j in range(column_count)]
        board_coords = {}

        # Add boards to structures
        for board in self.boards:
            board_class = type(board)

            if board_class in self.visible_boards:  # Filter out non-visible boards
                board_layout = self._config.BOARDS_LAYOUT[board_class]

                for column_offset in range(board_layout.get("columnspan", 1)):
                    for row_offset in range(board_layout.get("rowspan", 1)):
                        x = board_layout["column"] + column_offset
                        y = board_layout["row"] + row_offset
                        if grid_layout[x][y] is not None:
                            raise ValueError("Boards '{0}' and '{1}' are in the same cell: ({2}, {3})".format(
                                board_class, grid_layout[x][y], x, y
                            ))

                        grid_layout[x][y] = board_class
                        board_coords[board_class] = board_coords.get(board_class, []) + [(x, y)]

        # Shift boards upwards and to the left where possible (prioritising upwards)
        while True:
            no_boards_moved = True

            while True:
                no_boards_moved_upwards = True

                for board_class in board_coords:
                    coords_list = board_coords[board_class]

                    if can_move_board(grid_layout, board_coords, board_class, (0, -1)):
                        move_board(grid_layout, board_coords, board_class, (0, -1))
                        no_boards_moved_upwards = False
                        no_boards_moved = False

                if no_boards_moved_upwards:
                    break

            for board_class in board_coords:
                coords_list = board_coords[board_class]

                if can_move_board(grid_layout, board_coords, board_class, (-1, 0)):
                    move_board(grid_layout, board_coords, board_class, (-1, 0))
                    no_boards_moved = False
                    break  # After one leftward move, upward moves will be attempted again

            if no_boards_moved:
                break

        # Apply frame stretch to cells
        row_indices = set()
        column_indices = set()

        for coords_list in board_coords.values():
            for coords in coords_list:
                column_indices.add(coords[0])
                row_indices.add(coords[1])

        self._apply_frame_stretch(rows=tuple(row_indices), columns=tuple(column_indices))

        # Render boards
        for board in self.boards:
            board_class = type(board)

            if board_class in self.visible_boards:
                updated_board_layout = get_layout_from_coords_list(board_coords[board_class])

                board.render().grid(**updated_board_layout, sticky="nswe")

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
