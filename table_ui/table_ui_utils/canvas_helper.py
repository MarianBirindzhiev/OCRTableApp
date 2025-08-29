
class CanvasLogicHelper:
    """
    Helper class for managing table navigation and cell interactions.
    Provides methods to handle cursor movement, grid expansion, and
    visual updates in the table UI.
    """

    @staticmethod
    def move_cursor_and_focus(state, nav, controller):
        """
        Advances the cursor to the next cell and sets keyboard focus.
        """
        r, c = state.current_pos
        r, c = nav.next_position(r, c, state.rows, state.cols)
        state.current_pos = (r, c)
        controller.canvas_table.highlight_active_cell()
        controller.canvas_table.entries[r][c].focus_set()

    @staticmethod
    def rebuild_table(controller):
        """
        Rebuilds the visual grid and reconnects callbacks.
        """
        controller.canvas_table.rebuild_table(
            controller.callbacks
        )