from utilities import LOGGER_NAME, BG_COLOR

import tkinter as tk
import logging

logger = logging.getLogger(LOGGER_NAME)

class WindowManager:
    def __init__(self):
        self.root = None
        self.table_window = None
        self._setup()

    def _setup(self):
        self.root = tk.Tk()
        self.root.title("OCR Image Viewer")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.table_window = tk.Toplevel(self.root)
        self.table_window.title("Table Grid")
        self.table_window.geometry("950x450")
        self.table_window.configure(padx=10, pady=10, bg=BG_COLOR)
        self.table_window.protocol("WM_DELETE_WINDOW", self.on_close)
        logger.info("Window manager initialized with main and table windows.")

    def on_close(self):
        logger.info("Closing application.")
        self.root.quit()
        self.root.destroy()