from utilities import resource_path, LOGGER_NAME

import os
import sys
import logging
import easyocr

logger = logging.getLogger(LOGGER_NAME)

class OCRReader:
    def __init__(self, language='en', gpu=True):
        """
        Initialize the OCR reader with language and GPU usage.
        """
        self.language = language
        self.gpu = gpu

        logger.info(f"Initializing OCRReader (lang='{language}', gpu={gpu})")

        # Get model directory path
        model_dir = resource_path("models")
        
        # Determine download settings
        running_bundled = hasattr(sys, "_MEIPASS")
        download_enabled = not running_bundled

        # Initialize EasyOCR with proper parameters
        try:
            logger.info(f"Attempting EasyOCR initialization with model_storage_directory='{model_dir}'")
            self.reader = easyocr.Reader(
                [self.language], 
                gpu=self.gpu,
                model_storage_directory=model_dir if os.path.exists(model_dir) else None,
                download_enabled=download_enabled
            )
            logger.info("✅ EasyOCR reader initialized successfully")
            
        except Exception as e:
            logger.exception("❌ Primary EasyOCR initialization failed")
            
            # Fallback 1: Try without custom model directory
            if running_bundled and os.path.exists(model_dir):
                logger.info("Attempting fallback initialization without custom model directory...")
                try:
                    self.reader = easyocr.Reader(
                        [self.language], 
                        gpu=self.gpu,
                        download_enabled=False
                    )
                    logger.info("✅ EasyOCR reader initialized with fallback method")
                    return
                except Exception as e2:
                    logger.exception("❌ Fallback initialization also failed")
            
            # Fallback 2: Try with environment variable
            if running_bundled:
                logger.info("Attempting fallback with EASYOCR_MODULE_PATH...")
                try:
                    # Set environment variable for EasyOCR
                    os.environ['EASYOCR_MODULE_PATH'] = model_dir
                    self.reader = easyocr.Reader(
                        [self.language], 
                        gpu=self.gpu,
                        download_enabled=False
                    )
                    logger.info("✅ EasyOCR reader initialized with environment variable")
                    return
                except Exception as e3:
                    logger.exception("❌ Environment variable fallback failed")
            
            # If all fallbacks fail, raise the original error
            raise Exception(f"All EasyOCR initialization attempts failed. Original error: {str(e)}")

    def read(self, img):
        """
        Perform OCR on the given image.
        """
        logger.info("Starting OCR scan...")
        try:
            results = self.reader.readtext(img, detail=1, paragraph=False)
            logger.info(f"OCR scan complete: {len(results)} text regions found")
            return results
        except Exception as e:
            logger.exception("OCR reading failed")
            raise
