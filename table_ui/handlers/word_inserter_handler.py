from utilities import LOGGER_NAME
from table_core import GridLogicHelper
from ..table_ui_utils.canvas_helper import CanvasLogicHelper

import tkinter as tk
import logging

logger = logging.getLogger(LOGGER_NAME)

class WordInserterHandler:
    """
    Handles the insertion of words into the table.
    """

    def __init__(self, view):
        self.view = view

    def insert_word(self, word):
        """
        Handles inserting a word into the currently selected cell, 
        updating the grid state, expanding the grid if needed,
        and moving the cursor to the next cell.
        """        
        # Use WordInserter to insert the word and get the new position
        r, c, new_text = self.view.word_inserter.insert_word(word)
        logger.info(f"Inserted word '{word}' at ({r}, {c}). New text: '{new_text}'")
 
        # If new position exceeds grid size, expand and rebuild UI
        if GridLogicHelper.expand_if_needed(self.view.state, r, c):
            logger.info(f"Grid expanded due to Tab key at position ({r}, {c})")
            CanvasLogicHelper.rebuild_table(self.view)

        # Update the UI for the edited cell

        self.view.canvas_table.entries[r][c].delete(0, tk.END)
        self.view.canvas_table.entries[r][c].insert(0, new_text)
        logger.debug(f"UI cell ({r}, {c}) updated with text '{new_text}'")

        CanvasLogicHelper.move_cursor_and_focus(self.view.state, self.view.nav, self.view)
        logger.debug(f"Cursor moved to new cell: {self.view.state.current_pos}")