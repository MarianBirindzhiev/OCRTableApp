from .command import Command
from utilities import LOGGER_NAME
import logging
from copy import deepcopy

logger = logging.getLogger(LOGGER_NAME)

class ResizeGridCommand(Command):
    def __init__(self, grid_state, new_rows, new_cols):
        self.grid_state = grid_state
        self.new_rows = new_rows
        self.new_cols = new_cols

        # Backup old state for undo
        self.old_rows = grid_state.rows
        self.old_cols = grid_state.cols
        self.old_grid = deepcopy(grid_state.grid_data)
        self.old_pos = grid_state.current_pos

    def execute(self):
        logger.info(f"Executing ResizeGridCommand: {self.old_rows}x{self.old_cols} -> {self.new_rows}x{self.new_cols}")
        self._resize(self.new_rows, self.new_cols)

    def undo(self):
        logger.info(f"Undoing ResizeGridCommand: Restoring size to {self.old_rows}x{self.old_cols}")
        self._resize(self.old_rows, self.old_cols, self.old_grid, self.old_pos)

    def _resize(self, rows, cols, grid=None, pos=None):
        new_grid = [['' for _ in range(cols)] for _ in range(rows)]

        source_grid = grid if grid else self.grid_state.grid_data
        for r in range(min(len(source_grid), rows)):
            for c in range(min(len(source_grid[0]), cols)):
                new_grid[r][c] = source_grid[r][c]

        self.grid_state.rows = rows
        self.grid_state.cols = cols
        self.grid_state.grid_data = new_grid

        if pos:
            self.grid_state.current_pos = pos
        else:
            r, c = self.grid_state.current_pos
            self.grid_state.current_pos = (min(r, rows - 1), min(c, cols - 1))

        logger.debug(f"Grid resized to {rows}x{cols}, cursor at {self.grid_state.current_pos}")
