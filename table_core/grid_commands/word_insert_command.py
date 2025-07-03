from .command import Command
from .edit_cell_command import EditCellCommand
from utilities import LOGGER_NAME
import logging

logger = logging.getLogger(LOGGER_NAME)

class InsertWordCommand(Command):
    """
    Command for inserting a word into the currently selected cell in the grid.
    This supports both append and overwrite modes depending on the navigation controller mode.
    """

    def __init__(self, grid_state, nav_controller, word):
        self.grid_state = grid_state  # Reference to the grid state
        self.nav_controller = nav_controller  # Navigation controller to determine mode
        self.word = word  # Word to insert

        self.row, self.col = grid_state.current_pos  # Get current cell coordinates
        self.old_text = grid_state.get_cell(self.row, self.col)  # Store current text for undo

        # Determine new cell content based on navigation mode
        self.new_text = (
            self.old_text + (' ' if self.old_text else '') + word
            if nav_controller.nav_mode == '⟳'
            else word
        )

        # Prepare an inner EditCellCommand to delegate execution and undo logic
        self.edit_command = EditCellCommand(grid_state, self.row, self.col, self.new_text)

        self.result = None  # Will be set after execution with row, col, and inserted text

    def execute(self):
        """
        Executes the word insertion by delegating to an EditCellCommand.
        Updates the result with the affected cell and its new content.
        """
        logger.info(f"Inserting word '{self.word}' into cell ({self.row}, {self.col})")
        self.edit_command.execute()
        self.result = self.row, self.col, self.new_text

    def undo(self):
        """
        Undoes the word insertion, restoring the cell to its previous content.
        """
        logger.info(f"Undoing word insertion in cell ({self.row}, {self.col}): restoring '{self.old_text}'")
        self.edit_command.undo()
