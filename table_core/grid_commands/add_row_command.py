from .command import Command

import logging
from utilities import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)

class AddRowCommand(Command):
    """
    Command for adding a new row to the grid.
    Supports undo by removing the added row.
    """

    def __init__(self, grid_state):
        self.grid_state = grid_state  # Reference to the grid state manager
        self.added_row_index = None   # Will store the index where the row is added
        self.old_row_data = None      # Stores the inserted row (for undo validation)

    def execute(self):
        """
        Adds a new row at the end of the grid.
        """
        self.added_row_index = self.grid_state.rows  # Index where the row will be inserted
        self.old_row_data = ['' for _ in range(self.grid_state.cols)]  # Create empty row
        self.grid_state.grid_data.append(self.old_row_data.copy())     # Append row to grid
        self.grid_state.rows += 1  # Update row count
        logger.info("Row added at index %d", self.added_row_index)

    def undo(self):
        """
        Undoes the addition of the row by removing it from the grid.
        """
        if self.grid_state.rows == 0:
            logger.warning("Cannot undo AddRowCommand: no rows to remove.")
            return

        removed_row = self.grid_state.grid_data.pop()  # Remove the last row
        self.grid_state.rows -= 1                      # Decrease row count
        logger.info("Row removed from index %d", self.added_row_index)

        # Optional validation: checks whether the row removed matches what was added
        if removed_row != self.old_row_data:
            logger.warning("Removed row does not match original inserted row.")
