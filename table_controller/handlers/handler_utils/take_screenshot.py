from .handler_helper import generate_screenshot_filename
from utilities import LOGGER_NAME

from tkinter import Tk, Toplevel, Canvas, Label, BOTH
from PIL import ImageGrab
import logging
import sys

logger = logging.getLogger(LOGGER_NAME)


class SnipTool(Toplevel):
    def __init__(self, master, on_snip_done_callback):
        """
        A fullscreen overlay window that lets the user select a rectangular region
        on the screen to capture as an image.
        """
        super().__init__(master)
        self.on_snip_done_callback = on_snip_done_callback

        # Setup window transparency and background
        if sys.platform != "darwin":
            self.attributes('-fullscreen', True)
        else:   
            # make a borderless full‐screen window
            self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")
            self.overrideredirect(True)
            self.lift()
      
            # keep it always on top
            self.attributes('-topmost', True)
        
        self.attributes('-alpha', 0.15)
        self.config(bg='#121212')  # Subtle dark overlay

        # Initialize selection state
        self.start_x = self.start_y = self.end_x = self.end_y = None
        self.rect = None
        self.fill_box = None
        self.shadow_boxes = []

        # Canvas that captures mouse input and draws the selection
        self.canvas = Canvas(self, cursor="tcross", bg='#121212', highlightthickness=0)
        self.canvas.pack(fill=BOTH, expand=True)

        # Overlay instruction label
        self.info_label = Label(
            self,
            text="📸 Drag to select area. Press ESC to cancel.",
            font=("Segoe UI", 16, "bold"),
            bg="#121212",
            fg="#aaaaaa",
            padx=20,
            pady=10,
            bd=2,
            relief="solid"
        )
        self.info_label.place(relx=0.5, rely=0.02, anchor="n")

        logger.info("SnipTool initialized. Waiting for user selection.")
        self.bind_events()

    def bind_events(self):
        """Attach mouse and keyboard events for interactive region selection."""
        self.canvas.bind("<ButtonPress-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)
        self.bind("<Escape>", lambda e: self.destroy())

    def on_mouse_down(self, event):
        """Triggered when the user presses the mouse button to start selection."""
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        self.clear_canvas()

        # Create border rectangle and fill box
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y,
            outline='#ffffff', width=4, dash=(7, 5)
        )
        self.fill_box = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y,
            fill='#ffffff', outline=''
        )
        logger.debug(f"Selection started at ({self.start_x}, {self.start_y})")

    def on_mouse_drag(self, event):
        """Updates the selection rectangle as the user drags the mouse."""
        self.end_x = self.canvas.canvasx(event.x)
        self.end_y = self.canvas.canvasy(event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, self.end_x, self.end_y)
        self.canvas.coords(self.fill_box, self.start_x, self.start_y, self.end_x, self.end_y)

    def on_mouse_up(self, event):
        """Triggered when the user releases the mouse to complete the selection."""
        self.end_x = self.canvas.canvasx(event.x)
        self.end_y = self.canvas.canvasy(event.y)

        # Temporarily hide the overlay so ImageGrab doesn't capture it
        self.withdraw()
        self.update()

        x1, y1 = int(min(self.start_x, self.end_x)), int(min(self.start_y, self.end_y))
        x2, y2 = int(max(self.start_x, self.end_x)), int(max(self.start_y, self.end_y))

        logger.debug(f"Selection completed: ({x1}, {y1}) to ({x2}, {y2})")

        # Capture and save the screenshot
        if x2 > x1 and y2 > y1:
            try:
                img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
                file_path = generate_screenshot_filename()
                img.save(file_path)
                logger.info(f"Screenshot saved to {file_path}")
                self.on_snip_done_callback(file_path)
            except Exception as e:
                logger.error(f"Failed to capture screenshot: {e}")
        else:
            logger.warning("Invalid screenshot region selected.")

        self.destroy()

    def clear_canvas(self):
        """Clear all drawn rectangles and reset state."""
        if self.rect:
            self.canvas.delete(self.rect)
        if self.fill_box:
            self.canvas.delete(self.fill_box)
        for box in self.shadow_boxes:
            self.canvas.delete(box)
        self.shadow_boxes.clear()
        logger.debug("Canvas cleared.")


class ScreenshotTaker:
    def __init__(self, on_snip_done_callback):
        """
        Orchestrates launching the snipping tool and handling the captured result.
        """
        root = Tk()
        root.withdraw()
        self.root = root
        self.on_snip_done_callback = on_snip_done_callback
        logger.info("ScreenshotTaker initialized.")

    def start(self):
        """Launches the SnipTool window."""
        logger.info("Launching SnipTool for region selection.")
        SnipTool(self.root, self.on_snip_done_callback)
