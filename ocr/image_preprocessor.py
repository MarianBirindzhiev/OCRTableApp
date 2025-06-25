from utilities import LOGGER_NAME

import cv2
import logging

logger = logging.getLogger(LOGGER_NAME)

# === Image processor: loads, resizes, and enhances an image for OCR ===
class OCRImageProcessor:
    def __init__(self, image_path, scale_percent):
        """
        Initialize the processor with image path and scale percentage.
        Automatically loads and preprocesses the image.
        """
        self.image_path = image_path                # Path to the image file
        self.scale_percent = scale_percent          # Percentage to resize the image
        self.img = None                             # Original resized image (in color) 
        self.gray_enhanced = None                   # Preprocessed grayscale image for OCR

        logger.info(f"Initializing OCRImageProcessor for: {image_path} with scale {scale_percent}%")
        self.load_and_preprocess()                  # Perform preprocessing immediately


    def load_and_preprocess(self):
        """
        Load the image from disk, resize it, convert to grayscale,
        and apply contrast enhancement for better OCR results.
        """
        # Load the image using OpenCV
        logger.info("Loading image...")
        img = cv2.imread(self.image_path)
        if img is None:
            logger.error(f"Image not found at path: {self.image_path}")
            raise FileNotFoundError(f"Image not found: {self.image_path}")
        
        logger.info(f"Image loaded: {self.image_path} (original size: {img.shape[1]}x{img.shape[0]})")
        
        # === Resize the image by the given percentage ===
        new_dim = (
            int(img.shape[1] * self.scale_percent / 100), # New width
            int(img.shape[0] * self.scale_percent / 100)  # New height
        )
        img = cv2.resize(img, new_dim, interpolation=cv2.INTER_CUBIC)
        logger.info(f"Image resized to: {new_dim[0]}x{new_dim[1]}")

        # === Convert the image to grayscale ===
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        logger.debug("Converted image to grayscale.")
        # === Apply CLAHE (Contrast Limited Adaptive Histogram Equalization) ===
        # Improves contrast in varying lighting conditions for better OCR accuracy
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        gray_enhanced = clahe.apply(gray)
        logger.debug("Applied CLAHE for contrast enhancement.")
        # Save results to instance variables
        self.img = img                          # Resized color image (for display)
        self.gray_enhanced = gray_enhanced      # Enhanced grayscale image (for OCR)
        logger.info("Image preprocessing complete.")