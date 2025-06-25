from utilities import LOGGER_NAME

import logging
from copy import deepcopy

logger = logging.getLogger(LOGGER_NAME)

class GridStateManager:
    def __init__(self, rows, cols):
        self.rows = rows # Number of rows in the grid
        self.cols = cols # Number of columns in the grid
        # 2D list initialized with empty strings (""), representing the grid's cells
        self.grid_data = [['' for _ in range(cols)] for _ in range(rows)]
        self.current_pos = (0, 0) # Tracks the currently selected cell (row, col)
        self.undo_stack = [] # Stack to store past grid states (for undo)
        self.redo_stack = [] # Stack to store undone states (for redo)

        logger.info(f"Grid initialized with size {rows}x{cols}")

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

    def resize(self, rows, cols):
        logger.info(f"Resizing grid from {self.rows}x{self.cols} to {rows}x{cols}")
        self.save_state() # Save current state before resizing

        # Create new empty grid with target size
        new_grid = [['' for _ in range(cols)] for _ in range(rows)]

        # Copy data from old grid to new grid (within bounds)
        for r in range(min(self.rows, rows)):
            for c in range(min(self.cols, cols)):
                new_grid[r][c] = self.grid_data[r][c]
        # Update state
        self.rows = rows
        self.cols = cols
        self.grid_data = new_grid

        # Clamp current_pos if it's now out of bounds
        last_row, last_col = self.current_pos
        self.current_pos = (min(last_row, rows - 1), min(last_col, cols - 1))

    def add_row(self):
        self.rows += 1
        self.grid_data.append(['' for _ in range(self.cols)])
        logger.debug(f"Added a new row. Total rows: {self.rows}")

    def add_column(self):
        self.cols += 1
        for row in self.grid_data:
            row.append('')
        logger.debug(f"Added a new column. Total columns: {self.cols}")

    def set_cell(self, row, col, value):
        logger.debug(f"Set cell ({row}, {col}) to '{value}'")
        self.grid_data[row][col] = value

    def get_cell(self, row, col):
        return self.grid_data[row][col]
