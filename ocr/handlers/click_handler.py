import numpy as np
import logging
from utilities import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)

class WordClickHandler:
    def __init__(self, ax, ocr_results, visualizer, canvas_updater, controller):
        """
        Handles user mouse clicks on an image to select OCR-detected words.

        Parameters:
        - ax: Matplotlib Axes instance used to display the image.
        - ocr_results: List of (bounding box, text, confidence) from OCR.
        - visualizer: Instance of OCRImageVisualizer for drawing selections.
        - canvas_updater: Object that updates the Tkinter-embedded matplotlib canvas.
        - controller: Logic controller for inserting selected text into the table.
        """
        self.ax = ax
        self.ocr_results = ocr_results
        self.visualizer = visualizer
        self.canvas_updater = canvas_updater
        self.controller = controller 

    def on_click(self, event):
        """
        Called when the user clicks on the image canvas.
        Checks if the click was inside an OCR bounding box,
        and if so, triggers word insertion and visual feedback.
        """
        # Ignore clicks outside the image axes or incomplete click data
        if event.inaxes != self.ax or event.xdata is None or event.ydata is None:
            logger.debug("Click outside image bounds; ignored.")
            return

        # Get (x, y) coordinates of the click
        x, y = int(event.xdata), int(event.ydata)

        # Loop through OCR results and check if the click is within a word's bounding box
        for box, text, _ in self.ocr_results:
            pts = np.array(box).astype(int)

            # Compute rectangular bounds of the polygon for hit-testing
            x_min, y_min = pts[:, 0].min(), pts[:, 1].min()
            x_max, y_max = pts[:, 0].max(), pts[:, 1].max()

            # If the click falls inside the box, handle the selection
            if x_min <= x <= x_max and y_min <= y <= y_max:
                logger.info(f"Word selected: '{text}' at ({x},{y})")
                try:
                    # Insert the word into the table via the controller
                    self.controller.insert_word(text)

                    # Highlight the selected word on the image (green box)
                    self.visualizer.draw_selection(box)

                    # Redraw the canvas with the updated image
                    self.canvas_updater.update_image(self.visualizer.get_rgb_image())
                except Exception:
                    logger.exception(f"Failed to insert word '{text}'")
                break  # Stop after the first match
