from utilities import LOGGER_NAME
import logging

logger = logging.getLogger(LOGGER_NAME)

# === NavigationController: Manages the navigation direction in the table ===
class NavigationController:
    def __init__(self):
        # Default navigation mode is horizontal (right arrow)
        self.nav_mode = '→'

    def set_mode(self, mode):
        """
        Set the current navigation mode.
        """
        self.nav_mode = mode
        logger.info(f"Navigation mode changed to: {mode}")


    def next_position(self, row, col, rows, cols):
        """
        Compute the next cell position based on the current navigation mode.

        Parameters:
        - row, col: Current cell coordinates
        - rows, cols: Total number of rows and columns in the grid

        Returns:
        - A tuple (next_row, next_col) representing the next position
        """
        orig_row, orig_col = row, col
        if self.nav_mode == '→':
            col += 1
            if col >= cols:
                col = cols - 1
        elif self.nav_mode == '↓':
            row += 1
            if row >= rows:
                row = rows - 1
        logger.debug(f"Next position from ({orig_row}, {orig_col}) in mode '{self.nav_mode}' -> ({row}, {col})")
        return row, col
    