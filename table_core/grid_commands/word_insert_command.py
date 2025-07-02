from .command import Command
from .edit_cell_command import EditCellCommand
from utilities import LOGGER_NAME
import logging

logger = logging.getLogger(LOGGER_NAME)

class InsertWordCommand(Command):
    def __init__(self, grid_state, nav_controller, word):
        self.grid_state = grid_state
        self.nav_controller = nav_controller
        self.word = word

        self.row, self.col = grid_state.current_pos
        self.old_text = grid_state.get_cell(self.row, self.col)

        self.new_text = (
            self.old_text + (' ' if self.old_text else '') + word
            if nav_controller.nav_mode == '⟳'
            else word
        )
        self.edit_command = EditCellCommand(grid_state, self.row, self.col, self.new_text)
        self.result = None

    def execute(self):
        logger.info(f"Inserting word '{self.word}' into cell ({self.row}, {self.col})")
        self.edit_command.execute()
        self.result = self.row, self.col, self.new_text     

    def undo(self):
        logger.info(f"Undoing word insertion in cell ({self.row}, {self.col}): restoring '{self.old_text}'")
        self.edit_command.undo()
