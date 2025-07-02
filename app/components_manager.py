from table_core import GridStateManager, NavigationController
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
        self.exporter           = CSVExporter()
        self.nav_bar            = NavigationBar()
        self.resize_controls    = ResizeControls(self.state_manager)
        self.canvas_table       = TableCanvas()
