from utilities import LOGGER_NAME
from .canvas_config import InteractionMode

import logging

# Initialize logger for this module
logger = logging.getLogger(LOGGER_NAME)


class CanvasNavigationHandler:
    """
    Handles navigation between cells using arrow keys.
    
    This class manages keyboard navigation within the table, ensuring
    navigation only works in SELECT mode and respects table boundaries.
    """
    
    def __init__(self, table_canvas):
        """
        Initialize the navigation handler.
        
        Args:
            table_canvas: Reference to the parent TableCanvas instance
        """
        self.table_canvas = table_canvas
    
    def navigate(self, current_row: int, current_col: int, direction: str) -> bool:
        """
        Navigate from current position in the given direction.
        
        Navigation only works in SELECT mode. In EDIT mode, arrow keys
        should move the cursor within the text instead of navigating cells.
        
        Args:
            current_row: Starting row position
            current_col: Starting column position
            direction: Direction to move ('up', 'down', 'left', 'right')
            
        Returns:
            True if navigation occurred, False if blocked or invalid
        """
        # Only allow navigation in SELECT mode
        if self.table_canvas.get_interaction_mode() != InteractionMode.SELECT:
            return False
        
        # Calculate new position based on direction
        navigation_map = {
            "up": (current_row - 1, current_col),
            "down": (current_row + 1, current_col),
            "left": (current_row, current_col - 1),
            "right": (current_row, current_col + 1)
        }
        
        new_row, new_col = navigation_map.get(direction, (current_row, current_col))
        
        # Check if new position is valid and within table bounds
        if self._is_valid_position(new_row, new_col):
            # Move to new position
            self.table_canvas.select_cell(new_row, new_col)
            self.table_canvas.focus_cell(new_row, new_col)
            logger.debug(f"Navigated {direction} from ({current_row}, {current_col}) to ({new_row}, {new_col})")
            return True
        
        return False
    
    def _is_valid_position(self, row: int, col: int) -> bool:
        """
        Check if the given position is within table bounds.
        
        Args:
            row: Row index to check
            col: Column index to check
            
        Returns:
            True if position is valid, False otherwise
        """
        return (0 <= row < self.table_canvas.get_row_count() and 
                0 <= col < self.table_canvas.get_col_count())

