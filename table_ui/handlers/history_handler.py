from utilities import LOGGER_NAME
from table_core import GridLogicHelper
from ..table_ui_utils.canvas_helper import CanvasLogicHelper

import logging

logger = logging.getLogger(LOGGER_NAME)

class HistoryHandler:
    """
    Handles the history of changes in the table, allowing undo and redo operations.
    """
    def __init__(self, view):
        self.view = view

    def undo(self):
        """
        Undo the last grid operation.
        """
        logger.info("Undo triggered.")
        self.view.state.undo()
        self.view.canvas_table.rebuild(
            self.view.state, self.view.select_cell, self.view.start_edit, self.view.finish_edit, self.view.handle_tab
        )

    def redo(self):
        """
        Redo the last undone operation.
        """
        logger.info("Redo triggered.")
        self.view.state.redo()
        self.view.canvas_table.rebuild(
            self.view.state, self.view.select_cell, self.view.start_edit, self.view.finish_edit, self.view.handle_tab
        )
