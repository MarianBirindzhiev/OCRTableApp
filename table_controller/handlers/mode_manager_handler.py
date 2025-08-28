from utilities import LOGGER_NAME
from table_ui import CanvasLogicHelper
from table_core.grid_commands import EditCellCommand

import logging
import tkinter as tk

logger = logging.getLogger(LOGGER_NAME)

class ModeManagerHandler:
    def __init__(self, controller):
        self.controller = controller
        logger.info("ModeManagerHandler initialized.")
        
    def enter_edit_mode(self, row, col):
        """Enter edit mode for the specified cell"""
        logger.debug(f"Entering edit mode for cell ({row}, {col})")
        
        # Update state
        self.controller.state.interaction_mode = "EDIT"
        self.controller.state.editing_cell = (row, col)
        self.controller.state.current_pos = (row, col)
        
        # Update highlighting to show edit mode (green) - this will also set state to normal
        self.controller.canvas_table.highlight_active_cell()
        
        # Set focus and cursor position
        if (row < len(self.controller.canvas_table.entries) and 
            col < len(self.controller.canvas_table.entries[row])):
            entry = self.controller.canvas_table.entries[row][col]
            entry.focus_set()  # Set focus
            entry.icursor(tk.END)  # Position cursor at end
        
        logger.info(f"Entered edit mode for cell ({row}, {col})")

    def exit_edit_mode(self):
        """Exit edit mode and return to select mode"""
        editing_cell = getattr(self.controller.state, 'editing_cell', None)
        
        if editing_cell is None:
            return
            
        row, col = editing_cell
        logger.debug(f"Exiting edit mode for cell ({row}, {col})")
        
        # Save any changes before exiting
        if (row < len(self.controller.canvas_table.entries) and 
            col < len(self.controller.canvas_table.entries[row])):
            entry = self.controller.canvas_table.entries[row][col]
            new_value = entry.get()
            old_value = self.controller.state.get_cell(row, col)
            
            if new_value != old_value:
                # Save the change via command for undo support
                command = EditCellCommand(self.controller.state, row, col, new_value)
                self.controller.command_manager.execute(command)
        
        # Update state
        self.controller.state.interaction_mode = "SELECT"
        self.controller.state.editing_cell = None
        # Keep current_pos for selection highlighting
        
        # Update highlighting to show select mode (blue) - this will also set state to readonly
        self.controller.canvas_table.highlight_active_cell()
        
        logger.info(f"Exited edit mode, now in SELECT mode")