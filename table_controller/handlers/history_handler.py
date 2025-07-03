from utilities import LOGGER_NAME
from table_ui import CanvasLogicHelper

import logging

logger = logging.getLogger(LOGGER_NAME)

class HistoryHandler:
    """
    Handles the history of changes in the table, allowing undo and redo operations.
    """
    def __init__(self, controller):
        self.controller = controller

    def undo(self):
        """
        Undo the last grid operation.
        """
        logger.info("Undo triggered.")
        self.controller.command_manager.undo()
        CanvasLogicHelper.rebuild_table(self.controller)

    def redo(self):
        """
        Redo the last undone operation.
        """
        logger.info("Redo triggered.")
        self.controller.command_manager.redo()
        CanvasLogicHelper.rebuild_table(self.controller)
