from utilities import LOGGER_NAME
from table_ui import CanvasLogicHelper
from table_core.grid_commands import ClearDataCommand

import logging
import tkinter.messagebox as messagebox

logger = logging.getLogger(LOGGER_NAME)

class ClearDataHandler:
    """
    Handles clearing all data from the table.
    """
    def __init__(self, controller):
        self.controller = controller

    def clear_with_confirmation(self):
        """
        Clear all data with user confirmation dialog.
        """  
        # Check if there's any data to clear
        has_data = any(
            any(cell.strip() for cell in row) 
            for row in self.controller.state.grid_data
        )
        
        if not has_data:
            logger.info("No data to clear - grid is already empty")
            messagebox.showinfo("Clear Data", "The grid is already empty.")
            return
        
        # Ask for confirmation
        result = messagebox.askyesno(
            "Clear All Data",
            "Are you sure you want to clear all data from the table?",
            icon="warning"
        )
        
        if result:
            logger.info("User confirmed data clearing")
            self._clear_all_data()
        else:
            logger.info("User cancelled data clearing")
            
    def _clear_all_data(self):
            """
            Clear all data from the grid while preserving the structure.
            """
            logger.info("Clearing all data from the grid")
            
            # Check if there's any data to clear
            has_data = any(
                any(cell.strip() for cell in row) 
                for row in self.controller.state.grid_data
            )
            
            if not has_data:
                logger.info("No data to clear - grid is already empty")
                return
            
            # Execute the clear data command
            command = ClearDataCommand(self.controller.state)
            self.controller.command_manager.execute(command)
            
            # Rebuild the UI to reflect the changes
            CanvasLogicHelper.rebuild_table(self.controller)
            logger.debug("Canvas rebuilt after clearing data.")