
class CanvasLogicHelper:
    """
    Helper class for managing table navigation and cell interactions.
    Provides methods to handle cursor movement, grid expansion, and
    visual updates in the table UI.
    """

    @staticmethod
    def move_cursor_and_focus(state, nav, view):
        """
        Advances the cursor to the next cell and sets keyboard focus.
        """
        r, c = state.current_pos
        r, c = nav.next_position(r, c, state.rows, state.cols)
        state.current_pos = (r, c)
        view.canvas_table.highlight_active_cell()
        view.canvas_table.entries[r][c].focus_set()

    @staticmethod
    def _rebuild_table(view):
        """
        Rebuilds the visual grid and reconnects callbacks.
        """
        view.canvas_table.rebuild(
            view.state,
            view.select_cell,
            view.start_edit,
            view.finish_edit,
            view.handle_tab
        )