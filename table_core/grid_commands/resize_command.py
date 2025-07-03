from .command import Command
from utilities import LOGGER_NAME
import logging
from copy import deepcopy

logger = logging.getLogger(LOGGER_NAME)

class ResizeGridCommand(Command):
    """
    Command that resizes the grid to a new number of rows and columns.
    Supports undo by storing a deep copy of the previous grid state.
    """

    def __init__(self, grid_state, new_rows, new_cols):
        self.grid_state = grid_state  # Reference to the grid state manager
        self.new_rows = new_rows      # Target number of rows
        self.new_cols = new_cols      # Target number of columns

        # Store old grid state for undo
        self.old_rows = grid_state.rows
        self.old_cols = grid_state.cols
        self.old_grid = deepcopy(grid_state.grid_data)  # Deep copy to preserve data
        self.old_pos = grid_state.current_pos           # Save old cursor position

    def execute(self):
        """
        Perform the resize operation with new dimensions.
        """
        logger.info(f"Executing ResizeGridCommand: {self.old_rows}x{self.old_cols} -> {self.new_rows}x{self.new_cols}")
        self._resize(self.new_rows, self.new_cols)

    def undo(self):
        """
        Undo the resize operation by restoring the old dimensions and grid data.
        """
        logger.info(f"Undoing ResizeGridCommand: Restoring size to {self.old_rows}x{self.old_cols}")
        self._resize(self.old_rows, self.old_cols, self.old_grid, self.old_pos)

    def _resize(self, rows, cols, grid=None, pos=None):
        """
        Internal method to perform resizing logic.
        
        Args:
            rows (int): Target row count
            cols (int): Target column count
            grid (list[list[str]]): Optional grid to use instead of current state
            pos (tuple[int, int]): Optional cursor position to restore
        """
        # Initialize new grid with target size
        new_grid = [['' for _ in range(cols)] for _ in range(rows)]

        # Source grid: either given or current grid
        source_grid = grid if grid else self.grid_state.grid_data

        # Copy data within bounds
        for r in range(min(len(source_grid), rows)):
            for c in range(min(len(source_grid[0]), cols)):
                new_grid[r][c] = source_grid[r][c]

        # Update grid state manager
        self.grid_state.rows = rows
        self.grid_state.cols = cols
        self.grid_state.grid_data = new_grid

        # Update cursor position
        if pos:
            self.grid_state.current_pos = pos
        else:
            r, c = self.grid_state.current_pos
            self.grid_state.current_pos = (min(r, rows - 1), min(c, cols - 1))

        logger.debug(f"Grid resized to {rows}x{cols}, cursor at {self.grid_state.current_pos}")
