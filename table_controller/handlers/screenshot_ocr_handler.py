from utilities import LOGGER_NAME
from .handler_utils import ScreenshotTaker
from app.ocr_processor_manager import OCRProcessorManager

import logging
from types import SimpleNamespace
import os

logger = logging.getLogger(LOGGER_NAME)

class ScreenshotOCRHandler:
    """
    Handles screenshot capture and initiates OCR processing.
    This class coordinates the UI-based screenshot selection
    and forwards the result to the OCR pipeline.
    """
    
    def __init__(self, controller):
        """
        Initialize with a reference to the main table controller.
        
        Args:
            controller: An instance of TableGridController
        """
        self.controller = controller
        logger.info("ScreenshotOCRHandler initialized.")

    def start_ocr_processing(self):
        """
        Entry point to begin the screenshot and OCR flow.
        Launches the screenshot selection UI.
        """
        logger.info("Starting screenshot process...")
        self._setup()

    def _setup(self):
        """
        Prepares and starts the screenshot region selector tool.
        When done, it will trigger `_on_screenshot_ready`.
        """
        self.taker = ScreenshotTaker(self._on_screenshot_ready)
        self.taker.start()

    def _on_screenshot_ready(self, path):
        """
        Callback executed after screenshot is taken.
        Validates the file and passes it to the OCR processor.
        
        Args:
            path: File path of the saved screenshot
        """
        if not path or not os.path.exists(path):
            logger.error(f"Screenshot path invalid or file not found: {path}")
            return

        logger.info(f"Screenshot successfully captured at: {path}")

        args = SimpleNamespace(
            image_path=path,
            scale_percent=150,  # Adjustable scaling
            lang="en"           # Language for OCR
        )

        try:
            self.processor = OCRProcessorManager(args, self.controller)
            logger.info("OCRProcessorManager initialized and image passed for display.")
            self.processor.image.show()
        except Exception as e:
            logger.exception(f"OCR processing failed: {e}")
