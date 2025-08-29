from utilities import LOGGER_NAME
from table_core.grid_commands import EditCellCommand

import logging
import tkinter as tk

logger = logging.getLogger(LOGGER_NAME)

class DeleteCellHandler:
    def __init__(self, controller):
        self.controller = controller
        logger.info("DeleteCellHandler initialized.")
        
    def delete_cell_content(self, row, col):
        """Delete entire cell content in select mode"""
        logger.debug(f"Deleting content of cell ({row}, {col})")
            
        # Create command to clear cell
        command = EditCellCommand(self.controller.state, row, col, "")
        self.controller.command_manager.execute(command)
        
        # Update the UI entry
        if (row < len(self.controller.canvas_table.entries) and 
            col < len(self.controller.canvas_table.entries[row])):
            entry = self.controller.canvas_table.entries[row][col]
            # Temporarily enable to clear content
            entry.config(state="normal")
            entry.delete(0, tk.END)
            entry.config(state="readonly")  # Back to readonly
        
        logger.info(f"Cell ({row}, {col}) content cleared")