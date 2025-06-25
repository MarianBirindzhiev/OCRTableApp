from utilities import LOGGER_NAME
from .table_ui_utils.canvas_helper import CanvasLogicHelper
from table_core import GridLogicHelper

import logging

logger = logging.getLogger(LOGGER_NAME)

class TableInteractionHandler:
    def __init__(self, state, nav, word_inserter, exporter, canvas_table, view):
        self.state = state
        self.nav = nav
        self.word_inserter = word_inserter
        self.exporter = exporter
        self.canvas_table = canvas_table
        self.view = view
        self._editing_cell = None
        self._editing_original_value = ''
        logger.info("TableInteractionHandler initialized with state and navigation components.")

    def set_nav_mode(self, mode):
        """
        Callback for setting navigation mode from UI.
        """
        logger.info(f"Navigation mode changed to '{mode}'")        
        self.nav.set_mode(mode)
        self.view.nav_bar.update_mode_buttons(mode)

    def apply_size_from_input(self):
        """
        Callback to apply new row/col dimensions from input controls.
        """
        new_rows, new_cols = self.view.resize_controls.get_dimensions()
        logger.info(f"Applying resize: rows={new_rows}, cols={new_cols}")        
        if new_rows and new_cols:
            self.state.resize(new_rows, new_cols)
            self.canvas_table.rebuild(self.state, self.select_cell, self.start_edit, self.finish_edit, self.handle_tab)
            logger.debug("Canvas rebuilt after resize.")            

    def undo(self):
        """
        Undo the last grid operation.
        """
        logger.info("Undo triggered.")        
        self.state.undo()
        self.canvas_table.rebuild(self.state, self.select_cell, self.start_edit, self.finish_edit, self.handle_tab)

    def redo(self):
        """
        Redo the last undone operation.
        """
        logger.info("Redo triggered.")        
        self.state.redo()
        self.canvas_table.rebuild(self.state, self.select_cell, self.start_edit, self.finish_edit, self.handle_tab)

    def select_cell(self, row, col):
        """
        Update the currently selected cell.
        """
        logger.debug(f"Cell selected: ({row}, {col})")        
        self.state.current_pos = (row, col)
        self.canvas_table.highlight_active_cell()

    def start_edit(self, row, col):
        """
        Called when a cell gains focus — store its original value.
        """
        logger.debug(f"Started editing cell: ({row}, {col})")        
        self._editing_cell = (row, col)
        self._editing_original_value = self.canvas_table.get_entry_value(row, col)

    def finish_edit(self, row, col):
        """
        Called after cell editing is complete — update state if content changed.
        """
        if self._editing_cell != (row, col):
            return
        new_value = self.canvas_table.get_entry_value(row, col)
        if new_value != self._editing_original_value:
            logger.info(f"Cell ({row}, {col}) updated from '{self._editing_original_value}' to '{new_value}'")            
            self.state.save_state()
            self.state.set_cell(row, col, new_value)
            self._editing_original_value = new_value

    def handle_word_insert(self, word):
        """
        Handles inserting a word into the currently selected cell, 
        updating the grid state, expanding the grid if needed,
        and moving the cursor to the next cell.
        """        
        # Use WordInserter to insert the word and get the new position
        r, c, new_text = self.word_inserter.insert_word(word)
        logger.info(f"Inserted word '{word}' at ({r}, {c}). New text: '{new_text}'")
        # Update the state with the new text
        new_r, new_c = GridLogicHelper.next_cell_position(self.state, self.nav)
        logger.debug(f"Next cell after insertion: ({new_r}, {new_c})")        

        # If new position exceeds grid size, expand and rebuild UI
        if GridLogicHelper.expand_if_needed(self.state, r, c):
            logger.info(f"Grid expanded due to Tab key at position ({r}, {c})")
            self.canvas_table.rebuild(
                self.state, self.select_cell, self.start_edit, self.finish_edit, self.handle_tab
            )

        # Update the UI for the edited cell
        import tkinter as tk
        self.canvas_table.entries[r][c].delete(0, tk.END)
        self.canvas_table.entries[r][c].insert(0, new_text)
        logger.debug(f"UI cell ({r}, {c}) updated with text '{new_text}'")        

        CanvasLogicHelper.move_cursor_and_focus(self.state, self.nav, self)
        logger.debug(f"Cursor moved to new cell: {self.state.current_pos}")        

    def handle_tab(self, event):
        """
        Overrides the default Tab key behavior to move the cursor
        to the next logical cell based on navigation mode.
        """
        logger.debug("Tab key pressed. Moving to next cell.")

        # Compute next logical cell
        r, c = GridLogicHelper.next_cell_position(self.state, self.nav)
        logger.debug(f"Computed next position from Tab: ({r}, {c})")

        # If new position exceeds grid size, expand and rebuild UI
        if GridLogicHelper.expand_if_needed(self.state, r, c):
            logger.info(f"Grid expanded due to Tab key at position ({r}, {c})")
            self.canvas_table.rebuild(
                self.state, self.select_cell, self.start_edit, self.finish_edit, self.handle_tab
            )

        CanvasLogicHelper.move_cursor_and_focus(self.state, self.nav, self)
        logger.debug(f"Tab navigation complete. Current position: {self.state.current_pos}")
        return "break"  # Prevent default tab behavior

    def export(self):
        """
        Trigger the exporter to save the current grid.
        """
        logger.info("Exporting grid data.")        
        self.exporter.export(self.state.grid_data)
