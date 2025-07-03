from utilities import LOGGER_NAME
from .handler_utils.handler_helper import capture_screenshot_to_tmp
from app.ocr_processor_manager import OCRProcessorManager

import logging
from types import SimpleNamespace
import os

logger = logging.getLogger(LOGGER_NAME)

class ScreenshotOCRHandler:
    def __init__(self, controller):
        self.controller = controller
      
    def start_ocr_processing(self):
        self._setup()
        self.processor.image.show()

    def _setup(self):
        self.screenshot_path = capture_screenshot_to_tmp()

        if not self.screenshot_path or not os.path.exists(self.screenshot_path):
            logger.error(f"Screenshot path invalid or file not found: {self.screenshot_path}")
            return
      
        self.args = SimpleNamespace(
            image_path=self.screenshot_path,
            scale_percent=150,
            lang="en"
        )
        logger.info(f"Screenshot saved to: {self.screenshot_path}")
        self.processor = OCRProcessorManager(self.args, self.controller)

