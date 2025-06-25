from utilities import LOGGER_NAME

import tkinter as tk
import logging

logger = logging.getLogger(LOGGER_NAME)

# === WordInserter: Handles inserting text into the table and navigation ===
class WordInserter:
    """
    Initialize the WordInserter with grid state and navigation controller.

    Parameters:
    - state: GridStateManager instance that holds cell data and current position
    - nav: NavigationController instance that determines movement logic
    """
    def __init__(self, state, nav):
        self.state = state
        self.nav = nav
        logger.debug("WordInserter initialized with current position (%d, %d)", *self.state.current_pos)        

    def insert_word(self, word):
        """
        Insert a word into the current cell and return updated info.

        - In append mode (⟳), the word is added after the existing cell content.
        - In other modes, the cell is overwritten with the new word.

        Returns:
        - r, c: the row and column of the updated cell
        - new_text: the updated text inserted into the cell
        """        
        r, c = self.state.current_pos
        logger.info("Inserting word '%s' at cell (%d, %d)", word, r, c)        
        self.state.save_state()
        logger.debug("State saved before modifying cell (%d, %d)", r, c)        
        current_text = self.state.get_cell(r, c)
        if self.nav.nav_mode == '⟳':
            new_text = current_text + (' ' if current_text else '') + word
            logger.debug("Appending word. Old text: '%s', New text: '%s'", current_text, new_text)            
        else:
            new_text = word
            logger.debug("Overwriting cell with: '%s'", new_text)            
        self.state.set_cell(r, c, new_text)
        logger.info("Cell (%d, %d) updated with text: '%s'", r, c, new_text)        

        # Return new position and new text so UI can update itself
        return r, c, new_text
