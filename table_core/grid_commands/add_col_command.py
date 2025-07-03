from .command import Command
import logging
from utilities import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)

class AddColumnCommand(Command):
    """
    Command that adds a new column to the grid and supports undo/redo.
    """

    def __init__(self, grid_state):
        self.grid_state = grid_state                 # Reference to the grid manager
        self.added_col_index = None                  # Index where the column is added
        self.removed_cells = []                      # Stores removed cell values for undo

    def execute(self):
        """
        Adds a new empty column at the end of each row in the grid.
        """
        logger.info("Executing AddColumnCommand...")
        self.added_col_index = self.grid_state.cols  # Track where column is added

        for row in self.grid_state.grid_data:
            row.append('')                           # Add empty cell to each row

        self.grid_state.cols += 1                    # Update total column count
        logger.info(f"Column added at index {self.added_col_index}")

    def undo(self):
        """
        Undoes the addition of the column by removing the last column from each row.
        """
        logger.info("Undoing AddColumnCommand...")
        if self.grid_state.cols == 0:
            logger.warning("Cannot undo AddColumnCommand: no columns to remove.")
            return

        # Store the content of the column being removed for potential redo
        self.removed_cells = [row[-1] for row in self.grid_state.grid_data]

        for row in self.grid_state.grid_data:
            row.pop()                                # Remove the last column from each row

        self.grid_state.cols -= 1                    # Decrease column count
        logger.info(f"Column removed from index {self.added_col_index}")
