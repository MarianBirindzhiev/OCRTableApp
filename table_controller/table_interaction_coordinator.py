from utilities import LOGGER_NAME
from .handlers import (
        WordInserterHandler, 
        ResizeHandler, 
        HistoryHandler, 
        CellEditHandler, 
        NavigationHandler,
        ScreenshotOCRHandler,
        ClipboardOCRHandler
)

import logging

logger = logging.getLogger(LOGGER_NAME)

class TableInteractionCoordinator:
    def __init__(self, controller):
        self.controller = controller
        logger.info("TableInteractionCoordinator initialized with handlers.")
        self.word_inserter_handler = WordInserterHandler(controller)
        self.resize_handler = ResizeHandler(controller)
        self.history_handler = HistoryHandler(controller)
        self.cell_editor_handler = CellEditHandler(controller)
        self.nav_handler = NavigationHandler(controller)
        self.screenshot_ocr_handler = ScreenshotOCRHandler(controller)
        self.clipboard_ocr_handler = ClipboardOCRHandler(controller)


 