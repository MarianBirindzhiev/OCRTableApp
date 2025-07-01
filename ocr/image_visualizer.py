import cv2
import numpy as np
import logging
from utilities import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)

class OCRImageVisualizer:
    """
    Handles the visual representation of OCR results on an image.
    Draws bounding boxes for OCR-detected words and allows highlighting selections.
    """

    def __init__(self, img, ocr_results):
        """
        Initializes the visualizer with the original image and OCR data.

        Parameters:
        - img: the original OpenCV BGR image
        - ocr_results: list of OCR results as tuples (box, text, confidence)
        """
        self.original_img = img                        # BGR image as input
        self.ocr_results = ocr_results                 # OCR results with bounding boxes
        self.display_img = self._draw_boxes()          # Image with red boxes over words

    def _draw_boxes(self, color=(0, 0, 255)):
        """
        Draw bounding boxes for each OCR-detected word.

        Parameters:
        - color: box color in BGR (default: red)

        Returns:
        - A copy of the original image with boxes drawn
        """
        logger.debug("Drawing OCR bounding boxes...")
        img_copy = self.original_img.copy()
        for box, _, _ in self.ocr_results:
            pts = np.array(box).astype(int)  # Convert bounding box to int points
            cv2.polylines(img_copy, [pts], isClosed=True, color=color, thickness=2)
        return img_copy

    def get_rgb_image(self):
        """
        Convert the current display image from BGR to RGB for Matplotlib display.

        Returns:
        - RGB version of the current image
        """
        return cv2.cvtColor(self.display_img, cv2.COLOR_BGR2RGB)

    def draw_selection(self, box, color=(0, 255, 0)):
        """
        Highlight a selected word by drawing a green (or custom-colored) box over it.

        Parameters:
        - box: the bounding box of the word (polygon points)
        - color: the BGR color to use for highlighting (default: green)
        """
        pts = np.array(box).astype(int)
        cv2.polylines(self.display_img, [pts], isClosed=True, color=color, thickness=2)
