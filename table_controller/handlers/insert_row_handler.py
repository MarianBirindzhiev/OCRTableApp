from utilities import LOGGER_NAME
from table_ui import CanvasLogicHelper
from table_core.grid_commands import InsertRowCommand

import logging

logger = logging.getLogger(LOGGER_NAME)

class InsertRowHandler:
    """
    Handles insertion of new rows into the table.
    """
    def __init__(self, controller):
        self.controller = controller

    def insert_row_at_index(self, row_index):
        """
        Insert a new row at the specified index.
        
        Args:
            row_index (int): Index where the row should be inserted
        """
        logger.info(f"Inserting row at index: {row_index}")
        
        # Validate row index
        if row_index < 0 or row_index > self.controller.state.rows:
            logger.warning(f"Invalid row index {row_index}. Must be between 0 and {self.controller.state.rows}")
            row_index = self.controller.state.rows  # Default to append at end
        
        # Execute the insert row command
        command = InsertRowCommand(self.controller.state, row_index)
        self.controller.command_manager.execute(command)
        
        # Rebuild the UI to reflect the changes
        CanvasLogicHelper.rebuild_table(self.controller)
        logger.debug("Canvas rebuilt after row insertion.")

    def insert_row_after_current(self):
        """
        Insert a new row after the currently selected row.
        If no row is selected, insert at the end.
        """
        current_row = getattr(self.controller, 'selected_row', None)
        if current_row is not None:
            insert_index = current_row + 1
        else:
            insert_index = self.controller.state.rows
        
        logger.info(f"Inserting row after current selection at index: {insert_index}")
        self.insert_row_at_index(insert_index)

    def insert_row_before_current(self):
        """
        Insert a new row before the currently selected row.
        If no row is selected, insert at the beginning.
        """
        current_row, _ = self.controller.state.current_pos
        if current_row is not None:
            insert_index = current_row
        else:
            insert_index = 0
        
        logger.info(f"Inserting row before current selection at index: {insert_index}")
        self.insert_row_at_index(insert_index)

    def append_row(self):
        """
        Add a new row at the end of the table.
        """
        insert_index = self.controller.state.rows
        logger.info(f"Appending row at end: index {insert_index}")
        self.insert_row_at_index(insert_index)

    def prepend_row(self):
        """
        Add a new row at the beginning of the table.
        """
        logger.info("Prepending row at beginning: index 0")
        self.insert_row_at_index(0)