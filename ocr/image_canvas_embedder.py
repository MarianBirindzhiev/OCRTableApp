import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import logging
from utilities import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)

class ImageCanvasEmbedder:
    """
    Embeds a Matplotlib image canvas inside a Tkinter container.
    Handles initial display and updating of the image, as well as mouse click bindings.
    """
    def __init__(self, tk_container, image_rgb):
        """
        Initializes the canvas and displays the given image inside the Tkinter UI.

        Parameters:
        - tk_container: the Tkinter frame or window to embed the canvas into
        - image_rgb: the RGB image (as a NumPy array) to display initially
        """
        # Create a Matplotlib figure and axes
        self.fig, self.ax = plt.subplots(figsize=(12, 10))

        # Display the image using imshow and store the artist object
        self.im_artist = self.ax.imshow(image_rgb)

        # Hide the axes for a clean image display
        self.ax.axis('off')

        # Create a FigureCanvas and embed it in the given Tkinter container
        self.canvas = FigureCanvasTkAgg(self.fig, master=tk_container)
        self.canvas.draw()

        # Place the canvas widget inside the Tkinter layout
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

        logger.info("Matplotlib canvas successfully embedded in Tkinter container.")

    def update_image(self, image_rgb):
        """
        Updates the displayed image on the canvas.

        Parameters:
        - image_rgb: the new RGB image to display
        """
        self.im_artist.set_data(image_rgb)
        self.canvas.draw()

    def bind_click(self, handler):
        """
        Binds a mouse click handler to the canvas.

        Parameters:
        - handler: a function to call when the user clicks on the image
        """
        self.canvas.mpl_connect('button_press_event', handler)
