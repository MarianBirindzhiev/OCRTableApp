from ocr import OCRImageProcessor, OCRReader, WordSelectorImage
from utilities import LOGGER_NAME

import logging

logger = logging.getLogger(LOGGER_NAME)

class OCRProcessorManager:
    """
    Manages the OCR processing components of the application.
    """
    def __init__(self, args, table_controller):
        try:
            logger.info(f"Loading image: {args.image_path}")
            self.processor = OCRImageProcessor(args.image_path, args.scale_percent)
        except FileNotFoundError as e:
            logger.error(f"Failed to load image: {e}")
            raise e
        
        self.ocr = OCRReader(language=args.lang)
        ocr_results = self.ocr.read(self.processor.gray_enhanced)

        self.image = WordSelectorImage(
            self.processor.img, ocr_results, table_controller, table_controller.window_manager.create_table_window(f"{args.image_path} - OCR Results")
        )
