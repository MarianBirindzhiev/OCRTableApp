from .command import Command
import logging
from utilities import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)

class AddColumnCommand(Command):
    """
    Command that adds a new column to the grid and supports undo/redo.
    """
    def __init__(self, grid_state):
        self.grid_state = grid_state
        self.added_col_index = None
        self.removed_cells = []  # Holds last-column data for undo

    def execute(self):
        logger.info("Executing AddColumnCommand...")
        self.added_col_index = self.grid_state.cols
        for row in self.grid_state.grid_data:
            row.append('')
        self.grid_state.cols += 1
        logger.info(f"Column added at index {self.added_col_index}")


    def undo(self):
        logger.info("Undoing AddColumnCommand...")
        if self.grid_state.cols == 0:
            logger.warning("Cannot undo AddColumnCommand: no columns to remove.")
            return

        # Save data before removing, in case redo is needed
        self.removed_cells = [row[-1] for row in self.grid_state.grid_data]

        for row in self.grid_state.grid_data:
            row.pop()
        self.grid_state.cols -= 1
        logger.info(f"Column removed from index {self.added_col_index}")

    def redo(self):
        return self.execute()

'''
    def redo(self):
        logger.info("Redoing AddColumnCommand...")
        for i, row in enumerate(self.grid_state.grid_data):
            # Use saved values if available
            value = self.removed_cells[i] if i < len(self.removed_cells) else ''
            row.append(value)
        self.grid_state.cols += 1
        logger.info(f"Column re-added at index {self.added_col_index}")
'''