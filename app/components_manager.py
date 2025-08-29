from table_core import GridStateManager, NavigationController, GridCommandManager
from table_ui import  NavigationBar, LowerControls, TableCanvas
from utilities import CSVExporter, LOGGER_NAME

import logging

logger = logging.getLogger(LOGGER_NAME)

class ComponentsManager:
    """
    Manages the components of the application.
    """
    def __init__(self, rows, cols):
        self.state_manager      = GridStateManager(rows, cols)
        self.command_manager    = GridCommandManager()
        self.nav_controller     = NavigationController()
        self.exporter           = CSVExporter()
        self.nav_bar            = NavigationBar()
        self.lower_controls     = LowerControls(self.state_manager)
        self.canvas_table       = TableCanvas()
