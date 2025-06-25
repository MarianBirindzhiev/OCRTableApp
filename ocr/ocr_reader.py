from utilities import LOGGER_NAME

import easyocr
import logging

logger = logging.getLogger(LOGGER_NAME)

# === OCR engine wrapper using EasyOCR ===
class OCRReader:
    def __init__(self, language='en', gpu=True):
        """
        Initialize the OCR reader with language and GPU usage.

        Parameters:
        - language: ISO code for the OCR language (e.g., 'en' for English)
        - gpu: whether to use GPU acceleration (True by default)
        """
        self.language = language                                         # Language for OCR recognition
        self.gpu = gpu                                                   # Use GPU if available

        logger.info(f"Initializing OCRReader (lang='{language}', gpu={gpu})")

        # Create an EasyOCR reader instance
        try:
            self.reader = easyocr.Reader([self.language], gpu=self.gpu)
            logger.info("EasyOCR reader initialized successfully.")
        except Exception as e:
            logger.exception("Failed to initialize EasyOCR reader.")
            raise

    def read(self, img):
        """
        Perform OCR on the given image.

        Parameters:
        - img: a preprocessed image (typically grayscale)

        Returns:
        - List of tuples: each with (bounding_box, text, confidence_score)
        """
        logger.info("Starting OCR scan...")
        try:
            results = self.reader.readtext(img, detail=1, paragraph=False)
            logger.info(f"OCR scan complete: {len(results)} text regions found.")
            return results
        except Exception as e:
            logger.exception("OCR reading failed.")
            raise