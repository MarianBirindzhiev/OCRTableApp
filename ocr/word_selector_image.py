from utilities import LOGGER_NAME

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import cv2
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import logging

logger = logging.getLogger(LOGGER_NAME)

# === Handles display and interaction with the image ===
class WordSelectorImage:
    def __init__(self, img, ocr_results, view, tk_container):
        """
        Initializes the image viewer for OCR word selection.

        Parameters:
        - img: Original (BGR) image
        - ocr_results: List of tuples (box, text, confidence)
        - inserter: Instance of WordInserter to handle word placement
        - tk_container: Tkinter container in which to embed the Matplotlib figure
        """
        logger.info("Initializing WordSelectorImage...")
        self.img = img                                # Original OpenCV image (BGR)
        self.ocr_results = ocr_results                # OCR output from EasyOCR
        self.view = view                                # Word insertion logic controller
        self.tk_container = tk_container                # Tkinter frame or window

        self.img_rgb = None                           # RGB version of image for Matplotlib
        self.fig = None                               # Matplotlib figure
        self.ax = None                                # Matplotlib axes
        self.im_artist = None                         # Image artist for dynamic updates
        self.canvas = None                            # Matplotlib canvas embedded in Tkinter

        self.draw_boxes()                             # Draw red OCR boxes initially
        
    def draw_boxes(self, color=(0, 0, 255)):
        """
        Draw bounding boxes around OCR-detected words.

        Parameters:
        - color: Box color in BGR format (default is red)
        """
        logger.debug("Drawing OCR bounding boxes...")
        display_img = self.img.copy()
        for box, _, _ in self.ocr_results:
            pts = np.array(box).astype(int)
            cv2.polylines(display_img, [pts], isClosed=True, color=color, thickness=2)
        # Convert image to RGB for Matplotlib display
        self.img_rgb = cv2.cvtColor(display_img, cv2.COLOR_BGR2RGB)
        logger.debug("Bounding boxes drawn.")

    def setup_matplotlib(self):
        """
        Create the Matplotlib viewer, embed it in Tkinter,
        and handle mouse click events to select words.
        """
        # Setup Matplotlib figure and axes
        logger.info("Setting up matplotlib viewer in Tkinter...")
        self.fig, self.ax = plt.subplots(figsize=(12, 10))
        self.im_artist = self.ax.imshow(self.img_rgb)
        self.ax.axis('off')
        self.fig.tight_layout()
        self.fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

        # Embed Matplotlib canvas in Tkinter container
        self.canvas = FigureCanvasTkAgg(self.fig, master= self.tk_container)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

        # === Define click behavior: insert the clicked word ===
        def on_click(event):
            # Ignore clicks that are outside the image area or not in the axes
            if event.inaxes != self.ax or event.xdata is None or event.ydata is None:
                logger.debug("Click outside image bounds; ignored.")
                return
            x, y = int(event.xdata), int(event.ydata)
            # Loop through all OCR results to find which word (if any) was clicked
            for box, text, _ in self.ocr_results:
                # Convert the bounding box to a NumPy array of integer coordinates
                pts = np.array(box).astype(int)
                # Get bounding box rectangle (min/max x and y) from polygon points
                x_min, y_min = pts[:, 0].min(), pts[:, 1].min()
                x_max, y_max = pts[:, 0].max(), pts[:, 1].max()
                # Check if the mouse click lies within the bounding box
                if x_min <= x <= x_max and y_min <= y <= y_max:
                    logger.info(f"Word selected: '{text}' at ({x},{y})")
                    try:
                        # Insert the selected word into the current table cell
                        self.view.handle_word_insert(text)
                        # Draw a green box to indicate selection
                        cv2.polylines(self.img_rgb, [pts], isClosed=True, color=(0, 255, 0), thickness=2)
                        # Update the displayed image in the Matplotlib canvas
                        self.im_artist.set_data(self.img_rgb)
                        self.canvas.draw()
                    except:
                        logger.error(f"Failed to insert word '{text}' into table.")
                    break       # Stop after the first match

        # Connect the click event to the above handler
        self.canvas.mpl_connect('button_press_event', on_click)
        logger.info("Matplotlib viewer ready.")

    def show(self):
        logger.info("Launching OCR image viewer...")
        self.setup_matplotlib()