from .components_manager import ComponentsManager
from .window_manager import WindowManager
from utilities import LOGGER_NAME
from table_controller import TableGridController

import logging

logger = logging.getLogger(LOGGER_NAME)

class ControllerManager:
    """
    Manages the controllers and components of the application.
    """
    def __init__(self, rows: int, cols: int):
        self.window_manager = WindowManager()
        self.components_manager = ComponentsManager(rows, cols)

        self.controller = TableGridController(
            window_manager = self.window_manager,
            state=self.components_manager.state_manager,
            nav=self.components_manager.nav_controller,
            word_inserter=self.components_manager.word_inserter,
            exporter=self.components_manager.exporter,
            nav_bar=self.components_manager.nav_bar,
            resize_controls=self.components_manager.resize_controls,
            canvas_table=self.components_manager.canvas_table
        )

        logger.info("ControllerManager initialized with all components.")

