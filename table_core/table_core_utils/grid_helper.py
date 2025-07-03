from table_core.grid_commands import AddColumnCommand, AddRowCommand

class GridLogicHelper:
    @staticmethod
    def expand_if_needed(state, row, column, command_manager):
        expanded = False
        if row >= state.rows - 1:
            command_manager.execute(AddRowCommand(state))
            expanded = True
        if column >= state.cols - 1:
            command_manager.execute(AddColumnCommand(state))
            expanded = True
        return expanded

    @staticmethod
    def next_cell_position(state, nav):
        r, c = state.current_pos
        return nav.next_position(r, c, state.rows, state.cols)