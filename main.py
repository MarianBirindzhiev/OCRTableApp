from app import ControllerManager
from app import OCRProcessorManager
from utilities import setup_logger, parse_args, ROWS_DEFAULT, COLS_DEFAULT

import tkinter as tk
import argparse

logger = setup_logger()

class TableOCRApp:
    """Main application class that wires together the UI and logic components."""
    def __init__(self, rows: int = ROWS_DEFAULT, cols: int = COLS_DEFAULT, args: argparse.Namespace = None):
        logger.info("Initializing OCR Table application...")
        self.controller = ControllerManager(rows, cols)
        self.processor = OCRProcessorManager(args, self.controller.table_grid_controller)

    def run(self):
        logger.info("Launching application UI.")
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
