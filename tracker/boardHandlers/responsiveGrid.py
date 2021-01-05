from .boardHandler import BoardHandler


class ResponsiveGrid(BoardHandler):
    def __init__(self, tracker):
        super().__init__(tracker)

        self._grid_layout = self.tracker.config.BOARDS_GRID_LAYOUT
        self._board_classes = {board_class for board_class in self._grid_layout}

    @property
    def board_classes(self):
        return self._board_classes

    def arrange_boards(self):
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

        frame_stretch = {"rows": set(), "columns": set()}

        # Create structures to represent boards layout in grid form
        row_count = max([
            layout["row"]+layout.get("rowspan", 1) for layout in self._grid_layout.values()
        ])
        column_count = max([
            layout["column"]+layout.get("columnspan", 1) for layout in self._grid_layout.values()
        ])
        grid_layout = [[None for i in range(row_count)] for j in range(column_count)]
        board_coords = {}

        # Add boards to structures
        for board in self.tracker.boards:
            board_class = type(board)

            if board_class in self.tracker.visible_boards:  # Filter out non-visible boards
                board_layout = self._grid_layout[board_class]

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
                    if can_move_board(grid_layout, board_coords, board_class, (0, -1)):
                        move_board(grid_layout, board_coords, board_class, (0, -1))
                        no_boards_moved_upwards = False
                        no_boards_moved = False

                if no_boards_moved_upwards:
                    break

            for board_class in board_coords:
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

        frame_stretch["rows"].update(row_indices)
        frame_stretch["columns"].update(column_indices)

        # Render boards
        for board in self.tracker.boards:
            board_class = type(board)

            if board_class in self.tracker.visible_boards:
                updated_board_layout = get_layout_from_coords_list(board_coords[board_class])

                board.render().grid(**updated_board_layout, sticky="nswe")

        return frame_stretch
