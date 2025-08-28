from utilities import LOGGER_NAME
from table_core import GridLogicHelper
from table_ui import CanvasLogicHelper

import logging

logger = logging.getLogger(LOGGER_NAME)

class NavigationHandler:
    def __init__(self, controller):
        self.controller = controller

    def handle_tab(self):
            """
            Overrides the default Tab key behavior to move the cursor
            to the next logical cell based on navigation mode.
            """
            logger.debug("Tab key pressed. Moving to next cell.")

            # Compute next logical cell
            r, c = GridLogicHelper.next_cell_position(self.controller.state, self.controller.nav)
            logger.debug(f"Computed next position from Tab: ({r}, {c})")

            # If new position exceeds grid size, expand and rebuild UI
            if GridLogicHelper.expand_if_needed(self.controller.state, r, c, self.controller.command_manager):
                logger.info(f"Grid expanded due to Tab key at position ({r}, {c})")
                CanvasLogicHelper.rebuild_table(self.controller)

            CanvasLogicHelper.move_cursor_and_focus(self.controller.state, self.controller.nav, self.controller)
            logger.debug(f"Tab navigation complete. Current position: {self.controller.state.current_pos}")
            return "break"  # Prevent default tab behavior
    

    def select_cell(self, row, col):
        """Select a cell (SELECT mode)"""
        logger.debug(f"Selecting cell ({row}, {col})")
        
        # If currently in edit mode, exit it first
        if self.controller.state.interaction_mode == "EDIT":
            self.exit_edit_mode()
        
        # Update state
        self.controller.state.interaction_mode = "SELECT"
        self.controller.state.current_pos = (row, col)
        self.controller.state.editing_cell = None
        
        # Update highlighting
        self.controller.canvas_table.highlight_active_cell()
        
        logger.info(f"Selected cell ({row}, {col})")

    def set_nav_mode(self, mode):
        """
        Callback for setting navigation mode from UI.
        """
        logger.info(f"Navigation mode changed to '{mode}'")        
        self.controller.nav.set_mode(mode)
        self.controller.nav_bar.update_mode_buttons(mode)