from table_core import GridStateManager, NavigationController, WordInserter
from table_ui import TableGridView, NavigationBar, ResizeControls, TableCanvas
from ocr import OCRImageProcessor, OCRReader, WordSelectorImage
from utilities import setup_logger, CSVExporter ,BG_COLOR, ROWS_DEFAULT, COLS_DEFAULT

import tkinter as tk
import argparse
import logging

# === Initialize logger ===
logger = setup_logger()

# === Argument parser for command-line usage ===
def parse_args():
    parser = argparse.ArgumentParser(description="Interactive OCR word selector")
    parser.add_argument("image_path", help="Path to the input image")
    parser.add_argument("--scale_percent", type=int, default=150, help="Resize percent (default: 150)")
    parser.add_argument("--output_csv", default="selected_words.csv", help="CSV output file")
    parser.add_argument("--lang", default="en", help="OCR language (default: en)")
    return parser.parse_args()

class TableOCRApp:
    """Main application class that wires together the UI and logic components."""
    def __init__(self, rows=10, cols=10, args = None):
        logger.info("Initializing OCR Table application...")

        # Create the root Tkinter window
        self.root = tk.Tk()
        self.root.title("OCR Image Viewer")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # === Secondary window for table ===
        self.table_window = tk.Toplevel(self.root)
        self.table_window.title("Table Grid")
        self.table_window.geometry("950x450")
        self.table_window.configure(padx=10, pady=10, bg=BG_COLOR)
        self.table_window.protocol("WM_DELETE_WINDOW", self.on_close)

         # Initialize the main components
        self.state_manager = GridStateManager(rows, cols)
        self.nav_controller = NavigationController()
        self.word_inserter = WordInserter(self.state_manager, self.nav_controller)
        self.exporter = CSVExporter()

        # Create the UI components
        self.canvas_table = TableCanvas()
        self.nav_bar = NavigationBar()
        self.resize_controls = ResizeControls(self.state_manager)

        logger.info("Setting up the table UI...")
        self.view = TableGridView(
            root=self.table_window,
            state=self.state_manager,
            nav=self.nav_controller,
            word_inserter=self.word_inserter,
            exporter=self.exporter,
            nav_bar=self.nav_bar,
            resize_controls=self.resize_controls,
            canvas_table=self.canvas_table
        )

        # Load and preprocess image
        try:
            logger.info(f"Loading image: {args.image_path}")
            self.processor = OCRImageProcessor(args.image_path, args.scale_percent)
        except FileNotFoundError as e:
            logger.error(f"Failed to load image: {e}")
            raise SystemExit(1)
        self.ocr = OCRReader(language=args.lang)
        ocr_results = self.ocr.read(self.processor.gray_enhanced)
        self.image = WordSelectorImage(self.processor.img, ocr_results, self.view, self.root)

    def on_close(self):
        logger.info("Closing application.")
        self.root.quit()
        self.root.destroy()

    def run(self):
        logger.info("Launching application UI.")
        self.image.show()
        self.root.mainloop()


if __name__ == "__main__":
    args = parse_args()
    logger.info("Starting application with arguments: %s", args)

    app = TableOCRApp(
        rows=ROWS_DEFAULT,
        cols=COLS_DEFAULT,
        args=args
    )

    app.run()
