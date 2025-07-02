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

    def execute(self, command):
        command.execute()
        self.undo_stack.append(command)
        self.redo_stack.clear()

    def undo(self):
        if not self.undo_stack:
            return
        command = self.undo_stack.pop()
        command.undo()
        self.redo_stack.append(command)

    def redo(self):
        if not self.redo_stack:
            return
        command = self.redo_stack.pop()
        command.execute()
        self.undo_stack.append(command)
        
    def get_cell(self, row, col):
        if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
            logger.error(f"Attempted to access invalid cell ({row}, {col})")
            raise IndexError("Cell coordinates out of bounds")
        return self.grid_data[row][col]
