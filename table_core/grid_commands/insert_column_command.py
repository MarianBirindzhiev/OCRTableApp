from .command import Command
import logging
from utilities import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)

class InsertColumnCommand(Command):
    """
    Command that adds a new column to the grid and supports undo/redo.
    """

    def __init__(self, grid_state, col_index):
        self.grid_state = grid_state                 # Reference to the grid manager
        self.col_index = col_index                   # Index where the column is added
        self.removed_cells = []                      # Stores removed cell values for undo

    def execute(self):
        """
        Adds a new empty column at the specified index in the grid.
        """
        logger.info(f"Executing InsertColumnCommand at index {self.col_index}...")
        
        # Validate column index
        if self.col_index < 0 or self.col_index > self.grid_state.cols:
            logger.warning(f"Invalid column index {self.col_index}. Must be between 0 and {self.grid_state.cols}")
            self.col_index = self.grid_state.cols  # Default to append at end
        
        # Insert empty cell at specified index in each row
        for row in self.grid_state.grid_data:
            row.insert(self.col_index, '')           # Insert empty cell at specified index

        self.grid_state.cols += 1                    # Update total column count
        logger.info(f"Column inserted at index {self.col_index}")

    def undo(self):
        """
        Undoes the addition of the column by removing the column at the specified index.
        """
        logger.info(f"Undoing InsertColumnCommand at index {self.col_index}...")
        
        if self.grid_state.cols == 0:
            logger.warning("Cannot undo InsertColumnCommand: no columns to remove.")
            return
            
        if self.col_index >= self.grid_state.cols:
            logger.warning(f"Cannot undo InsertColumnCommand: invalid column index {self.col_index}")
            return

        # Store the content of the column being removed for potential redo
        self.removed_cells = [row[self.col_index] for row in self.grid_state.grid_data]

        # Remove the column at the specified index from each row
        for row in self.grid_state.grid_data:
            row.pop(self.col_index)                  # Remove column at specified index

        self.grid_state.cols -= 1                    # Decrease column count
        logger.info(f"Column removed from index {self.col_index}")