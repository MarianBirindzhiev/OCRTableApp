from .command import Command
import logging
from utilities import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)

class InsertRowCommand(Command):
    """
    Command that adds a new row to the grid at a specified index and supports undo/redo.
    """

    def __init__(self, grid_state, row_index):
        self.grid_state = grid_state                 # Reference to the grid manager
        self.row_index = row_index                   # Index where the row should be inserted
        self.removed_row = []                        # Stores removed row data for undo

    def execute(self):
        """
        Adds a new empty row at the specified index in the grid.
        """
        logger.info(f"Executing InsertRowCommand at index {self.row_index}...")
        
        # Validate row index
        if self.row_index < 0 or self.row_index > self.grid_state.rows:
            logger.warning(f"Invalid row index {self.row_index}. Must be between 0 and {self.grid_state.rows}")
            self.row_index = self.grid_state.rows  # Default to append at end
        
        # Create new empty row with the same number of columns
        new_row = [''] * self.grid_state.cols
        
        # Insert the new row at the specified index
        self.grid_state.grid_data.insert(self.row_index, new_row)

        self.grid_state.rows += 1                    # Update total row count
        logger.info(f"Row inserted at index {self.row_index}")

    def undo(self):
        """
        Undoes the addition of the row by removing the row at the specified index.
        """
        logger.info(f"Undoing InsertRowCommand at index {self.row_index}...")
        
        if self.grid_state.rows == 0:
            logger.warning("Cannot undo InsertRowCommand: no rows to remove.")
            return
            
        if self.row_index >= self.grid_state.rows:
            logger.warning(f"Cannot undo InsertRowCommand: invalid row index {self.row_index}")
            return

        # Store the content of the row being removed for potential redo
        self.removed_row = self.grid_state.grid_data[self.row_index][:]

        # Remove the row at the specified index
        self.grid_state.grid_data.pop(self.row_index)

        self.grid_state.rows -= 1                    # Decrease row count
        logger.info(f"Row removed from index {self.row_index}")