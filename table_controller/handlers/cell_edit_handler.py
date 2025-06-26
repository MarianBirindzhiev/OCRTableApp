from utilities import LOGGER_NAME

import logging

logger = logging.getLogger(LOGGER_NAME)


class CellEditHandler:
    def __init__(self, controller):
        """
        Initialize the handler with the canvas table and state manager.
        
        Parameters:
        - canvas_table: The TableCanvas instance that renders the grid
        - state: GridStateManager instance that holds cell data and current position
        """
        self.controller = controller
        self._editing_cell = None
        self._editing_original_value = None

    def start_edit(self, row, col):
        """
        Called when a cell gains focus — store its original value.
        """
        logger.debug(f"Started editing cell: ({row}, {col})")        
        self._editing_cell = (row, col)
        self._editing_original_value = self.controller.canvas_table.get_entry_value(row, col)

    def finish_edit(self, row, col):
        """
        Called after cell editing is complete — update state if content changed.
        """
        if self._editing_cell != (row, col):
            return
        new_value = self.controller.canvas_table.get_entry_value(row, col)
        if new_value != self._editing_original_value:
            logger.info(f"Cell ({row}, {col}) updated from '{self._editing_original_value}' to '{new_value}'")            
            self.controller.state.save_state()
            self.controller.state.set_cell(row, col, new_value)
            self._editing_original_value = new_value