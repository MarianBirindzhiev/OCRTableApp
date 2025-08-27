from utilities import LOGGER_NAME
from table_ui import CanvasLogicHelper
from table_core.grid_commands import ResizeGridCommand

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
        new_rows, new_cols = self.controller.lower_controls.get_dimensions()
        logger.info(f"Applying resize: rows={new_rows}, cols={new_cols}")        
        if new_rows and new_cols:
            self.controller.command_manager.execute(ResizeGridCommand(self.controller.state, new_rows, new_cols))
            CanvasLogicHelper.rebuild_table(self.controller)
            logger.debug("Canvas rebuilt after resize.")