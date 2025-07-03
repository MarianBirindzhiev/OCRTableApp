from utilities import LOGGER_NAME, BG_COLOR

import tkinter as tk
import logging

logger = logging.getLogger(LOGGER_NAME)

class WindowManager:
    def __init__(self):
        self.root = None
        self.table_windows = []  # List to hold multiple table windows
        self._setup()

    def _setup(self):
        self.root = tk.Tk()
        self.root.title("Table Grid")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.geometry("950x450")
        logger.info("Window manager initialized with main window.")

    def create_table_window(self, title="OCR Image Controller"):
        table_window = tk.Toplevel(self.root)
        table_window.title(title)
        table_window.configure(padx=10, pady=10, bg=BG_COLOR)
        table_window.protocol("WM_DELETE_WINDOW", lambda win=table_window: self.close_table_window(win))
        self.table_windows.append(table_window)
        logger.info(f"Created new table window: {title}")
        return table_window

    def close_table_window(self, window):
        if window in self.table_windows:
            self.table_windows.remove(window)
        window.destroy()
        logger.info("Closed a table window.")

    def on_close(self):
        logger.info("Closing application.")
        # Close all table windows
        for win in self.table_windows[:]:
            win.destroy()
        self.table_windows.clear()
        # Close the main window
        self.root.quit()
        self.root.destroy()