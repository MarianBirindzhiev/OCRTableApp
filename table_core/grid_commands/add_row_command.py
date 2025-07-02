from .command import Command

import logging
from utilities import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)

class AddRowCommand(Command):
    def __init__(self, grid_state):
        self.grid_state = grid_state
        self.added_row_index = None
        self.old_row_data = None  # capture during execute

    def execute(self):
        self.added_row_index = self.grid_state.rows
        self.old_row_data = ['' for _ in range(self.grid_state.cols)]
        self.grid_state.grid_data.append(self.old_row_data.copy())
        self.grid_state.rows += 1
        logger.info("Row added at index %d", self.added_row_index)

    def undo(self):
        if self.grid_state.rows == 0:
            logger.warning("Cannot undo AddRowCommand: no rows to remove.")
            return

        removed_row = self.grid_state.grid_data.pop()
        self.grid_state.rows -= 1
        logger.info("Row removed from index %d", self.added_row_index)

        # Validate match with what was inserted
        if removed_row != self.old_row_data:
            logger.warning("Removed row does not match original inserted row.")

    def redo(self):
        return self.execute()
'''
    def redo(self):
        logger.info("Redoing AddRowCommand...")
        self.grid_state.grid_data.append(self.old_row_data.copy())
        self.grid_state.rows += 1
        logger.info("Row re-added at index %d", self.added_row_index)
'''
