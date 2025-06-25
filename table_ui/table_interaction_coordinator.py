from utilities import LOGGER_NAME
from .handlers import (
        WordInserterHandler, 
        ResizeHandler, 
        HistoryHandler, 
        CellEditHandler, 
        NavigationHandler
)

import logging

logger = logging.getLogger(LOGGER_NAME)

class TableInteractionCoordinator:
    def __init__(self, view):
        self.view = view
        logger.info("TableInteractionCoordinator initialized with handlers.")
        self.word_inserter_handler = WordInserterHandler(view)
        self.resize_handler = ResizeHandler(view)
        self.history_handler = HistoryHandler(view)
        self.cell_editor_handler = CellEditHandler(view)
        self.nav_handler = NavigationHandler(view)


 