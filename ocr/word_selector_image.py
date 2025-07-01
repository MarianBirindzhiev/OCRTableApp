from .image_visualizer import OCRImageVisualizer
from .image_canvas_embedder import ImageCanvasEmbedder
from .handlers import WordClickHandler
from utilities import LOGGER_NAME

import logging

logger = logging.getLogger(LOGGER_NAME)

class WordSelectorImage:
    """
    High-level orchestrator for OCR word selection:
    - Visualizes OCR results on the image
    - Embeds image in the Tkinter interface
    - Handles word-click interaction and insertion
    """

    def __init__(self, img, ocr_results, controller, tk_container):
        """
        Initializes the full word selector interface.

        Parameters:
        - img: BGR image (from OpenCV)
        - ocr_results: list of (box, text, confidence) from OCR
        - controller: logic handler for inserting selected words into a table
        - tk_container: Tkinter widget to host the embedded image viewer
        """
        logger.info("Initializing WordSelectorImage...")

        # Prepare image with red OCR bounding boxes
        self.visualizer = OCRImageVisualizer(img, ocr_results)

        # Embed the RGB image in a Tkinter + Matplotlib canvas
        self.canvas = ImageCanvasEmbedder(tk_container, self.visualizer.get_rgb_image())

        # Handle click events for inserting words
        self.click_handler = WordClickHandler(
            ax=self.canvas.ax,
            ocr_results=ocr_results,
            visualizer=self.visualizer,
            canvas_updater=self.canvas,
            controller=controller
        )

    def show(self):
        """
        Enables the image display and activates click-based word selection.
        """
        logger.info("Activating word selection UI...")
        self.canvas.bind_click(self.click_handler.on_click)
