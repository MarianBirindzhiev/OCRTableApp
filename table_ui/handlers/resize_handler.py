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
            CanvasLogicHelper.rebuild_table(self.view)
            logger.debug("Canvas rebuilt after resize.")