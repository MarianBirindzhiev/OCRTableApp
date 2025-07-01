from ocr import OCRImageProcessor, OCRReader, WordSelectorImage
from utilities import LOGGER_NAME

import logging

logger = logging.getLogger(LOGGER_NAME)

class OCRProcessorManager:
    """
    Manages the OCR processing components of the application.
    """
    def __init__(self, args, controller):
        try:
            logger.info(f"Loading image: {args.image_path}")
            self.processor = OCRImageProcessor(args.image_path, args.scale_percent)
        except FileNotFoundError as e:
            logger.error(f"Failed to load image: {e}")
            raise SystemExit(1)
        self.ocr = OCRReader(language=args.lang)
        ocr_results = self.ocr.read(self.processor.gray_enhanced)
        self.image = WordSelectorImage(self.processor.img, ocr_results, controller.controller, controller.window_manager.table_window)
