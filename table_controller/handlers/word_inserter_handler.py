from utilities import LOGGER_NAME
from table_core import GridLogicHelper, GridStateManager
from table_ui import CanvasLogicHelper
from table_core.grid_commands import InsertWordCommand

import tkinter as tk
import logging

logger = logging.getLogger(LOGGER_NAME)

class WordInserterHandler:
    """
    Handles the insertion of words into the table.
    """

    def __init__(self, controller):
        self.controller = controller

    def insert_word(self, word):
        """
        Handles inserting a word into the currently selected cell, 
        updating the grid state, expanding the grid if needed,
        and moving the cursor to the next cell.
        """        
        # Use WordInserter to insert the word and get the new position
        command = InsertWordCommand(self.controller.state, self.controller.nav, word)
        self.controller.state.execute(command)

        r, c, new_text = command.result
        logger.info(f"Inserted word '{word}' at ({r}, {c}). New text: '{new_text}'")
 
        # If new position exceeds grid size, expand and rebuild UI
        if GridLogicHelper.expand_if_needed(self.controller.state, r, c):
            logger.info(f"Grid expanded due to Tab key at position ({r}, {c})")
            CanvasLogicHelper.rebuild_table(self.controller)

        # Update the UI for the edited cell

        self.controller.canvas_table.entries[r][c].delete(0, tk.END)
        self.controller.canvas_table.entries[r][c].insert(0, new_text)
        logger.debug(f"UI cell ({r}, {c}) updated with text '{new_text}'")

        CanvasLogicHelper.move_cursor_and_focus(self.controller.state, self.controller.nav, self.controller)
        logger.debug(f"Cursor moved to new cell: {self.controller.state.current_pos}")