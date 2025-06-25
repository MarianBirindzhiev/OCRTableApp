from table_core import GridStateManager, NavigationController, WordInserter
from table_ui import  NavigationBar, ResizeControls, TableCanvas
from utilities import CSVExporter, LOGGER_NAME

import logging

logger = logging.getLogger(LOGGER_NAME)

class ComponentsManager:
    """
    Manages the components of the application.
    """
    def __init__(self, rows, cols):
        self.state_manager      = GridStateManager(rows, cols)
        self.nav_controller     = NavigationController()
        self.word_inserter      = WordInserter(self.state_manager, self.nav_controller)
        self.exporter           = CSVExporter()
        self.nav_bar            = NavigationBar()
        self.resize_controls    = ResizeControls(self.state_manager)
        self.canvas_table       = TableCanvas()
