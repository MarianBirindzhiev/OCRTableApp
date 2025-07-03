from table_core.grid_commands import AddColumnCommand, AddRowCommand

class GridLogicHelper:
    @staticmethod
    def expand_if_needed(state, row, column, command_manager):
        """
        Expands the grid if the specified row or column is at the edge.
        Executes AddRowCommand or AddColumnCommand via the command manager.

        Parameters:
        - state: the current grid state
        - row: target row index to check
        - column: target column index to check
        - command_manager: manager to handle execution and tracking of commands

        Returns:
        - expanded (bool): True if a row or column was added, otherwise False
        """
        expanded = False
        if row >= state.rows - 1:
            command_manager.execute(AddRowCommand(state))  # Add a new row if at bottom edge
            expanded = True
        if column >= state.cols - 1:
            command_manager.execute(AddColumnCommand(state))  # Add a new column if at right edge
            expanded = True
        return expanded

    @staticmethod
    def next_cell_position(state, nav):
        """
        Calculates the next cell position based on current position and navigation mode.

        Parameters:
        - state: the current grid state
        - nav: navigation controller used to determine direction

        Returns:
        - Tuple[int, int]: the next (row, col) position
        """
        r, c = state.current_pos
        return nav.next_position(r, c, state.rows, state.cols)
