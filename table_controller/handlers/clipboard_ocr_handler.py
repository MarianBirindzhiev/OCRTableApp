from utilities import LOGGER_NAME
from .handler_utils.clipboard_helper import get_image_from_clipboard
from app.ocr_processor_manager import OCRProcessorManager

import logging
import tkinter as tk
from tkinter import messagebox
from types import SimpleNamespace

logger = logging.getLogger(LOGGER_NAME)

class ClipboardOCRHandler:
    def __init__(self, controller):
        """
        Initialize with a reference to the main table controller.
        Args:
            controller: An instance of TableGridController
        """
        self.controller = controller
        logger.info("ClipboardOCRHandler initialized.")

    def _setup(self):
        try:
            # Get image from clipboard
            path = get_image_from_clipboard()
            
            if path is None:
                messagebox.showwarning(
                    "No Image", 
                    "No image found in clipboard. Please copy an image first."
                )
                logger.warning("No image found in clipboard")
                return
            
            self.path = path
        except Exception as e:
            logger.exception(f"Failed to get image from clipboard: {e}")
            messagebox.showerror("Error", f"Failed to get image from clipboard: {e}")
            return


    def run_ocr_from_clipboard(self):
        """Handle clipboard OCR operation."""
        self._setup()
        logger.info("Starting clipboard OCR process...")
        
        args = SimpleNamespace(
            image_path=self.path,
            scale_percent=150,  # Adjustable scaling
            lang="en"           # Language for OCR
        )

        try:
            self.processor = OCRProcessorManager(args, self.controller)
            logger.info("OCRProcessorManager initialized and image passed for display.")
            self.processor.image.show()
        except Exception as e:
            logger.exception(f"OCR processing failed: {e}")