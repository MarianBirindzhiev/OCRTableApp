from app import ControllerManager
from app import OCRProcessorManager
from utilities import setup_logger, parse_args, ROWS_DEFAULT, COLS_DEFAULT

import tkinter as tk
import argparse
import os

os.environ['TK_FORCE_LIGHT_MODE'] = '1'  # Force light mode for Tkinter

logger = setup_logger()

class TableOCRApp:
    """Main application class that wires together the UI and logic components."""
    def __init__(self, rows: int = ROWS_DEFAULT, cols: int = COLS_DEFAULT, args: argparse.Namespace = None):
        logger.info("Initializing OCR Table application...")
        self.controller = ControllerManager(rows, cols)
        try:
            self.processor = OCRProcessorManager(args, self.controller.table_grid_controller)
        except FileNotFoundError as e:
            self.processor = None

    def run(self):
        logger.info("Launching application UI.")
        if self.processor:
            self.processor.image.show()
        
        self.controller.window_manager.root.mainloop()

if __name__ == "__main__":
    args = parse_args()
    logger.info("Starting application with arguments: %s", args)
    app = TableOCRApp(
        rows=ROWS_DEFAULT,
        cols=COLS_DEFAULT,
        args=args
    )

    app.run()
