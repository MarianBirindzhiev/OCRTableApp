class GridLogicHelper:
    @staticmethod
    def expand_if_needed(state, row, column):
        expanded = False
        if row >= state.rows - 1:
            state.add_row()
            expanded = True
        if column >= state.cols - 1:
            state.add_column()
            expanded = True
        return expanded

    @staticmethod
    def next_cell_position(state, nav):
        r, c = state.current_pos
        return nav.next_position(r, c, state.rows, state.cols)