from .command import Command
import logging
from utilities import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)

class ClearDataCommand(Command):
    """
    Command that clears all data from the grid while preserving structure and supports undo/redo.
    """

    def __init__(self, grid_state):
        self.grid_state = grid_state                 # Reference to the grid manager
        self.backup_data = []                        # Stores all cell data for undo

    def execute(self):
        """
        Clears all data from the grid while keeping the grid structure intact.
        """
        logger.info("Executing ClearDataCommand...")
        
        # Store current data for undo
        self.backup_data = []
        for row in self.grid_state.grid_data:
            self.backup_data.append(row[:])  # Create a copy of each row
        
        # Clear all cells
        for row in self.grid_state.grid_data:
            for i in range(len(row)):
                row[i] = ''
        
        logger.info("All grid data cleared")

    def undo(self):
        """
        Restores all the previously cleared data.
        """
        logger.info("Undoing ClearDataCommand...")
        
        if not self.backup_data:
            logger.warning("Cannot undo ClearDataCommand: no backup data available.")
            return
        
        # Restore the backed up data
        for i, backup_row in enumerate(self.backup_data):
            if i < len(self.grid_state.grid_data):
                for j, cell_value in enumerate(backup_row):
                    if j < len(self.grid_state.grid_data[i]):
                        self.grid_state.grid_data[i][j] = cell_value
        
        logger.info("Grid data restored from backup")