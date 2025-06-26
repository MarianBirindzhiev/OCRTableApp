from utilities import LOGGER_NAME
from table_ui import CanvasLogicHelper

import logging

logger = logging.getLogger(LOGGER_NAME)

class ResizeHandler:
    """
    Handles resizing of the table UI components.
    """
    def __init__(self, controller):
        self.controller = controller

    def apply_size_from_input(self):
        """
        Callback to apply new row/col dimensions from input controls.
        """
        new_rows, new_cols = self.controller.resize_controls.get_dimensions()
        logger.info(f"Applying resize: rows={new_rows}, cols={new_cols}")        
        if new_rows and new_cols:
            self.controller.state.resize(new_rows, new_cols)
            CanvasLogicHelper.rebuild_table(self.controller)
            logger.debug("Canvas rebuilt after resize.")