from utilities import LOGGER_NAME

import logging
import csv
from tkinter import filedialog
from abc import ABC, abstractmethod

logger = logging.getLogger(LOGGER_NAME)

# === IExporter: Interface for exporting data in different formats ===
class IExporter(ABC):
    @abstractmethod
    def export(self, data):
        """
        Abstract method to export data.
        Must be implemented by any subclass.
        """
        pass

# === CSVExporter: Concrete exporter that saves grid data as a CSV file ===
class CSVExporter(IExporter):
    def export(self, grid_data):
        """
        Prompt the user to save a CSV file, and write the grid data to it.

        Parameters:
        - grid_data: 2D list representing the table/grid content
        """
        # Show file save dialog
        logger.info("Opening file dialog to export grid as CSV.")        
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Save CSV"
        )
        # If user cancels the dialog, exit early
        if not filename:
            logger.info("CSV export cancelled by user.")            
            return
        try:
            # Open file and write data row-by-row
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                for row in grid_data:
                    writer.writerow(row)
            logger.info(f"✅ Grid exported successfully to '{filename}'")
        except Exception as e:
            # Handle unexpected errors (e.g. permission denied)
            logger.exception(f"❌ Failed to export CSV to '{filename}': {e}")
