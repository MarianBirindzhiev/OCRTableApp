from utilities import LOGGER_NAME
from table_core import GridLogicHelper
from ..table_ui_utils.canvas_helper import CanvasLogicHelper

import logging

logger = logging.getLogger(LOGGER_NAME)

class ResizeHandler:
    """
    Handles resizing of the table UI components.
    """
    def __init__(self, view):
        self.view = view

    def apply_size_from_input(self):
        """
        Callback to apply new row/col dimensions from input controls.
        """
        new_rows, new_cols = self.view.resize_controls.get_dimensions()
        logger.info(f"Applying resize: rows={new_rows}, cols={new_cols}")        
        if new_rows and new_cols:
            self.view.state.resize(new_rows, new_cols)
            self.view.canvas_table.rebuild(
                self.view.state, self.view.select_cell, self.view.start_edit, self.view.finish_edit, self.view.handle_tab
            )
            logger.debug("Canvas rebuilt after resize.")