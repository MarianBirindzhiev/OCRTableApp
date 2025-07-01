from utilities import LOGGER_NAME

import logging
from copy import deepcopy

logger = logging.getLogger(LOGGER_NAME)

class GridHistory:
    """
    Class to manage the history of grid states.
    """

    def __init__(self):
        self.history = []
        self.current_index = -1

    def save_state(self):
        self.undo_stack.append({
            'grid': deepcopy(self.grid_data),   # Save full copy of grid
            'pos': self.current_pos             # Save current position
        })
        self.redo_stack.clear()                 # Clear redo history when new action is taken
        logger.debug(f"State saved: {len(self.undo_stack)} undo actions available")

    def undo(self):
        if not self.undo_stack:
            return
        # Save current state in redo stack before undoing
        self.redo_stack.append({
            'grid': deepcopy(self.grid_data),
            'pos': self.current_pos
        })
        # Restore the last saved state
        state = self.undo_stack.pop()
        self.grid_data = deepcopy(state['grid'])    # Restore grid data
        self.current_pos = state['pos']              # Restore cursor position

        # Update internal row/column dimensions based on restored grid
        self.rows = len(self.grid_data)
        self.cols = max(len(row) for row in self.grid_data)
        logger.debug(f"Undo performed: {self.current_pos}")

    def redo(self):
        if not self.redo_stack:
            return
        # Save current state in undo stack before redoing
        self.undo_stack.append({
            'grid': deepcopy(self.grid_data),
            'pos': self.current_pos
        })
        # Restore the previously undone state
        state = self.redo_stack.pop()
        self.grid_data = deepcopy(state['grid'])
        self.current_pos = state['pos']
        self.rows = len(self.grid_data)
        self.cols = max(len(row) for row in self.grid_data)
        logger.debug(f"Redo performed: {self.current_pos}")