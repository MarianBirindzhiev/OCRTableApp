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
        
        # Enhanced debugging - log the complete environment
        logger.info(f"Python executable: {sys.executable}")
        logger.info(f"Running bundled: {hasattr(sys, '_MEIPASS')}")
        if hasattr(sys, '_MEIPASS'):
            logger.info(f"Bundle temp dir (_MEIPASS): {sys._MEIPASS}")
        
        logger.info(f"Model directory path: {model_dir}")
        logger.info(f"Model directory exists: {os.path.exists(model_dir)}")
        
        # List ALL files in model directory for debugging
        if os.path.exists(model_dir):
            logger.info("=== Model directory contents ===")
            for root, dirs, files in os.walk(model_dir):
                level = root.replace(model_dir, '').count(os.sep)
                indent = ' ' * 2 * level
                logger.info(f"{indent}{os.path.basename(root)}/")
                subindent = ' ' * 2 * (level + 1)
                for file in files:
                    file_path = os.path.join(root, file)
                    file_size = os.path.getsize(file_path)
                    logger.info(f"{subindent}{file} ({file_size} bytes)")
        else:
            logger.error(f"Model directory does not exist: {model_dir}")

        # Check for required model files
        required_files = ['craft_mlt_25k.pth', 'english_g2.pth']
        missing_files = []
        
        for required_file in required_files:
            file_path = os.path.join(model_dir, required_file)
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                logger.info(f"✅ Found {required_file} ({file_size} bytes)")
            else:
                logger.error(f"❌ Missing {required_file}")
                missing_files.append(required_file)
        
        if missing_files:
            logger.error(f"Missing required model files: {missing_files}")

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
