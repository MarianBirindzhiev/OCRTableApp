from .command import Command
from utilities import LOGGER_NAME

import logging

logger = logging.getLogger(LOGGER_NAME)

class EditCellCommand(Command):
    def __init__(self, grid_state, row: int, col: int, new_text: str):
        self.grid_state = grid_state
        self.row = row
        self.col = col
        self.new_text = new_text

        if self._is_valid_cell():
            self.old_text = grid_state.get_cell(row, col)
        else:
            raise ValueError(f"Invalid cell coordinates: ({row}, {col})")

    def execute(self):
        if not self._is_valid_cell():
            logger.exception(f"Invalid cell position: ({self.row}, {self.col})")
            return
        
        self.grid_state.grid_data[self.row][self.col] = self.new_text
        self.grid_state.current_pos = (self.row, self.col)
        logger.info(f"Cell ({self.row}, {self.col}) updated from '{self.old_text}' to '{self.new_text}'")

    def undo(self):
        if not self._is_valid_cell():
            logger.exception(f"Invalid cell position: ({self.row}, {self.col})")
            return

        self.grid_state.grid_data[self.row][self.col] = self.old_text
        self.grid_state.current_pos = (self.row, self.col)
        logger.info(f"Cell ({self.row}, {self.col}) restored to '{self.old_text}'")

    def _is_valid_cell(self) -> bool:
        return (
            0 <= self.row < self.grid_state.rows and
            0 <= self.col < self.grid_state.cols
        )