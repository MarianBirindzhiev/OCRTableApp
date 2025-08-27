from utilities import LOGGER_NAME
from table_ui import CanvasLogicHelper
from table_core.grid_commands import InsertColumnCommand

import logging

logger = logging.getLogger(LOGGER_NAME)

class InsertColHandler:
    """
    Handles insertion of new columns into the table.
    """
    def __init__(self, controller):
        self.controller = controller

    def insert_col_at_index(self, col_index):
        """
        Insert a new column at the specified index.
        
        Args:
            col_index (int): Index where the column should be inserted
        """
        logger.info(f"Inserting column at index: {col_index}")
        
        # Validate column index
        if col_index < 0 or col_index > self.controller.state.cols:
            logger.warning(f"Invalid column index {col_index}. Must be between 0 and {self.controller.state.cols}")
            col_index = self.controller.state.cols  # Default to append at end
        
        # Execute the insert column command
        command = InsertColumnCommand(self.controller.state, col_index)
        self.controller.command_manager.execute(command)
        
        # Rebuild the UI to reflect the changes
        CanvasLogicHelper.rebuild_table(self.controller)
        logger.debug("Canvas rebuilt after column insertion.")

    def insert_col_after_current(self):
        """
        Insert a new column after the currently selected column.
        If no column is selected, insert at the end.
        """
        current_col = getattr(self.controller, 'selected_col', None)
        if current_col is not None:
            insert_index = current_col + 1
        else:
            insert_index = self.controller.state.cols
        
        logger.info(f"Inserting column after current selection at index: {insert_index}")
        self.insert_col_at_index(insert_index)

    def insert_col_before_current(self):
        """
        Insert a new column before the currently selected column.
        If no column is selected, insert at the beginning.
        """
        _, current_col = self.controller.state.current_pos
        if current_col is not None:
            insert_index = current_col
        else:
            insert_index = 0
        
        logger.info(f"Inserting column before current selection at index: {insert_index}")
        self.insert_col_at_index(insert_index)

    def append_col(self):
        """
        Add a new column at the end of the table.
        """
        insert_index = self.controller.state.cols
        logger.info(f"Appending column at end: index {insert_index}")
        self.insert_col_at_index(insert_index)

    def prepend_col(self):
        """
        Add a new column at the beginning of the table.
        """
        logger.info("Prepending column at beginning: index 0")
        self.insert_col_at_index(0)